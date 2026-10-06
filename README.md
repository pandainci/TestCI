# TestCI

[![CI](https://github.com/pandainci/TestCI/actions/workflows/ci.yml/badge.svg)](https://github.com/pandainci/TestCI/actions/workflows/ci.yml)

A small Python text statistics CLI with automated tests and GitHub Actions CI.
Requires Python 3.11 or newer. No third-party dependencies are needed.

## Run

Read text from standard input:

```sh
echo "Hello Python world" | python -m textstats
```

Or read a UTF-8 file:

```sh
python -m textstats README.md
```

The CLI prints JSON with character, word, and line counts. Characters include
whitespace, words are separated by whitespace, and lines follow Python's
`str.splitlines()` rules. Empty text has zero lines. A final newline does not
add an extra line.

Example output for `Hello Python world\n`:

```json
{"characters": 19, "words": 3, "lines": 1}
```

## Test locally

Run these commands from the repository root:

```sh
python -m unittest discover -s tests -v
python -m compileall -q textstats tests
```

## Continuous integration

[GitHub Actions](https://github.com/pandainci/TestCI/actions) runs on every push,
pull request, and manual dispatch. It runs the tests, checks Python compilation,
and exercises the CLI on Ubuntu with Python 3.11, 3.12, 3.13, and 3.14, plus
Windows with Python 3.14. Tests cover counting rules, Unicode, file input,
standard input, and missing-file errors.

To trigger CI manually, open **Actions → CI → Run workflow**.
