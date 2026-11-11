import json
import subprocess
import sys
import unittest
from pathlib import Path

from tools.json_tool import format_json


SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "json_tool.py"


def run_cli(*args, input_text=""):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        input=input_text,
        capture_output=True,
        encoding="utf-8",
        text=True,
        check=False,
    )


class JsonToolTests(unittest.TestCase):
    def test_pretty_unicode(self):
        data = json.loads(format_json('{"name":"café","items":[1,2]}'))
        self.assertEqual(data, {"name": "café", "items": [1, 2]})

    def test_compact_output(self):
        self.assertEqual(format_json('{"x": 1, "y": true}', compact=True), '{"x":1,"y":true}')

    def test_cli_check_valid_silent(self):
        result = run_cli("--check", input_text='{"ok":true}')
        self.assertEqual((result.returncode, result.stdout), (0, ""))

    def test_cli_invalid_json_returns_nonzero_and_location(self):
        result = run_cli("--check", input_text='{"bad":}')
        self.assertEqual(result.returncode, 1)
        self.assertIn("line 1", result.stderr)
        self.assertIn("column", result.stderr)

    def test_cli_compact_and_check_conflict(self):
        result = run_cli("--check", "--compact", input_text="{}")
        self.assertEqual(result.returncode, 2)

    def test_cli_indent_out_of_range(self):
        result = run_cli("--indent", "-1", input_text="{}")
        self.assertEqual(result.returncode, 2)

    def test_sort_keys_pretty_nested(self):
        result = format_json('{"z":{"b":1,"a":2},"a":0}', sort_keys=True)
        self.assertLess(result.index('"a": 0'), result.index('"z":'))
        self.assertLess(result.index('"a": 2'), result.index('"b": 1'))

    def test_sort_keys_compact_cli(self):
        result = run_cli("--sort-keys", "--compact", input_text='{"z":2,"a":1}')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), '{"a":1,"z":2}')

    def test_default_preserves_order(self):
        self.assertEqual(format_json('{"z":2,"a":1}', compact=True), '{"z":2,"a":1}')

    def test_empty_input_invalid(self):
        result = run_cli(input_text="")
        self.assertEqual(result.returncode, 1)

    def test_cli_unicode_roundtrip(self):
        result = run_cli("--compact", input_text='{"emoji":"☕"}')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout), {"emoji": "☕"})


if __name__ == "__main__":
    unittest.main()
