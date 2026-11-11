import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.checksum import sha256_file


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "checksum.py"


class ChecksumTests(unittest.TestCase):
    def test_known_digest(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.txt"
            path.write_bytes(b"abc")
            self.assertEqual(sha256_file(path), hashlib.sha256(b"abc").hexdigest())

    def test_empty_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty"
            path.write_bytes(b"")
            self.assertEqual(sha256_file(path), hashlib.sha256(b"").hexdigest())

    def test_large_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "large.bin"
            content = b"0123456789" * 150000
            path.write_bytes(content)
            self.assertEqual(sha256_file(path), hashlib.sha256(content).hexdigest())

    def test_cli_verify_success_and_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data"
            path.write_bytes(b"abc")
            expected = hashlib.sha256(b"abc").hexdigest()
            accepted = subprocess.run(
                [sys.executable, str(SCRIPT), str(path), "--expect", expected.upper()],
                capture_output=True, text=True,
            )
            self.assertEqual(accepted.returncode, 0)
            rejected = subprocess.run(
                [sys.executable, str(SCRIPT), str(path), "--expect", "0" * 64],
                capture_output=True, text=True,
            )
            self.assertEqual(rejected.returncode, 1)
            self.assertIn("mismatch", rejected.stderr)

    def test_cli_missing_file(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "missing-sha256-file-5487"],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 2)

    def test_cli_invalid_expected_digest(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "not-needed", "--expect", "bad"],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
