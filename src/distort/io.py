"""Text-file input and output helpers for Distort."""

from collections.abc import Iterable
from pathlib import Path


class DistortIOError(Exception):
    """Base exception for expected Distort file errors."""


class InputFileError(DistortIOError):
    """Raised when an input wordlist cannot be used."""


class OutputFileError(DistortIOError):
    """Raised when generated candidates cannot be written."""


def read_words(path: str | Path) -> list[str]:
    """Read usable non-blank lines from a UTF-8 wordlist file."""
    input_path = Path(path)
    if not input_path.exists():
        raise InputFileError(f"input file does not exist: {input_path}")
    if not input_path.is_file():
        raise InputFileError(f"input path is not a file: {input_path}")

    try:
        with input_path.open("r", encoding="utf-8") as handle:
            words = [line.rstrip("\r\n") for line in handle if line.strip()]
    except PermissionError as exc:
        raise InputFileError(f"input file is not readable: {input_path}") from exc
    except UnicodeDecodeError as exc:
        raise InputFileError(f"input file is not valid UTF-8: {input_path}") from exc
    except OSError as exc:
        message = exc.strerror or str(exc)
        raise InputFileError(f"could not read input file {input_path}: {message}") from exc

    if not words:
        raise InputFileError(f"input file contains no usable words: {input_path}")
    return words


def write_candidates(path: str | Path, candidates: Iterable[str]) -> None:
    """Write candidates as UTF-8 text with exactly one trailing newline."""
    output_path = Path(path)
    if output_path.exists() and output_path.is_dir():
        raise OutputFileError(f"output path is a directory: {output_path}")

    parent = output_path.parent
    if not parent.exists():
        raise OutputFileError(f"output directory does not exist: {parent}")
    if not parent.is_dir():
        raise OutputFileError(f"output parent is not a directory: {parent}")

    text = "\n".join(candidates)
    if text:
        text += "\n"

    try:
        output_path.write_text(text, encoding="utf-8", newline="\n")
    except PermissionError as exc:
        raise OutputFileError(f"output location is not writable: {output_path}") from exc
    except OSError as exc:
        message = exc.strerror or str(exc)
        raise OutputFileError(f"could not write output file {output_path}: {message}") from exc
