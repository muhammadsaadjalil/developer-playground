# Developer Playground

A small, open-source collection of **dependency-free Python developer utilities** with readable code, practical examples, and automated tests.

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
```

Example:

```json
{"lines": 2, "words": 4, "characters": 21}
```

To read from standard input:

```bash
echo "Hello world" | python tools/text_stats.py --json
```

For the full list of options, run `python tools/text_stats.py --help`.

### How counts work

- **Lines:** Number of lines returned by Python's `str.splitlines()`. A trailing newline does not create an extra empty line.
- **Words:** Runs of non-whitespace characters, as matched by `\S+`.
- **Characters:** Number of Python Unicode code points, including whitespace and newlines (not byte size).

### Running tests

```bash
python -m unittest discover -s tests -v
```

The same tests run automatically on pull requests and pushes to `main` through GitHub Actions.

## JSON Formatter & Validator

Format, minify, or validate JSON using only the Python standard library.

```bash
python tools/json_tool.py examples/sample.json
python tools/json_tool.py --compact examples/sample.json
python tools/json_tool.py --check examples/sample.json
echo '{"name":"café","active":true}' | python tools/json_tool.py --indent 4
```

**Options:** `--check` validates without output (exit code 0 for valid, 1 for malformed JSON); `--compact` writes minified JSON; `--indent N` sets indentation from 0 to 16 (default 2). Input errors and invalid option combinations return exit code 2. Use `--help` for details.

## Contributing

New ideas, bug fixes, and documentation improvements are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow and expectations. A collaborative JSON feature was completed through [issue #2](https://github.com/muhammadsaadjalil/developer-playground/issues/2).

## License

Released under the [MIT License](LICENSE).
