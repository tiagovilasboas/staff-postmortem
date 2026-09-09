#!/usr/bin/env python3
"""Fail if a relative Markdown link does not exist on disk. External URLs are skipped."""

from __future__ import annotations

import os
import re
import sys

LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
SKIP_PREFIXES = ("http://", "https://", "mailto:")


def iter_markdown(root: str) -> list[str]:
    paths: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {".git", "node_modules"}]
        for name in filenames:
            if name.endswith(".md"):
                paths.append(os.path.join(dirpath, name))
    return paths


def main() -> int:
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    broken: list[str] = []
    for path in iter_markdown(root):
        text = open(path, encoding="utf-8").read()
        for match in LINK.finditer(text):
            raw = match.group(2).split()[0].strip("<>")
            if raw.startswith(SKIP_PREFIXES) or raw.startswith("#"):
                continue
            rel = raw.split("#", 1)[0]
            if not rel:
                continue
            target = os.path.normpath(os.path.join(os.path.dirname(path), rel))
            if not os.path.exists(target):
                broken.append(f"{os.path.relpath(path, root)} -> {raw}")
    if broken:
        print("Broken relative Markdown links:")
        for item in broken:
            print(f"  {item}")
        return 1
    print("Relative Markdown links: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
