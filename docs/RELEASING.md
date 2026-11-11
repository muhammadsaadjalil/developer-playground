# Release checklist

Developer Playground is a source-based collection of Python scripts rather than an installable package. A release can be created from a tested Git commit.

## Before a release

1. Check that documentation and sample commands match the current scripts.
2. Ensure the PR test matrix passes on Python 3.10, 3.11, 3.12, and 3.13.
3. Run `python -m unittest discover -s tests -v` locally.
4. Run `python scripts/smoke_test.py` to exercise all CLIs with the sample files.
5. Review the Git diff for accidental secrets or generated files.
6. Confirm the README, LICENSE, and CONTRIBUTING guidance remain accurate.
7. Create a meaningful version tag and GitHub release only after the checked commit has been merged.
8. Describe actual functionality and breaking changes, if any; do not invent downloads, ratings or adoption figures.

## Testing a downloaded release

Requires Python 3.10+; no runtime third-party dependencies.

```bash
python -m unittest discover -s tests -v
python scripts/smoke_test.py
```

Releases should stay small, reproducible and truthful.
