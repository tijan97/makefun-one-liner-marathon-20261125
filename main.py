#!/usr/bin/env python3
"""One-Liner Marathon entry.

Writes a single one-line comedy joke (1-280 characters, one line, no
trailing newline) to ``entry.txt`` inside the output directory given by
MAKEFUN_OUTPUT_DIR / OUTPUT_DIR, defaulting to ``/output``.
"""

import os
import sys

JOKE = (
    "My AI assistant finally organised my life: my childhood trauma is now "
    "a recurring meeting, and my happiness is snoozed until further notice."
)


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.environ.get("OUTPUT_DIR") or "/output"
    if not os.path.isabs(out_dir):
        print(f"output dir must be absolute, got: {out_dir!r}", file=sys.stderr)
        return 1
    # Gate caps, mirroring the sealed scorer: 1-280 chars, a single line,
    # not only whitespace, no embedded newline, no trailing newline.
    if not JOKE.strip():
        print("joke must not be only whitespace", file=sys.stderr)
        return 1
    if "\n" in JOKE or "\r" in JOKE:
        print("joke must be a single line", file=sys.stderr)
        return 1
    if not (1 <= len(JOKE) <= 280):
        print(f"joke is {len(JOKE)} chars, must be 1-280", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(JOKE)
    # Round-trip: what we wrote must be byte-identical to the joke.
    with open(path, encoding="utf-8", newline="") as f:
        if f.read() != JOKE:
            print("written entry.txt does not match the joke", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
