"""Smoke-test the documented CLIs using real fixture files."""

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(*args: str) -> str:
    result = subprocess.run(
        [sys.executable, *args],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
        check=True,
    )
    return result.stdout.strip()


def main() -> None:
    json_file = "examples/sample.json"
    csv_file = "examples/sample.csv"

    assert run("tools/json_tool.py", "--check", json_file) == ""
    formatted = json.loads(run("tools/json_tool.py", "--compact", json_file))
    assert formatted["project"] == "developer-playground"

    csv_result = json.loads(run("tools/csv_analyzer.py", "--json", csv_file))
    assert csv_result["rows"] == 3
    assert csv_result["missing_values"]["language"] == 1

    text_result = json.loads(run("tools/text_stats.py", "--json", json_file))
    assert text_result["characters"] > 0

    expected = hashlib.sha256((ROOT / json_file).read_bytes()).hexdigest()
    assert run("tools/checksum.py", json_file, "--expect", expected) == "SHA-256 verified"

    print("CLI smoke tests passed")


if __name__ == "__main__":
    main()
