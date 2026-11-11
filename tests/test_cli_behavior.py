"""Integration tests for the public command-line interface."""

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "text_stats.py"


class CliBehaviorTests(unittest.TestCase):
    def run_cli(self, *args: str, input_text: str = "") -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            input=input_text,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )

    def test_default_output_preserves_readable_format(self):
        result = self.run_cli(input_text="Hello world\n")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "lines: 1\nwords: 2\ncharacters: 12\n")
        self.assertEqual(result.stderr, "")

    def test_missing_input_file_reports_error(self):
        missing_file = ROOT / "__missing_text_stats_input_9b7f__.txt"
        result = self.run_cli(str(missing_file))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("error:", result.stderr.lower())

    def test_help_lists_json_option(self):
        result = self.run_cli("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("--json", result.stdout)


if __name__ == "__main__":
    unittest.main()
