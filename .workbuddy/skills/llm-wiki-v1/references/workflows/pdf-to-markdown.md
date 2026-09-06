# PDF 转 Markdown（PaddleOCR）工作流 - Reference

把 `raw/` 中的 PDF 文档转换为可供 ingest 工作流直接读取的 Markdown。该能力可选：仅当 `EXTEND.md` 中配置了 `pdf_ocr` 时才启用；否则回退为询问用户是否有可用工具。

## 触发条件(trigger)

- 用户将 PDF 放入 `raw/`，并指示 LLM 摄取该文件。
- 用户明确要求“把这个 PDF 转成 markdown”“OCR 这个 PDF”等。

## 前置条件

- `EXTEND.md` 中已配置 `pdf_ocr.token`（必填），以及可选的 `model`、`endpoint`、开关与 `poll_interval`。
- 运行环境已安装 `requests`。缺失时执行 `pip install requests`。

## Step 0：预检

1. 按 `references/config/extend-schema.md` 的查找顺序读取 active `EXTEND.md`，简要说明当前启用的偏好文件。
2. 检查 `pdf_ocr.token` 是否已填写；若缺失，引导用户在 `EXTEND.md` 中补全后再继续，不得硬编码或改用其他来源。
3. 确认待转换文件存在于 `raw/`。

## Step 1：运行转换脚本

读取 `EXTEND.md` 的 `pdf_ocr.*`，把配置映射为脚本参数后运行：

```bash
python scripts/pdf_to_markdown.py \
  --input "raw/{filename}.pdf" \
  --output-dir raw \
  --token "{pdf_ocr.token}" \
  --model "{pdf_ocr.model}"
```

`scripts/pdf_to_markdown.py` 位于已安装的 skill 包内；若在生成的 wiki 目录下运行，请替换为 skill 脚本的实际路径。

可选开关按 `EXTEND.md` 取值传递：`--use-doc-orientation-classify`、`--use-doc-unwarping`、`--use-chart-recognition`；`poll_interval` 映射为 `--poll-interval`。

## Step 2：校验输出

转换完成后确认：

- 生成 `raw/{stem}.md`（与 PDF 同名的合并 Markdown）。
- 图片保存到 `raw/assets/{stem}/`（`raw/{stem}.md` 中的图片引用已指向该目录）。
- 抽查开头与结尾，确认页码顺序、内容完整、无乱码。

## Step 3：转交摄取

将生成的 `raw/{stem}.md` 作为来源，按 `references/workflows/ingest.md` 继续摄取。原始 PDF 保留在 `raw/` 作为不可变证据，不做修改。

## 错误处理

| 症状                 | 处理                                                                      |
| -------------------- | ------------------------------------------------------------------------- |
| HTTP 401 / 403       | 令牌无效或无权限；检查 `EXTEND.md` 的 `pdf_ocr.token` 后重试。            |
| 任务 state 为 failed | 记录脚本输出的 `errorMsg`，反馈给用户；必要时调整模型或文件后重试。       |
| 轮询长时间无进展     | 检查网络与 `pdf_ocr.endpoint`，必要时中止并重试。                         |
| 图片下载失败         | 脚本会打印警告并跳过；Markdown 文本仍会保留，后续可在 ingest 时补充说明。 |

## 规则

- 不得把 `pdf_ocr.token` 写入生成的 wiki、`wiki/log.md` 或任何输出页面。
- 转换产出的 `raw/{stem}.md` 与图片属于 `raw/` 下的新增文件，不覆盖已有来源文件。
- 非 PDF 输入不使用本工作流，仍走 `ingest.md` 的既有分类处理。
