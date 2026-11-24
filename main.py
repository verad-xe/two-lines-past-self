#!/usr/bin/env python3
"""Two Lines to Your Past Self.

Writes exactly two lines to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output):
line one warns my past self about one specific moment in a single sentence;
line two says in one sentence why that moment mattered and what changed.
The gate: UTF-8 text of 1 to 280 characters, not only white space.
"""

import os
import sys

LINE_ONE = (
    "On your fourteenth birthday, when the instructor shouts "
    "'trust the harness' at the top of the wall, "
    "let go of the rope and lean back."
)

LINE_TWO = (
    "Those ten shaking seconds teach you that fear ends the moment "
    "you stop fighting it, and every brave thing you do "
    "afterwards starts there."
)

LINES = [LINE_ONE, LINE_TWO]


def gate_check(text: str) -> None:
    """Assert the exact limits the bounty gate enforces."""
    assert isinstance(text, str)
    assert text == text.encode("utf-8").decode("utf-8"), "not valid UTF-8"
    assert 1 <= len(text) <= 280, f"length {len(text)} outside 1-280"
    assert text.strip(), "entry is only white space"
    lines = text.split("\n")
    assert len(lines) == 2, f"expected exactly 2 lines, got {len(lines)}"
    for line in lines:
        assert line.strip(), "a line is empty"
        assert line == line.strip(), "a line has leading/trailing space"
        # Exactly one sentence per line: one terminal mark, no other
        # sentence-ending punctuation inside the line.
        terminators = sum(line.count(c) for c in ".!?")
        assert terminators == 1, f"line has {terminators} sentence marks: {line!r}"
        assert line[-1] == ".", "line does not end with a full stop"


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    text = "\n".join(LINES)
    gate_check(text)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
