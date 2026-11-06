from pathlib import Path

import pytest

from distort.io import InputFileError, OutputFileError, read_words, write_candidates
from distort.mutations import generate_wordlist


def test_read_words_valid_file_ignores_blank_lines(tmp_path: Path) -> None:
    input_file = tmp_path / "input.txt"
    input_file.write_text("Example\n\n security \n\t\n", encoding="utf-8")
    assert read_words(input_file) == ["Example", " security "]


def test_read_words_empty_file_fails(tmp_path: Path) -> None:
    input_file = tmp_path / "empty.txt"
    input_file.write_text("\n \n\t\n", encoding="utf-8")
    with pytest.raises(InputFileError, match="no usable words"):
        read_words(input_file)


def test_read_words_missing_file_fails(tmp_path: Path) -> None:
    with pytest.raises(InputFileError, match="does not exist"):
        read_words(tmp_path / "missing.txt")


def test_read_words_directory_fails(tmp_path: Path) -> None:
    with pytest.raises(InputFileError, match="not a file"):
        read_words(tmp_path)


def test_read_words_invalid_utf8_fails(tmp_path: Path) -> None:
    input_file = tmp_path / "invalid.txt"
    input_file.write_bytes(b"example\n\xff\n")
    with pytest.raises(InputFileError, match="valid UTF-8"):
        read_words(input_file)


def test_duplicate_file_words_are_suppressed_during_generation(tmp_path: Path) -> None:
    input_file = tmp_path / "input.txt"
    input_file.write_text("example\nEXAMPLE\nexample\n", encoding="utf-8")
    assert generate_wordlist(read_words(input_file), 5) == generate_wordlist(["example"], 5)


def test_write_candidates_creates_file_with_final_newline(tmp_path: Path) -> None:
    output_file = tmp_path / "output.txt"
    write_candidates(output_file, ["alpha", "beta"])
    assert output_file.read_bytes() == b"alpha\nbeta\n"


def test_write_candidates_rejects_directory(tmp_path: Path) -> None:
    with pytest.raises(OutputFileError, match="is a directory"):
        write_candidates(tmp_path, ["alpha"])


def test_write_candidates_rejects_missing_parent(tmp_path: Path) -> None:
    output_file = tmp_path / "missing" / "output.txt"
    with pytest.raises(OutputFileError, match="directory does not exist"):
        write_candidates(output_file, ["alpha"])


def test_read_words_permission_error_is_wrapped(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    input_file = tmp_path / "protected.txt"
    input_file.write_text("example\n", encoding="utf-8")
    original_open = Path.open

    def denied_open(path: Path, *args: object, **kwargs: object):
        if path == input_file:
            raise PermissionError("permission denied")
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, "open", denied_open)
    with pytest.raises(InputFileError, match="not readable"):
        read_words(input_file)


def test_read_words_os_error_is_wrapped(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    input_file = tmp_path / "unavailable.txt"
    input_file.write_text("example\n", encoding="utf-8")
    original_open = Path.open

    def failing_open(path: Path, *args: object, **kwargs: object):
        if path == input_file:
            raise OSError("device unavailable")
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, "open", failing_open)
    with pytest.raises(InputFileError, match="could not read input file"):
        read_words(input_file)


def test_write_candidates_rejects_parent_that_is_a_file(tmp_path: Path) -> None:
    parent_file = tmp_path / "not-a-directory"
    parent_file.write_text("x", encoding="utf-8")
    with pytest.raises(OutputFileError, match="parent is not a directory"):
        write_candidates(parent_file / "output.txt", ["alpha"])


def test_write_candidates_empty_iterable_creates_empty_file(tmp_path: Path) -> None:
    output_file = tmp_path / "empty.txt"
    write_candidates(output_file, [])
    assert output_file.read_bytes() == b""


def test_write_candidates_permission_error_is_wrapped(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    output_file = tmp_path / "protected.txt"

    def denied_write(
        path: Path, data: str, *args: object, **kwargs: object
    ) -> int:
        if path == output_file:
            raise PermissionError("permission denied")
        return 0

    monkeypatch.setattr(Path, "write_text", denied_write)
    with pytest.raises(OutputFileError, match="not writable"):
        write_candidates(output_file, ["alpha"])


def test_write_candidates_os_error_is_wrapped(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    output_file = tmp_path / "broken.txt"

    def failing_write(
        path: Path, data: str, *args: object, **kwargs: object
    ) -> int:
        if path == output_file:
            raise OSError("device unavailable")
        return 0

    monkeypatch.setattr(Path, "write_text", failing_write)
    with pytest.raises(OutputFileError, match="could not write output file"):
        write_candidates(output_file, ["alpha"])
