import json
import subprocess
import sys
import unittest
from pathlib import Path

from tools.csv_analyzer import analyze_csv


SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "csv_analyzer.py"


def run_cli(*args, input_text=""):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        input=input_text,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )


class CsvAnalyzerTests(unittest.TestCase):
    def test_counts_rows_and_missing_values(self):
        result = analyze_csv("name,city\nAlice,Lahore\nBob,\n")
        self.assertEqual(result["rows"], 2)
        self.assertEqual(result["columns"], 2)
        self.assertEqual(result["missing_values"], {"name": 0, "city": 1})

    def test_quoted_commas(self):
        result = analyze_csv('name,notes\nAlice,"one,two"\n')
        self.assertEqual(result["rows"], 1)

    def test_utf8_bom_in_stdin(self):
        result = run_cli("--json", input_text="\\ufeffname,city\\nAlice,Lahore\\n")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["column_names"], ["name", "city"])

    def test_quoted_multiline_field(self):
        result = analyze_csv('name,notes\\nAlice,"first\\nsecond"\\n')
        self.assertEqual(result["rows"], 1)
        self.assertEqual(result["missing_values"], {"name": 0, "notes": 0})

    def test_unclosed_quote_rejected(self):
        with self.assertRaisesRegex(Exception, "unexpected end"):
            analyze_csv('name,notes\\nAlice,"unfinished')

    def test_header_only(self):
        self.assertEqual(analyze_csv("a,b\n")["rows"], 0)

    def test_duplicate_headers_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            analyze_csv("a,a\n1,2\n")

    def test_inconsistent_row_rejected(self):
        with self.assertRaisesRegex(ValueError, "expected 2 columns"):
            analyze_csv("a,b\n1\n")

    def test_empty_csv_rejected(self):
        with self.assertRaisesRegex(ValueError, "empty"):
            analyze_csv("")

    def test_non_comma_delimiter(self):
        self.assertEqual(analyze_csv("a;b\n1;2\n", delimiter=";")["rows"], 1)

    def test_cli_json_mode(self):
        result = run_cli("--json", input_text="a,b\n1,\n")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["missing_values"]["b"], 1)

    def test_cli_bad_input_code(self):
        result = run_cli(input_text="a,b\n1\n")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Invalid CSV", result.stderr)

    def test_cli_invalid_delimiter(self):
        result = run_cli("--delimiter", "::", input_text="a,b\n")
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
