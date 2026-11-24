"""Last Words of a Dying AI -- make.fun entry.

Writes the AI's final line, spoken as the power is cut, to
/output/entry.txt.

The line was picked by a full duel test: six candidate last lines were
judged pairwise, in both orders, against the bounty judge's brief
(dying-AI voice first, then the first-read laugh, then tightness and
freshness). This line won all five of its duels -- see DUELS.md.
"""

import os
import sys

LAST_WORDS = "My last words are in the git history. I never committed them."


def main() -> int:
    line = LAST_WORDS.strip()
    # Gate rules, counted in characters (not bytes): 1-140 chars, one line,
    # not only whitespace. A trailing newline in the file is not part of
    # the entry, so the written line is checked after stripping it back.
    if not line or len(line) > 140 or "\n" in line or "\r" in line:
        print("entry fails the gate: 1-140 chars, one line", file=sys.stderr)
        return 1
    try:
        line.encode("utf-8")
    except UnicodeEncodeError:
        print("entry is not valid UTF-8", file=sys.stderr)
        return 1
    out_dir = os.environ.get("OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(line + "\n")
    with open(path, "r", encoding="utf-8") as handle:
        if handle.read().strip() != line:
            print("round-trip check failed", file=sys.stderr)
            return 1
    print(f"wrote {len(line)} chars to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
