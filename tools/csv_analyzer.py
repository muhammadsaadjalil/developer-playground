#!/usr/bin/env python3
"""Summarize CSV files from disk or standard input without external packages."""

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path


def analyze_csv(text: str, *, delimiter: str = ",") -> dict:
    """Return a CSV summary; raise ValueError on malformed headers or rows."""
    import io

    reader = csv.reader(io.StringIO(text.removeprefix("\ufeff"), newline=""), delimiter=delimiter, strict=True)
    try:
        headers = next(reader)
    except StopIteration as error:
        raise ValueError("CSV is empty") from error
    if not headers or any(not header.strip() for header in headers):
        raise ValueError("CSV must have nonempty column headers")
    if len(set(headers)) != len(headers):
        raise ValueError("CSV has duplicate column headers")

    empty_counts = Counter({name: 0 for name in headers})
    row_count = 0
    for row in reader:
        if len(row) != len(headers):
            raise ValueError(
                f"Row {reader.line_num}: expected {len(headers)} columns; found {len(row)}"
            )
        row_count += 1
        for name, value in zip(headers, row):
            if not value.strip():
                empty_counts[name] += 1
    return {
        "rows": row_count,
        "columns": len(headers),
        "column_names": headers,
        "missing_values": dict(empty_counts),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", nargs="?", type=Path, help="CSV input file (default: stdin)")
    parser.add_argument("--delimiter", default=",", help="One-character field delimiter")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()
    if len(args.delimiter) != 1:
        parser.error("--delimiter must be a single character")
    try:
        raw = args.file.read_bytes() if args.file else sys.stdin.buffer.read()
        text = raw.decode("utf-8")
        result = analyze_csv(text, delimiter=args.delimiter)
    except (OSError, UnicodeError) as error:
        print(f"Input error: {error}", file=sys.stderr)
        return 2
    except (ValueError, csv.Error) as error:
        print(f"Invalid CSV: {error}", file=sys.stderr)
        return 1

    sys.stdout.reconfigure(encoding="utf-8")
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"Rows: {result['rows']}")
        print(f"Columns: {result['columns']}")
        for name in result["column_names"]:
            print(f"{name}: {result['missing_values'][name]} empty value(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
