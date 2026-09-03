#!/usr/bin/env python3
"""使用 PaddleOCR HTTP API 把 PDF 文档转换为 Markdown。

这是 llm-wiki-bootstrap skill 的自有辅助脚本，不会复制进生成的 wiki。
令牌(token)必须通过 --token 传入，来源为 EXTEND.md 的 pdf_ocr.token。

用法示例：
    python scripts/pdf_to_markdown.py \
        --input "raw/foo.pdf" \
        --output-dir raw \
        --token "<pdf_ocr.token>"

输入可以是本地 PDF 路径，也可以是 http(s) 的 URL。
输出：
  raw/{stem}.md              合并后的整篇 Markdown
  raw/assets/{stem}/         文档内嵌图片（Markdown 中的引用已指向此处）
  raw/assets/{stem}/output/  版面解析输出图

依赖：requests（缺失时请先运行 pip install requests）。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import NoReturn
from urllib.parse import urlparse

try:
    import requests
except ImportError:  # pragma: no cover - 取决于运行环境
    sys.stderr.write("缺少依赖 requests。请先运行：pip install requests\n")
    sys.exit(1)

DEFAULT_ENDPOINT = "https://paddleocr.aistudio-app.com/api/v2/ocr/jobs"
DEFAULT_MODEL = "PaddleOCR-VL-1.6"


def fail(message: str, code: int = 1) -> NoReturn:
    sys.stderr.write(f"错误：{message}\n")
    sys.exit(code)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="使用 PaddleOCR 把 PDF 转换为 Markdown",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--input", required=True, help="本地 PDF 路径或 http(s) URL"
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="输出目录；默认与输入文件同目录（URL 输入时为当前目录）",
    )
    parser.add_argument(
        "--token",
        required=True,
        help="PaddleOCR 访问令牌（取自 EXTEND.md 的 pdf_ocr.token）",
    )
    parser.add_argument(
        "--model", default=DEFAULT_MODEL, help=f"OCR 模型名，默认 {DEFAULT_MODEL}"
    )
    parser.add_argument(
        "--endpoint",
        default=DEFAULT_ENDPOINT,
        help="任务提交地址，默认 PaddleOCR 官方地址",
    )
    parser.add_argument(
        "--use-doc-orientation-classify",
        action="store_true",
        help="启用文档方向分类",
    )
    parser.add_argument(
        "--use-doc-unwarping", action="store_true", help="启用文档展平"
    )
    parser.add_argument(
        "--use-chart-recognition", action="store_true", help="启用图表识别"
    )
    parser.add_argument(
        "--poll-interval",
        type=float,
        default=5.0,
        help="轮询任务状态的间隔秒数，默认 5",
    )
    return parser.parse_args()


def is_url(path: str) -> bool:
    return path.startswith("http://") or path.startswith("https://")


def input_stem(path: str) -> str:
    if is_url(path):
        name = os.path.basename(urlparse(path).path) or "document"
    else:
        name = os.path.basename(path)
    stem, _ext = os.path.splitext(name)
    return stem or "document"


def submit_job(
    args: argparse.Namespace, headers: dict, optional_payload: dict
) -> requests.Response:
    if is_url(args.input):
        headers["Content-Type"] = "application/json"
        payload = {
            "fileUrl": args.input,
            "model": args.model,
            "optionalPayload": optional_payload,
        }
        return requests.post(args.endpoint, json=payload, headers=headers)

    if not os.path.exists(args.input):
        fail(f"文件不存在：{args.input}")

    data = {
        "model": args.model,
        "optionalPayload": json.dumps(optional_payload),
    }
    with open(args.input, "rb") as handle:
        files = {"file": handle}
        return requests.post(
            args.endpoint, headers=headers, data=data, files=files
        )


def poll_job(args: argparse.Namespace, headers: dict, job_id: str) -> str:
    while True:
        response = requests.get(f"{args.endpoint}/{job_id}", headers=headers)
        if response.status_code != 200:
            fail(
                f"查询任务状态失败，HTTP {response.status_code}: {response.text}"
            )
        data = response.json().get("data", {})
        state = data.get("state")

        if state == "pending":
            print("当前任务状态：pending（排队中）")
        elif state == "running":
            progress = data.get("extractProgress", {})
            total = progress.get("totalPages")
            extracted = progress.get("extractedPages")
            if total is not None and extracted is not None:
                print(f"当前任务状态：running（总页数 {total}，已提取 {extracted}）")
            else:
                print("当前任务状态：running")
        elif state == "done":
            progress = data.get("extractProgress", {})
            print(
                f"任务完成：已提取 {progress.get('extractedPages')} 页，"
                f"开始时间 {progress.get('startTime')}，结束时间 {progress.get('endTime')}"
            )
            return data.get("resultUrl", {}).get("jsonUrl", "")
        elif state == "failed":
            fail(f"任务失败：{data.get('errorMsg', '未知原因')}")
        else:
            print(f"未知状态：{state}")

        time.sleep(args.poll_interval)


def save_image(url: str, destination: Path) -> None:
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"警告：下载图片失败 {url}：{exc}")
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(response.content)
    print(f"图片已保存：{destination}")


def rewrite_image_refs(text: str, image_path: str, relative_path: str) -> str:
    """把 Markdown 文本中对 image_path 的引用改写为 relative_path。"""
    if image_path in text:
        return text.replace(image_path, relative_path)
    basename = os.path.basename(image_path)
    if basename and basename in text:
        return text.replace(basename, relative_path)
    return text


def main() -> None:
    args = parse_args()
    headers = {"Authorization": f"bearer {args.token}"}
    optional_payload = {
        "useDocOrientationClassify": args.use_doc_orientation_classify,
        "useDocUnwarping": args.use_doc_unwarping,
        "useChartRecognition": args.use_chart_recognition,
    }

    print(f"正在处理：{args.input}")
    response = submit_job(args, headers, optional_payload)
    print(f"提交响应：HTTP {response.status_code}")
    if response.status_code != 200:
        if response.status_code in (401, 403):
            fail(
                "令牌无效或无权限，请检查 EXTEND.md 中的 pdf_ocr.token "
                f"（HTTP {response.status_code}）"
            )
        fail(f"提交失败，HTTP {response.status_code}: {response.text}")

    job_id = response.json()["data"]["jobId"]
    print(f"任务提交成功，jobId: {job_id}")
    print("开始轮询结果……")

    jsonl_url = poll_job(args, headers, job_id)
    if not jsonl_url:
        fail("任务完成但未返回结果地址")

    jsonl_response = requests.get(jsonl_url)
    jsonl_response.raise_for_status()

    stem = input_stem(args.input)
    if args.output_dir:
        output_dir = Path(args.output_dir)
    elif not is_url(args.input):
        output_dir = Path(args.input).resolve().parent
    else:
        output_dir = Path.cwd()
    output_dir.mkdir(parents=True, exist_ok=True)

    assets_dir = output_dir / "assets" / stem
    md_path = output_dir / f"{stem}.md"

    md_parts: list[str] = []
    page_num = 0
    for line in jsonl_response.text.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        result = json.loads(line).get("result", {})
        for res in result.get("layoutParsingResults", []):
            markdown = res.get("markdown", {})
            text = markdown.get("text", "")

            # 文档内嵌图片：保存并修正 Markdown 引用
            for image_path, image_url in markdown.get("images", {}).items():
                local_name = f"p{page_num:02d}_{os.path.basename(image_path)}"
                local_path = assets_dir / local_name
                save_image(image_url, local_path)
                text = rewrite_image_refs(
                    text, image_path, f"assets/{stem}/{local_name}"
                )

            if text:
                md_parts.append(text)

            # 版面解析输出图
            for image_name, image_url in res.get("outputImages", {}).items():
                output_name = f"p{page_num:02d}_{image_name}"
                if not os.path.splitext(output_name)[1]:
                    output_name += ".jpg"
                save_image(image_url, assets_dir / "output" / output_name)

            page_num += 1

    if not md_parts:
        fail("转换结果为空，未提取到任何 Markdown 内容")

    content = "\n\n".join(part.strip() for part in md_parts).strip() + "\n"
    md_path.write_text(content, encoding="utf-8")
    print(f"Markdown 已保存：{md_path}")
    print(f"共处理 {page_num} 个版面结果。")


if __name__ == "__main__":
    main()
