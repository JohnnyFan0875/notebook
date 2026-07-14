#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEGACY_PATHS = [
    ROOT / "mkdocs.yml",
    ROOT / ".gitbook",
    ROOT / "site",
    ROOT / "docs",
    ROOT / "docs" / "javascripts",
    ROOT / "docs" / "stylesheets",
]
MARKDOWN_FILES = sorted(
    {
        path
        for path in ROOT.rglob("*.md")
        if ".git/" not in str(path)
    }
)

FORBIDDEN_PATTERNS = [
    (re.compile(r"^\?\?\?\s", re.MULTILINE), "MkDocs admonition syntax (`???`)"),
    (re.compile(r'^===\s+"[^"]+"', re.MULTILINE), "MkDocs tabs syntax (`=== \"...\"`)"),
    (re.compile(r"\{\s*\.img-center\s*\}"), "MkDocs attribute list (`{ .img-center }`)"),
    (re.compile(r"\.gitbook/assets/"), "legacy `.gitbook/assets` image path"),
    (re.compile(r"--8<--"), "MkDocs snippet include syntax"),
]

LINK_RE = re.compile(r"(!?)\[[^\]]*]\(([^)]+)\)")


def is_relative_target(target: str) -> bool:
    if not target or target.startswith("#"):
        return False
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
        return False
    return True


def normalize_target(target: str) -> str:
    target = target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    return target


def check_forbidden_patterns(path: Path, text: str) -> list[str]:
    errors: list[str] = []
    for pattern, description in FORBIDDEN_PATTERNS:
        if pattern.search(text):
            errors.append(f"{path}: contains {description}")
    return errors


def check_links(path: Path, text: str) -> list[str]:
    errors: list[str] = []
    for _bang, raw_target in LINK_RE.findall(text):
        target = normalize_target(raw_target).split("#", 1)[0].strip()
        if not is_relative_target(target):
            continue
        resolved = (path.parent / target).resolve()
        try:
            resolved.relative_to(ROOT)
        except ValueError:
            errors.append(f"{path}: link escapes repository root -> {raw_target}")
            continue
        if not resolved.exists():
            errors.append(f"{path}: missing local target -> {raw_target}")
    return errors


def check_legacy_paths() -> list[str]:
    errors: list[str] = []
    for path in LEGACY_PATHS:
        if path.exists():
            errors.append(f"{path.relative_to(ROOT)}: legacy MkDocs-era path still exists")
    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(check_legacy_paths())
    for path in MARKDOWN_FILES:
        text = path.read_text(encoding="utf-8")
        errors.extend(check_forbidden_patterns(path.relative_to(ROOT), text))
        errors.extend(check_links(path.relative_to(ROOT), text))

    if errors:
        for error in errors:
            print(error)
        print(f"\nFound {len(errors)} issue(s).")
        return 1

    print(f"Checked {len(MARKDOWN_FILES)} Markdown files: no MkDocs-specific syntax or broken local links found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
