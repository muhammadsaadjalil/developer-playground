# Developer Playground

Small, self-contained utilities and learning exercises built through a standard branch and pull-request workflow.

## Text statistics CLI

The Python CLI at `tools/text_stats.py` reports lines, whitespace-separated words, and Unicode characters from a UTF-8 text file or standard input. No third-party packages are required.

```bash
python tools/text_stats.py README.md
python tools/text_stats.py --json README.md
printf 'Hello world\n' | python tools/text_stats.py --json
```

The optional `--json` flag prints machine-readable values with the keys `lines`, `words`, and `characters`. Without it, the original human-readable output remains unchanged.

Run the tests from the repository root:

```bash
python -m unittest discover -s tests
```

The JSON feature and its tests were developed collaboratively through [issue #2](https://github.com/muhammadsaadjalil/developer-playground/issues/2).

## License

No license has been granted yet. A license file can be added separately if the project is to be reused by others.
