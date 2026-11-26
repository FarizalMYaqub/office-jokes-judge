"""Office-jokes entry: writes one joke line to the output directory.

The competition gate requires /output/entry.txt to be UTF-8 text of
1 to 199 characters, not only white space. This program writes the
line with no trailing newline, so the file holds exactly the joke.
"""

import os
import sys

JOKE = (
    "Our AI notetaker summarized the hour-long meeting in four words "
    "\u2014 'we'll meet again tomorrow' \u2014 the first honest minutes "
    "in company history."
)


def output_dir() -> str:
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main() -> int:
    text = JOKE
    if not 1 <= len(text) <= 199:
        print(f"entry text length {len(text)} outside 1..199", file=sys.stderr)
        return 1
    if not text.strip():
        print("entry text is only white space", file=sys.stderr)
        return 1
    if len(text.encode("utf-8")) > 199:
        print("entry text exceeds 199 UTF-8 bytes", file=sys.stderr)
        return 1
    out = output_dir()
    os.makedirs(out, exist_ok=True)
    staging = os.path.join(out, "entry.staging.txt")
    target = os.path.join(out, "entry.txt")
    with open(staging, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    with open(staging, "r", encoding="utf-8", newline="") as handle:
        staged = handle.read()
    if staged != text:
        print("staging read-back mismatch", file=sys.stderr)
        return 1
    os.replace(staging, target)
    with open(target, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != text:
        print("final read-back mismatch", file=sys.stderr)
        return 1
    print(f"wrote {len(text)} characters to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
