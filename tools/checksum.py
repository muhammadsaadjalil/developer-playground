#!/usr/bin/env python3
"""Calculate or verify the SHA-256 digest of a file."""

import argparse
import hashlib
import re
import sys
from pathlib import Path


def sha256_file(path: Path) -> str:
    """Hash a file in chunks so memory usage remains bounded."""
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="File to hash or verify")
    parser.add_argument("--expect", help="Expected 64-character hexadecimal SHA-256 digest")
    args = parser.parse_args()
    if args.expect is not None and not re.fullmatch(r"[0-9a-fA-F]{64}", args.expect):
        parser.error("--expect must be a 64-character hexadecimal SHA-256 digest")

    try:
        digest = sha256_file(args.file)
    except OSError as error:
        print(f"File error: {error}", file=sys.stderr)
        return 2

    if args.expect is not None:
        if digest.lower() == args.expect.lower():
            print("SHA-256 verified")
            return 0
        print(f"SHA-256 mismatch: actual {digest}", file=sys.stderr)
        return 1

    print(digest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
