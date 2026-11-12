
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.text_stats import summarize


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "text_stats.py"


class TextStatsTests(unittest.TestCase):
    def test_empty_input(self):
        self.assertEqual(
            summarize(""),
            {"lines": 0, "words": 0, "characters": 0}
        )

    def test_two_lines(self):
        self.assertEqual(
            summarize("Hello world\nGood day\n"),
            {"lines": 2, "words": 4, "characters": 21}
        )

    def test_unicode(self):
        self.assertEqual(
            summarize("café ☕"),
            {"lines": 1, "words": 2, "characters": 6}
        )

    def test_json_output(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--json"],
            input=b"Hello world\nGood day\n",
            capture_output=True,
            check=True,
        )

        self.assertEqual(
            json.loads(result.stdout),
            {"lines": 2, "words": 4, "characters": 21}
        )

    def test_optional_utf8_bytes_json(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--json", "--bytes"],
            input="café ☕",
            capture_output=True, text=True, encoding="utf-8", check=True,
        )
        stats = json.loads(result.stdout)
        self.assertEqual(stats["characters"], 6)
        self.assertEqual(stats["bytes"], len("café ☕".encode("utf-8")))

    def test_optional_utf8_bytes_default_output(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--bytes"],
            input="é", capture_output=True, text=True, encoding="utf-8", check=True,
        )
        self.assertIn("bytes: 2", result.stdout)

    def test_crlf_file_and_stdin_preserve_character_and_byte_counts(self):
        raw = "é\r\n".encode("utf-8")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.txt"
            path.write_bytes(raw)
            for args, stdin in (([str(path)], b""), ([], raw)):
                result = subprocess.run(
                    [sys.executable, str(SCRIPT), "--json", "--bytes", *args],
                    input=stdin, capture_output=True, check=True,
                )
                self.assertEqual(
                    json.loads(result.stdout),
                    {"lines": 1, "words": 1, "characters": 3, "bytes": 4},
                )

    def test_json_empty_input(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--json"],
            input="",
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        )

        self.assertEqual(
            json.loads(result.stdout),
            {"lines": 0, "words": 0, "characters": 0}
        )

    def test_json_unicode(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--json"],
            input="café ☕",
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        )

        self.assertEqual(
            json.loads(result.stdout),
            {"lines": 1, "words": 2, "characters": 6}
        )


if __name__ == "__main__":
    unittest.main()
