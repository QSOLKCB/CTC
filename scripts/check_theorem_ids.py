#!/usr/bin/env python3
"""Fail if the CTC-MATH theorem inventory disagrees across normative files and Lean sources."""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
ID_RE = re.compile(r"CTC-MATH-\d{3}")


def ids(text: str) -> set[str]:
    return set(ID_RE.findall(text))


def markdown_section(text: str, heading: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    capture = False
    for line in lines:
        if line.startswith("## "):
            if capture:
                break
            capture = line.startswith(heading)
            continue
        if capture:
            out.append(line)
    if not out:
        raise SystemExit(f"missing markdown section beginning {heading!r}")
    return "\n".join(out)


def main() -> int:
    spec = (ROOT / "spec/ctc-core-v0.1.yaml").read_text(encoding="utf-8")
    plan = (ROOT / "docs/FORMALIZATION-PLAN.md").read_text(encoding="utf-8")
    core = (ROOT / "docs/MATHEMATICAL-CORE-v0.1.md").read_text(encoding="utf-8")
    roadmap = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")

    lean_files = sorted((ROOT / "CTC").glob("*.lean"))
    if not lean_files:
        raise SystemExit("no CTC/*.lean theorem sources found")
    lean_text = "\n".join(path.read_text(encoding="utf-8") for path in lean_files)

    inventories = {
        "spec/ctc-core-v0.1.yaml formal_targets": ids(spec.split("formal_targets:", 1)[1]),
        "docs/FORMALIZATION-PLAN.md §12": ids(markdown_section(plan, "## 12.")),
        "docs/MATHEMATICAL-CORE-v0.1.md §13": ids(markdown_section(core, "## 13.")),
        "ROADMAP.md PR 2": ids(markdown_section(roadmap, "## PR 2")),
        "CTC/*.lean": ids(lean_text),
    }

    expected = {f"CTC-MATH-{n:03d}" for n in range(1, 17)}
    ok = True
    for name, found in inventories.items():
        missing = sorted(expected - found)
        extra = sorted(found - expected)
        if missing:
            print(f"::error::{name} missing: {', '.join(missing)}")
            ok = False
        if extra:
            print(f"::error::{name} unexpected: {', '.join(extra)}")
            ok = False

    if all(found == expected for found in inventories.values()):
        print("CTC theorem inventory agrees across normative files and Lean sources")
    print("inventory:", ", ".join(sorted(expected)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
