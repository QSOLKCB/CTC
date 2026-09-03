#!/usr/bin/env python3
"""Audit trusted CTC Lean source text before compilation.

This is deliberately a source-provenance guard, not the kernel-level axiom audit.
The GitHub Actions workflow also runs lean-action's axiom-audit and leanchecker.
"""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
TRUSTED = sorted((ROOT / "CTC").glob("*.lean"))
FORBIDDEN = re.compile(r"\b(?:axiom|sorry|admit)\b")


def strip_comments_and_strings(text: str) -> str:
    """Replace Lean comments and strings with spaces while preserving newlines."""
    out: list[str] = []
    i = 0
    block_depth = 0
    in_string = False
    while i < len(text):
        if block_depth:
            if text.startswith("/-", i):
                block_depth += 1
                out.extend("  ")
                i += 2
            elif text.startswith("-/", i):
                block_depth -= 1
                out.extend("  ")
                i += 2
            else:
                out.append("\n" if text[i] == "\n" else " ")
                i += 1
            continue
        if in_string:
            if text[i] == "\\" and i + 1 < len(text):
                out.extend("  ")
                i += 2
            elif text[i] == '"':
                in_string = False
                out.append(" ")
                i += 1
            else:
                out.append("\n" if text[i] == "\n" else " ")
                i += 1
            continue
        if text.startswith("--", i):
            j = text.find("\n", i)
            if j == -1:
                out.extend(" " * (len(text) - i))
                break
            out.extend(" " * (j - i))
            out.append("\n")
            i = j + 1
            continue
        if text.startswith("/-", i):
            block_depth = 1
            out.extend("  ")
            i += 2
            continue
        if text[i] == '"':
            in_string = True
            out.append(" ")
            i += 1
            continue
        out.append(text[i])
        i += 1
    if block_depth:
        raise ValueError("unterminated block comment")
    if in_string:
        raise ValueError("unterminated string literal")
    return "".join(out)


def main() -> int:
    if not TRUSTED:
        print("::error::no trusted CTC/*.lean sources found")
        return 1
    ok = True
    for path in TRUSTED:
        rel = path.relative_to(ROOT)
        try:
            stripped = strip_comments_and_strings(path.read_text(encoding="utf-8"))
        except ValueError as exc:
            print(f"::error file={rel}::{exc}")
            ok = False
            continue
        for match in FORBIDDEN.finditer(stripped):
            line = stripped.count("\n", 0, match.start()) + 1
            print(f"::error file={rel},line={line}::forbidden trusted-source token: {match.group(0)}")
            ok = False
    if ok:
        print(f"trusted-source audit passed for {len(TRUSTED)} Lean files")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
