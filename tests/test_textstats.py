"""Behavioral tests for the public API and CLI."""

from dataclasses import FrozenInstanceError
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from textstats import TextStats, analyze


ROOT = Path(__file__).resolve().parents[1]


class AnalyzeTests(unittest.TestCase):
    def test_counts(self):
        cases = [
            ("", TextStats(0, 0, 0)),
            ("hello", TextStats(5, 1, 1)),
            ("hello world", TextStats(11, 2, 1)),
            ("hello\nworld\n", TextStats(12, 2, 2)),
            ("\n", TextStats(1, 0, 1)),
            ("\n\n", TextStats(2, 0, 2)),
            (" \t ", TextStats(3, 0, 1)),
            ("a\r\nb", TextStats(4, 2, 2)),
            ("a\rb", TextStats(3, 2, 2)),
            ("hello\tworld", TextStats(11, 2, 1)),
            ("café 世界", TextStats(7, 2, 1)),
            ("a\u00a0b", TextStats(3, 2, 1)),
            ("a\u2028b", TextStats(3, 2, 2)),
        ]
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(analyze(text), expected)

    def test_stats_are_immutable(self):
        stats = analyze("hello")
        with self.assertRaises(FrozenInstanceError):
            stats.words = 2


class CliTests(unittest.TestCase):
    def run_cli(self, *args, input_text=""):
        return subprocess.run(
            [sys.executable, "-m", "textstats", *args],
            input=input_text,
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=ROOT,
            check=False,
        )

    def test_stdin(self):
        result = self.run_cli(input_text="hello world\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout), {"characters": 12, "words": 2, "lines": 1}
        )
        self.assertEqual(result.stderr, "")

    def test_empty_stdin(self):
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout), {"characters": 0, "words": 0, "lines": 0}
        )

    def test_utf8_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample text.txt"
            path.write_text("café 世界\n", encoding="utf-8")
            result = self.run_cli(str(path))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout), {"characters": 8, "words": 2, "lines": 1}
        )

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_cli(str(Path(directory) / "missing.txt"))
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("textstats:", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_invalid_utf8_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.txt"
            path.write_bytes(b"\xff")
            result = self.run_cli(str(path))
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("textstats:", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_help(self):
        result = self.run_cli("--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Count characters, words, and lines.", result.stdout)

    def test_extra_arguments_are_rejected(self):
        result = self.run_cli("one", "two")
        self.assertEqual(result.returncode, 2)
        self.assertIn("unrecognized arguments", result.stderr)


if __name__ == "__main__":
    unittest.main()
