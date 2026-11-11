# Developer Playground

[![Release v1.0.0](https://img.shields.io/badge/Release-v1.0.0-2ea44f?logo=github&logoColor=white)](https://github.com/muhammadsaadjalil/developer-playground/releases/tag/v1.0.0)
[![Python tests](https://github.com/muhammadsaadjalil/developer-playground/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/muhammadsaadjalil/developer-playground/actions/workflows/tests.yml)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![MIT License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen)](CONTRIBUTING.md)

**Small Python tools for everyday development tasks.** Format and validate JSON, analyze CSV data, count lines, words, and characters in text, and compute or verify SHA-256 checksums. All four tools use only the Python standard library and have automated tests.

> Built for developers, students, and anyone who wants practical command-line utilities with readable source code.

## Download v1.0.0

Download the verified v1.0.0 source code directly from GitHub: **[ZIP archive](https://github.com/muhammadsaadjalil/developer-playground/archive/refs/tags/v1.0.0.zip)** · **[TAR.GZ archive](https://github.com/muhammadsaadjalil/developer-playground/archive/refs/tags/v1.0.0.tar.gz)** · **[Release details](https://github.com/muhammadsaadjalil/developer-playground/releases/tag/v1.0.0)**.

These archives contain the Python source scripts, examples, documentation, and tests. Python 3.10 or later is required; no installation package or compiled executable is provided.

## At a glance

| Tool | What it does | Try it |
| --- | --- | --- |
| **Text Statistics** | Counts lines, words, and characters; supports JSON output | `python tools/text_stats.py --json README.md` |
| **JSON Formatter & Validator** | Pretty-prints, minifies, and validates JSON | `python tools/json_tool.py --check examples/sample.json` |
| **SHA-256 Checksum** | Hashes files in chunks and verifies an expected SHA-256 digest | `python tools/checksum.py README.md` |
| **CSV Analyzer** | Counts rows/columns and empty cells; supports JSON output | `python tools/csv_analyzer.py --json examples/sample.csv` |

**Latest stable release:** [v1.0.0](https://github.com/muhammadsaadjalil/developer-playground/releases/tag/v1.0.0) · [Version file](VERSION) · [Changelog](CHANGELOG.md) · [Release notes](docs/RELEASE_NOTES_v1.0.0.md).

**Quick start:** Requires Python 3.10 or later. Clone this repository and run any of the commands above from the repository root. See below for detailed usage and examples.

**Feedback and contributions:** [Browse issues](https://github.com/muhammadsaadjalil/developer-playground/issues) · [Suggest an improvement](https://github.com/muhammadsaadjalil/developer-playground/issues/new) · [Contributing guide](CONTRIBUTING.md)

## Available utility: Text Statistics CLI

Count lines, whitespace-separated words, and Unicode characters in UTF-8 text. Input can come from a file or from standard input. The tool uses only the Python standard library.

**Requirements:** Python 3.10 or later. No installation or third-party packages needed.

### Quick start

Clone this repository and navigate into its directory:

```bash
git clone https://github.com/muhammadsaadjalil/developer-playground.git
cd developer-playground
```

Run a file through the CLI:

```bash
python tools/text_stats.py README.md
```

Example output:

```text
lines: 52
words: 281
characters: 1760
```

*Those counts are illustrative; your actual output will depend on the input file.*

Machine-readable JSON output is available for scripts and automation:

```bash
python tools/text_stats.py --json README.md
python tools/text_stats.py --json --bytes README.md
```

Example:

```json
{"lines": 2, "words": 4, "characters": 21}
```

To read from standard input:

```bash
echo "Hello world" | python tools/text_stats.py --json
```

The optional `--bytes` flag adds the UTF-8 encoded byte count alongside the default character count, useful when diagnosing encoding and file-size differences.

For the full list of options, run `python tools/text_stats.py --help`.

### How counts work

- **Lines:** Number of lines returned by Python's `str.splitlines()`. A trailing newline does not create an extra empty line.
- **Words:** Runs of non-whitespace characters, as matched by `\S+`.
- **Characters:** Number of Python Unicode code points, including whitespace and newlines (not byte size).

### Running tests

```bash
python -m unittest discover -s tests -v
```

The same tests run automatically on pull requests and pushes to `main` through GitHub Actions. Run `python scripts/smoke_test.py` for end-to-end sample-file checks. See [Release checklist](docs/RELEASING.md) before tagging a release.

## JSON Formatter & Validator

Format, minify, or validate JSON using only the Python standard library.

```bash
python tools/json_tool.py examples/sample.json
python tools/json_tool.py --compact examples/sample.json
python tools/json_tool.py --sort-keys examples/sample.json
python tools/json_tool.py --check examples/sample.json
echo '{"name":"café","active":true}' | python tools/json_tool.py --indent 4
```

**Options:** `--sort-keys` sorts object keys for deterministic output; `--check` validates without output (exit code 0 for valid, 1 for malformed JSON); `--compact` writes minified JSON; `--indent N` sets indentation from 0 to 16 (default 2). Input errors and invalid option combinations return exit code 2. Use `--help` for details.

## CSV Analyzer CLI

Inspect CSV structure, count data rows, list column names, and identify empty values per column without external packages. Input can be a UTF-8 file or standard input.

```bash
python tools/csv_analyzer.py examples/sample.csv
python tools/csv_analyzer.py --json examples/sample.csv
python tools/csv_analyzer.py --delimiter ';' examples/sample.csv
```

The last example illustrates delimiter selection; choose a delimiter that matches your file's actual format. The CLI rejects missing/duplicate headers and inconsistent row widths, handles quoted delimiters, and returns nonzero exit codes for invalid files. It reports *empty string or whitespace-only cells* as missing values, without inferring numeric types.

## SHA-256 Checksum CLI

Calculate a SHA-256 digest for a file or compare it against a known digest. The file is read in 1 MB chunks rather than loading the entire file into memory.

```bash
python tools/checksum.py README.md
python tools/checksum.py README.md --expect 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
```

The second command demonstrates syntax with a placeholder digest and will report a mismatch unless your file happens to match it. Replace the example hash with a trusted expected SHA-256 digest for real verification. Verification exits with 0 for a match, 1 for a mismatch, or 2 for invalid inputs and file errors. SHA-256 can detect changes to a file when you already have a trusted expected digest; it does not itself establish the origin of that digest.

## Contributing

New ideas, bug fixes, and documentation improvements are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow and expectations. A collaborative JSON feature was completed through [issue #2](https://github.com/muhammadsaadjalil/developer-playground/issues/2).

## License

Released under the [MIT License](LICENSE).
