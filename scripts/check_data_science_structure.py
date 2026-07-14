#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_SCIENCE_ROOT = ROOT / "data-science"
LINK_RE = re.compile(r"\(([^)#]+\.md)(?:#[^)]+)?\)")
BAD_H1_RE = re.compile(r"^#\s+(Introduction|.+Documentation)\s*$", re.MULTILINE)


def iter_readmes() -> list[Path]:
    return sorted(DATA_SCIENCE_ROOT.rglob("README.md"))


def linked_markdown_targets(readme: Path) -> set[Path]:
    text = readme.read_text(encoding="utf-8")
    linked: set[Path] = set()
    for match in LINK_RE.finditer(text):
        target = (readme.parent / match.group(1)).resolve()
        if target.exists():
            linked.add(target)
    return linked


def sibling_markdown_files(readme: Path) -> list[Path]:
    return sorted(
        p.resolve()
        for p in readme.parent.iterdir()
        if p.suffix == ".md" and p.name != "README.md"
    )


def check_readme_coverage() -> list[str]:
    errors: list[str] = []
    for readme in iter_readmes():
        linked = linked_markdown_targets(readme)
        missing = [p.name for p in sibling_markdown_files(readme) if p not in linked]
        if missing:
            rel = readme.relative_to(ROOT)
            errors.append(f"{rel}: missing links to sibling notes -> {', '.join(missing)}")
    return errors


def check_h1_quality() -> list[str]:
    errors: list[str] = []
    for readme in iter_readmes():
        text = readme.read_text(encoding="utf-8")
        if BAD_H1_RE.search(text):
            rel = readme.relative_to(ROOT)
            errors.append(f"{rel}: generic H1 title still present")
    return errors


def check_top_level_index_coverage() -> list[str]:
    errors: list[str] = []
    top_level_readme = DATA_SCIENCE_ROOT / "README.md"
    linked = linked_markdown_targets(top_level_readme)
    expected = sorted((p.resolve() for p in DATA_SCIENCE_ROOT.glob("*/README.md")))
    missing = [p.parent.name for p in expected if p not in linked]
    if missing:
        rel = top_level_readme.relative_to(ROOT)
        errors.append(
            f"{rel}: missing top-level section links -> {', '.join(missing)}"
        )
    return errors


def main() -> int:
    errors = []
    errors.extend(check_readme_coverage())
    errors.extend(check_h1_quality())
    errors.extend(check_top_level_index_coverage())

    if errors:
        for error in errors:
            print(error)
        print(f"\nFound {len(errors)} data-science structure issue(s).")
        return 1

    print(
        "Checked data-science structure: every README links to sibling notes, the top-level index covers every top-level section, and no generic README H1 titles remain."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
