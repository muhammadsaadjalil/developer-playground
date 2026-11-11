#!/usr/bin/env python3
"""Print simple text statistics from a UTF-8 file or standard input."""

import argparse
import re
import sys
from pathlib import Path


def summarize(text: str) -> dict[str, int]:
    """Return line, word and character counts for text."""
    return {
        "lines": len(text.splitlines()),
        "words": len(re.findall(r"\S+", text)),
        "characters": len(text),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", nargs="?", type=Path, help="UTF-8 file (default: stdin)")
    args = parser.parse_args()
    try:
        text = args.file.read_text(encoding="utf-8") if args.file else sys.stdin.read()
    except (OSError, UnicodeError) as error:
        parser.error(str(error))
    for key, value in summarize(text).items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
