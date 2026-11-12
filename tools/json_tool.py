#!/usr/bin/env python3
"""Validate, pretty-print, or minify JSON from a file or standard input."""

import argparse
import json
import sys
from pathlib import Path


def reject_constant(token: str) -> None:
    raise ValueError(f"{token} is not a valid JSON constant")


def parse_json(text: str):
    return json.loads(text.removeprefix("\ufeff"), parse_constant=reject_constant)


def format_json(text: str, *, compact: bool = False, indent: int = 2, sort_keys: bool = False) -> str:
    """Return normalized JSON, or raise an error if it cannot be formatted."""
    output = json.dumps(
        parse_json(text), ensure_ascii=False, allow_nan=False, sort_keys=sort_keys,
        indent=None if compact else indent, separators=(",", ":") if compact else None,
    )
    # Preserve escaped lone surrogates without emitting invalid UTF-8.
    return output.encode("utf-8", errors="backslashreplace").decode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", nargs="?", type=Path, help="JSON input file (default: stdin)")
    parser.add_argument("--check", action="store_true", help="Validate only; don't print JSON")
    parser.add_argument("--compact", action="store_true", help="Print minified JSON")
    parser.add_argument("--sort-keys", action="store_true", help="Sort object keys for reproducible output")
    parser.add_argument("--indent", type=int, default=2, help="Indent width (default: 2)")
    args = parser.parse_args()
    if args.check and args.compact:
        parser.error("--check and --compact cannot be combined")
    if args.indent < 0 or args.indent > 16:
        parser.error("--indent must be between 0 and 16")
    try:
        raw = args.file.read_bytes() if args.file else sys.stdin.buffer.read()
        text = raw.decode("utf-8")
        if args.check:
            parse_json(text)
            return 0
        output = format_json(text, compact=args.compact, indent=args.indent, sort_keys=args.sort_keys)
    except (OSError, UnicodeError) as error:
        print(f"Input error: {error}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as error:
        print(f"Invalid JSON at line {error.lineno}, column {error.colno}: {error.msg}", file=sys.stderr)
        return 1
    except (ValueError, RecursionError) as error:
        print(f"JSON error: {error}", file=sys.stderr)
        return 1
    sys.stdout.reconfigure(encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
