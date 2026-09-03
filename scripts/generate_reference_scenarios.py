#!/usr/bin/env python3
"""Render the seven synthetic CTC reference scenarios to stdout."""

from ctc.scenarios import reference_sha256, render_reference

print(render_reference(), end="")
print(f"# sha256 {reference_sha256()}", file=__import__("sys").stderr)
