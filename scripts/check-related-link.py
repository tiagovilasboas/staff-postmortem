#!/usr/bin/env python3
"""Fail if README Related does not point at staff-impact-cases / ops-postmortems."""

from __future__ import annotations

import os
import sys

NEEDLES: list[str] = [
    "https://github.com/tiagovilasboas/staff-impact-cases",
    "ops-postmortems",
]


def related_block(text: str) -> str | None:
    marker = "## Related"
    if marker not in text:
        return None
    rest = text.split(marker, 1)[1]
    parts = rest.split("\n## ", 1)
    return parts[0]


def main() -> int:
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    path = os.path.join(root, "README.md")
    text = open(path, encoding="utf-8").read()
    block = related_block(text)
    if block is None:
        print("README.md: missing ## Related")
        return 1
    missing = [needle for needle in NEEDLES if needle not in block]
    if missing:
        print("README.md Related: missing required link text:")
        for needle in missing:
            print(f"  {needle}")
        return 1
    print("README Related link to staff-impact-cases: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
