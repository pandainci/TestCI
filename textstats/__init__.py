"""Simple text statistics without third-party dependencies."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TextStats:
    """Character, whitespace-delimited word, and logical line counts."""

    characters: int
    words: int
    lines: int


def analyze(text: str) -> TextStats:
    """Count characters, words, and lines using Python's Unicode string rules."""
    return TextStats(
        characters=len(text),
        words=len(text.split()),
        lines=len(text.splitlines()),
    )
