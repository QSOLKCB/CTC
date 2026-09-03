#!/usr/bin/env python3
"""Verify that the checked-in deterministic scenario artifact matches the implementation."""

from __future__ import annotations

import hashlib
from pathlib import Path
import sys

from ctc.scenarios import render_reference

ROOT = Path(__file__).resolve().parents[1]
artifact = ROOT / "reference/scenarios-v0.1.json"
manifest = ROOT / "reference/SHA256SUMS"

expected = render_reference()
actual = artifact.read_text(encoding="utf-8")
if actual != expected:
    print("reference artifact differs from deterministic renderer", file=sys.stderr)
    sys.exit(1)

digest = hashlib.sha256(actual.encode("utf-8")).hexdigest()
tokens = manifest.read_text(encoding="utf-8").strip().split()
if tokens != [digest, artifact.name]:
    print("reference SHA256 manifest mismatch", file=sys.stderr)
    sys.exit(1)

print(f"reference scenarios verified: {digest}  {artifact.name}")
