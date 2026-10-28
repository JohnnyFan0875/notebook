"""檢查 Markdown 筆記：相對連結、anchor、圖片位置與引用。

用法：uv run --no-project check_links.py <資料夾> [<資料夾> ...]
輸出只有 `Checked N files` 代表沒有問題。
"""
import re
import sys
from pathlib import Path
from urllib.parse import unquote

IMG_EXT = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}
CODE_BLOCK = re.compile(r"```.*?```", re.S)
LINK = re.compile(r"\]\(([^)\s]+)\)")
_slug_cache = {}


def slugs(md: Path) -> set:
    # GitHub slug：小寫、移除標點（保留字母數字、空白、-、_）、空白換成 -，重複標題加 -1、-2
    if md not in _slug_cache:
        seen, in_code = set(), False
        for line in md.read_text(encoding="utf-8").splitlines():
            if line.lstrip().startswith("```"):
                in_code = not in_code
                continue
            m = None if in_code else re.match(r"^#{1,6}\s+(.+?)\s*$", line)
            if m:
                base = re.sub(r"[^\w\s-]", "", m.group(1).lower()).replace(" ", "-")
                s, i = base, 1
                while s in seen:
                    s, i = f"{base}-{i}", i + 1
                seen.add(s)
        _slug_cache[md] = seen
    return _slug_cache[md]


def check(root: Path) -> list:
    problems, all_text = [], []
    files = sorted(p for p in root.rglob("*.md") if not any(x.startswith(".") for x in p.relative_to(root).parts))
    for f in files:
        text = f.read_text(encoding="utf-8")
        all_text.append(text)
        rel = f.relative_to(root)
        for link in LINK.findall(CODE_BLOCK.sub("", text)):
            if re.match(r"^(https?:|mailto:)", link):
                continue
            path, _, anchor = link.partition("#")
            target = (f.parent / unquote(path)).resolve() if path else f
            if not target.exists():
                problems.append(f"MISSING    {rel} -> {link}")
            elif anchor and target.suffix == ".md" and unquote(anchor) not in slugs(target):
                problems.append(f"ANCHOR     {rel} -> {link}")
    joined = "\n".join(all_text)
    for img in sorted(p for p in root.rglob("*") if p.suffix.lower() in IMG_EXT and not any(x.startswith(".") for x in p.relative_to(root).parts)):
        rel = img.relative_to(root)
        if img.parent.name != "src":
            problems.append(f"NOT-IN-SRC {rel}")
        if img.name not in joined:
            problems.append(f"UNUSED     {rel}")
    print(f"Checked {len(files)} files in {root}")
    return problems


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    roots = [Path(p).resolve() for p in sys.argv[1:]] or [Path.cwd()]
    problems = [p for r in roots for p in check(r)]
    print("\n".join(problems))
    sys.exit(1 if problems else 0)
