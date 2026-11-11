# Developer Playground v1.0.0

**First stable release — Python CLI developer utilities**

Developer Playground v1.0.0 packages four small, open-source command-line tools implemented with the Python standard library. They are designed for direct use from source, readable code, and practical developer workflows.

## Included tools

- **Text Statistics:** count lines, whitespace-delimited words, Unicode characters, and optional UTF-8 bytes; use file or stdin; output JSON when needed.
- **JSON Formatter & Validator:** validate JSON, display useful parsing locations, pretty-print or compact it, and optionally sort object keys.
- **CSV Analyzer:** count data rows, inspect column headers, and report blank cells per column. Supports quoted fields, configurable delimiters, and JSON output.
- **SHA-256 Checksum:** calculate file checksums or compare them with a trusted expected digest while reading files in chunks.

## Get started

Requires **Python 3.10 or newer**. No pip installation or third-party runtime dependencies.

Download the source archive from this GitHub release or clone the repository. From the repository root:

```bash
python tools/text_stats.py --json README.md
python tools/json_tool.py --check examples/sample.json
python tools/csv_analyzer.py --json examples/sample.csv
python tools/checksum.py examples/sample.json
```

## Quality and compatibility

- Automated unit tests plus CLI smoke tests.
- GitHub Actions test matrix: **Python 3.10, 3.11, 3.12, and 3.13**.
- MIT licensed; contributions welcome.

## Distribution and limitations

- **Source release only.** No PyPI package, compiled binary, installer, or API service is included.
- CSV empty-value detection treats empty and whitespace-only cells as blank; it does not infer data types.
- A SHA-256 digest detects differences against a *trusted* expected digest but does not prove the source of that digest.

See [README.md](../README.md), [CHANGELOG.md](../CHANGELOG.md), and [CONTRIBUTING.md](../CONTRIBUTING.md).

Thank you for trying Developer Playground. Issues and meaningful contributions are welcome.
