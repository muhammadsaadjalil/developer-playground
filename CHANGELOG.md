# Changelog

Notable changes to Developer Playground are recorded here.

## [1.0.0] - 2026-11-11

First stable source-based release of the dependency-free Python developer utilities.

### Added

- **Text Statistics CLI:** UTF-8 text line, word, and character counts; standard input; JSON output; optional UTF-8 byte counts.
- **JSON Formatter & Validator:** formatting, compact output, validity checking, detailed syntax errors, configurable indentation, and deterministic key sorting.
- **CSV Analyzer:** row/column summaries, column names, counts of blank cells, configurable delimiter, and JSON output.
- **SHA-256 Checksum CLI:** chunked file hashing and expected-digest verification with documented exit codes.
- Python standard-library unit tests and sample-file CLI smoke tests.
- GitHub Actions test matrix covering Python 3.10–3.13.
- MIT license, contribution guide, example files, and release checklist.

### Notes

- This is a collection of standalone scripts; it is **not** published as a pip-installable package or to PyPI.
- No runtime third-party Python dependencies are required.
- This is the first versioned release; no prior versioned API or migration path is implied.
