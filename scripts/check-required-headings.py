#!/usr/bin/env python3
"""Fail if template or worked examples drop or reorder required H2 sections."""

from __future__ import annotations

import os
import sys

REQUIRED: list[str] = [
    "## Summary",
    "## Impact",
    "## Timeline",
    "## Detection",
    "## What happened",
    "## Root cause",
    "## Contributing factors",
    "## What went well",
    "## Evidence checklist",
    "## Actions",
    "## Follow-ups",
    "## Conclusion Q&A",
]

TARGETS: list[str] = [
    "docs/template.md",
    "docs/example-checkout-latency.md",
    "docs/example-short-spike.md",
]


def h2_headings(text: str) -> list[str]:
    found: list[str] = []
    for line in text.splitlines():
        if line.startswith("## ") and not line.startswith("### "):
            found.append(line.strip())
    return found


def is_subsequence(required: list[str], found: list[str]) -> bool:
    iterator = iter(found)
    return all(heading in iterator for heading in required)


def main() -> int:
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    failed = 0
    for rel in TARGETS:
        path = os.path.join(root, rel)
        if not os.path.isfile(path):
            print(f"missing file: {rel}")
            failed += 1
            continue
        text = open(path, encoding="utf-8").read()
        found = h2_headings(text)
        missing = [heading for heading in REQUIRED if heading not in found]
        if missing:
            print(f"{rel}: missing headings:")
            for heading in missing:
                print(f"  {heading}")
            failed += 1
            continue
        if not is_subsequence(REQUIRED, found):
            print(f"{rel}: required headings out of order.")
            print("  found H2:")
            for heading in found:
                print(f"    {heading}")
            failed += 1
            continue
        print(f"{rel}: headings ok")
    if failed:
        return 1
    print("Required headings: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
