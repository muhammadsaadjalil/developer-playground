#!/usr/bin/env python3
"""Validate, pretty-print, or minify JSON from a file or standard input."""

import argparse
import json
import sys
from pathlib import Path


def format_json(text: str, *, compact: bool = False, indent: int = 2) -> str:
    """Return normalized JSON, or raise JSONDecodeError for invalid input."""
    value = json.loads(text)
    if compact:
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return json.dumps(value, ensure_ascii=False, indent=indent)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", nargs="?", type=Path, help="JSON input file (default: stdin)")
    parser.add_argument("--check", action="store_true", help="Validate only; don't print JSON")
    parser.add_argument("--compact", action="store_true", help="Print minified JSON")
    parser.add_argument("--indent", type=int, default=2, help="Indent width (default: 2)")
    args = parser.parse_args()
    if args.check and args.compact:
        parser.error("--check and --compact cannot be combined")
    if args.indent < 0 or args.indent > 16:
        parser.error("--indent must be between 0 and 16")
    try:
        text = args.file.read_text(encoding="utf-8") if args.file else sys.stdin.read()
        output = format_json(text, compact=args.compact, indent=args.indent)
    except (OSError, UnicodeError) as error:
        print(f"Input error: {error}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as error:
        print(f"Invalid JSON at line {error.lineno}, column {error.colno}: {error.msg}", file=sys.stderr)
        return 1
    if not args.check:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
