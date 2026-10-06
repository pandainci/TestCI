"""Run with python -m textstats [UTF-8 file]."""

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys

from textstats import analyze


def main() -> int:
    parser = argparse.ArgumentParser(description="Count characters, words, and lines.")
    parser.add_argument("file", nargs="?", type=Path, help="UTF-8 file (default: stdin)")
    args = parser.parse_args()

    try:
        text = args.file.read_text(encoding="utf-8") if args.file else sys.stdin.read()
    except (OSError, UnicodeError) as exc:
        print(f"textstats: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(asdict(analyze(text))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
