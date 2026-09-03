#!/usr/bin/env python3
"""Fail if the frozen CTC theorem inventory disagrees across contracts and Lean declarations."""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
ID_RE = re.compile(r"CTC-MATH-\d{3}")
PLAN_PAIR_RE = re.compile(r"^(CTC-MATH-\d{3})\s+([A-Za-z_][A-Za-z0-9_']*)\s*$", re.MULTILINE)


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

    lean_files = [ROOT / "CTC.lean", *sorted((ROOT / "CTC").rglob("*.lean"))]
    missing_sources = [path for path in lean_files if not path.is_file()]
    if missing_sources:
        raise SystemExit(
            "missing Lean source(s): "
            + ", ".join(str(path.relative_to(ROOT)) for path in missing_sources)
        )
    lean_text = "\n".join(path.read_text(encoding="utf-8") for path in lean_files)

    plan_section = markdown_section(plan, "## 12.")
    plan_pairs = dict(PLAN_PAIR_RE.findall(plan_section))

    expected = {f"CTC-MATH-{n:03d}" for n in range(1, 17)}
    ok = True
    if set(plan_pairs) != expected:
        missing = sorted(expected - set(plan_pairs))
        extra = sorted(set(plan_pairs) - expected)
        if missing:
            print(f"::error::formalisation plan missing ID/name pairs: {', '.join(missing)}")
        if extra:
            print(f"::error::formalisation plan has unexpected ID/name pairs: {', '.join(extra)}")
        ok = False

    inventories = {
        "spec/ctc-core-v0.1.yaml formal_targets": ids(spec.split("formal_targets:", 1)[1]),
        "docs/FORMALIZATION-PLAN.md §12": ids(plan_section),
        "docs/MATHEMATICAL-CORE-v0.1.md §13": ids(markdown_section(core, "## 13.")),
        "ROADMAP.md PR 2": ids(markdown_section(roadmap, "## PR 2")),
        "trusted Lean sources": ids(lean_text),
    }

    for label, found in inventories.items():
        missing = sorted(expected - found)
        extra = sorted(found - expected)
        if missing:
            print(f"::error::{label} missing: {', '.join(missing)}")
            ok = False
        if extra:
            print(f"::error::{label} unexpected: {', '.join(extra)}")
            ok = False

    # Bind every frozen ID to the exact theorem declaration named by the normative plan.
    # Requiring the ID in the theorem's immediately preceding doc comment prevents a
    # stale ID comment elsewhere from masking a deleted or renamed formal claim.
    for theorem_id, theorem_name in sorted(plan_pairs.items()):
        bound = re.compile(
            rf"/-.*?\b{re.escape(theorem_id)}\b.*?-/\s*"
            rf"theorem\s+{re.escape(theorem_name)}\b",
            re.DOTALL,
        )
        if not bound.search(lean_text):
            print(
                f"::error::trusted Lean sources do not bind {theorem_id} "
                f"to theorem {theorem_name}"
            )
            ok = False

    if ok:
        print("CTC theorem inventory and ID-to-declaration bindings agree")
    print(
        "inventory:",
        ", ".join(f"{theorem_id}={plan_pairs.get(theorem_id, '?')}" for theorem_id in sorted(expected)),
    )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
