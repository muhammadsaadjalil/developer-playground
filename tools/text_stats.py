#!/usr/bin/env python3
"""Print simple text statistics from a UTF-8 file or standard input."""

import argparse
import json
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
    parser.add_argument("--json", action="store_true", help="Print statistics as JSON")
    parser.add_argument("--bytes", action="store_true", help="Include UTF-8 byte count")
    args = parser.parse_args()
    try:
        raw = args.file.read_bytes() if args.file else sys.stdin.buffer.read()
        text = raw.decode("utf-8")
    except (OSError, UnicodeError) as error:
        parser.error(str(error))
    statistics = summarize(text)
    if args.bytes:
        statistics["bytes"] = len(raw)
    if args.json:
        print(json.dumps(statistics, ensure_ascii=False))
    else:
        for key, value in statistics.items():
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()
