from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skill"
MIRROR_ROOT = REPO_ROOT / ".agents" / "skills" / "llm-wiki-v1"
FIXTURES_ROOT = Path(__file__).resolve().parent / "fixtures"

CONCEPT_TYPES = (
    "原理",
    "机制",
    "方法",
    "模型／框架",
    "分类",
    "区分",
    "状态／属性",
    "评价标准",
    "产出",
)

EXPORT_FIELDS = (
    "chunk_id",
    "page_path",
    "title",
    "type",
    "heading_path",
    "ordinal",
    "sources",
    "tags",
    "updated",
    "text",
)

DUAL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\([^()]+\)\.md$")
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(64 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_frontmatter(text: str) -> dict[str, str]:
    normalized = text.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        return {}
    end = normalized.find("\n---\n", 4)
    if end < 0:
        return {}
    result: dict[str, str] = {}
    for line in normalized[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    return result


def section(text: str, heading: str) -> str:
    normalized = text.replace("\r\n", "\n")
    marker = f"## {heading}\n"
    start = normalized.find(marker)
    if start < 0:
        raise AssertionError(f"missing section: {heading}")
    start += len(marker)
    end = normalized.find("\n## ", start)
    return normalized[start : end if end >= 0 else None].strip()


def copy_test_wiki(destination: Path) -> Path:
    resolved_destination = destination.resolve()
    try:
        resolved_destination.relative_to(REPO_ROOT.resolve())
    except ValueError:
        pass
    else:
        raise ValueError(
            f"test wiki destination must be outside the repository: {destination}"
        )

    shutil.copytree(FIXTURES_ROOT / "wiki", destination / "wiki")
    shutil.copytree(FIXTURES_ROOT / "raw", destination / "raw")
    scripts_dir = destination / "scripts"
    scripts_dir.mkdir(parents=True)
    shutil.copy2(
        SKILL_ROOT / "references" / "templates" / "wiki_fts.py",
        scripts_dir / "wiki_fts.py",
    )
    return destination


def run_bm25(root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["PYTHONUTF8"] = "1"
    environment["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(
        [sys.executable, str(root / "scripts" / "wiki_fts.py"), *arguments],
        cwd=root,
        env=environment,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
