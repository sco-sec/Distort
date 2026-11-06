from __future__ import annotations

import os
import runpy
import subprocess
import sys
from pathlib import Path

import pytest

from distort.cli import main

ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args: str, wrapper: bool = False) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    source = str(ROOT / "src")
    env["PYTHONPATH"] = source + os.pathsep + env.get("PYTHONPATH", "")
    command = [sys.executable, str(ROOT / "distort.py") if wrapper else "-m"]
    if not wrapper:
        command.append("distort.cli")
    command.extend(args)
    return subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def test_help() -> None:
    result = run_cli("--help")
    assert result.returncode == 0
    assert "Input modes:" in result.stdout
    assert "Mutation levels:" in result.stdout
    assert "Responsible use:" in result.stdout


def test_version() -> None:
    result = run_cli("--version")
    assert result.returncode == 0
    assert result.stdout.strip() == "distort 0.2.0"


def test_single_word_default_level() -> None:
    result = run_cli("example")
    assert result.returncode == 0
    assert len(result.stdout.splitlines()) == 18
    assert result.stdout.splitlines() == sorted(result.stdout.splitlines())
    assert result.stderr == ""


def test_single_word_explicit_level() -> None:
    result = run_cli("example", "-l", "5")
    assert result.returncode == 0
    assert len(result.stdout.splitlines()) == 18


def test_input_file(tmp_path: Path) -> None:
    input_file = tmp_path / "input.txt"
    input_file.write_text("example\nsecurity\n", encoding="utf-8")
    result = run_cli("-i", str(input_file), "-l", "0")
    assert result.returncode == 0
    assert "example" in result.stdout.splitlines()
    assert "security" in result.stdout.splitlines()


def test_input_and_output_file(tmp_path: Path) -> None:
    input_file = tmp_path / "input.txt"
    output_file = tmp_path / "output.txt"
    input_file.write_text("example\n", encoding="utf-8")
    result = run_cli("-i", str(input_file), "-o", str(output_file))
    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr.strip() == f"Written to: {output_file}"
    assert output_file.read_text(encoding="utf-8").endswith("\n")


def test_quiet_suppresses_output_file_status(tmp_path: Path) -> None:
    output_file = tmp_path / "output.txt"
    result = run_cli("example", "-o", str(output_file), "--quiet")
    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""


def test_stats_go_to_stderr_without_polluting_stdout() -> None:
    result = run_cli("example", "-l", "7", "--stats")
    assert result.returncode == 0
    assert len(result.stdout.splitlines()) == 126
    assert "Input words: 1" in result.stderr
    assert "Mutation level: 7" in result.stderr
    assert "Unique candidates: 126" in result.stderr


def test_negative_level_fails_cleanly() -> None:
    result = run_cli("example", "-l", "-1")
    assert result.returncode == 2
    assert "level must be between 0 and 9" in result.stderr
    assert "Traceback" not in result.stderr


def test_level_above_range_fails_cleanly() -> None:
    result = run_cli("example", "-l", "10")
    assert result.returncode == 2
    assert "level must be between 0 and 9" in result.stderr


def test_missing_input_file_returns_nonzero(tmp_path: Path) -> None:
    result = run_cli("-i", str(tmp_path / "does-not-exist.txt"))
    assert result.returncode == 1
    assert "input file does not exist" in result.stderr
    assert "Traceback" not in result.stderr


def test_empty_input_file_returns_nonzero(tmp_path: Path) -> None:
    input_file = tmp_path / "empty.txt"
    input_file.write_text("\n \n", encoding="utf-8")
    result = run_cli("-i", str(input_file))
    assert result.returncode == 1
    assert "no usable words" in result.stderr


def test_word_and_input_file_are_rejected_together(tmp_path: Path) -> None:
    input_file = tmp_path / "input.txt"
    input_file.write_text("security\n", encoding="utf-8")
    result = run_cli("example", "-i", str(input_file))
    assert result.returncode == 2
    assert "cannot be used together" in result.stderr


def test_missing_input_mode_is_an_argparse_error() -> None:
    result = run_cli()
    assert result.returncode == 2
    assert "provide either WORD or --input FILE" in result.stderr


def test_compatibility_wrapper_matches_module_cli() -> None:
    module = run_cli("example", "-l", "5")
    wrapper = run_cli("example", "-l", "5", wrapper=True)
    assert wrapper.returncode == module.returncode == 0
    assert wrapper.stdout == module.stdout
    assert wrapper.stderr == module.stderr


def test_importing_cli_does_not_parse_process_arguments() -> None:
    env = os.environ.copy()
    source = str(ROOT / "src")
    env["PYTHONPATH"] = source + os.pathsep + env.get("PYTHONPATH", "")
    result = subprocess.run(
        [sys.executable, "-c", "import distort.cli; print('imported')", "--unexpected"],
        cwd=ROOT.parent,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "imported"
    assert result.stderr == ""


def test_output_is_stable_across_hash_randomization_seeds() -> None:
    env_one = os.environ.copy()
    env_two = os.environ.copy()
    source = str(ROOT / "src")
    env_one["PYTHONPATH"] = source + os.pathsep + env_one.get("PYTHONPATH", "")
    env_two["PYTHONPATH"] = source + os.pathsep + env_two.get("PYTHONPATH", "")
    env_one["PYTHONHASHSEED"] = "1"
    env_two["PYTHONHASHSEED"] = "999"
    command = [sys.executable, "-m", "distort.cli", "example", "-l", "9"]
    first = subprocess.run(
        command,
        cwd=ROOT.parent,
        env=env_one,
        text=True,
        capture_output=True,
        check=False,
    )
    second = subprocess.run(
        command,
        cwd=ROOT.parent,
        env=env_two,
        text=True,
        capture_output=True,
        check=False,
    )
    assert first.returncode == second.returncode == 0
    assert first.stdout == second.stdout


def test_main_writes_single_word_candidates_to_stdout(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["example", "--level", "0"]) == 0
    captured = capsys.readouterr()
    assert captured.out.splitlines() == ["EXAMPLE", "Example", "example"]
    assert captured.err == ""


def test_main_reads_file_writes_output_and_reports_stats(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    input_file = tmp_path / "seeds.txt"
    output_file = tmp_path / "candidates.txt"
    input_file.write_text("example\nsecurity\n", encoding="utf-8")

    assert main(["--input", str(input_file), "--output", str(output_file), "--stats"]) == 0

    captured = capsys.readouterr()
    assert captured.out == ""
    assert f"Written to: {output_file}" in captured.err
    assert "Input words: 2" in captured.err
    assert "Mutation level: 5" in captured.err
    assert output_file.read_text(encoding="utf-8").endswith("\n")


def test_main_quiet_suppresses_output_confirmation(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    output_file = tmp_path / "candidates.txt"
    assert main(["example", "--output", str(output_file), "--quiet"]) == 0
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_main_returns_one_for_expected_io_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["--input", str(tmp_path / "missing.txt")]) == 1
    captured = capsys.readouterr()
    assert "input file does not exist" in captured.err
    assert "Traceback" not in captured.err


@pytest.mark.parametrize(
    "arguments",
    [
        [],
        ["example", "--level", "10"],
        ["example", "--level", "not-a-number"],
        ["example", "--input", "seeds.txt"],
        ["   "],
    ],
)
def test_main_reports_argument_errors(arguments: list[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(arguments)
    assert exc_info.value.code == 2


def test_main_version_action_exits_successfully() -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["--version"])
    assert exc_info.value.code == 0


def test_python_m_distort_entry_point(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(sys, "argv", ["distort", "example", "--level", "0"])
    with pytest.raises(SystemExit) as exc_info:
        runpy.run_module("distort.__main__", run_name="__main__")
    assert exc_info.value.code == 0
    assert capsys.readouterr().out.splitlines() == ["EXAMPLE", "Example", "example"]


def test_cli_module_direct_entry_point(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.delitem(sys.modules, "distort.cli", raising=False)
    monkeypatch.setattr(sys, "argv", ["distort", "example", "--level", "0"])
    with pytest.raises(SystemExit) as exc_info:
        runpy.run_module("distort.cli", run_name="__main__")
    assert exc_info.value.code == 0
    assert capsys.readouterr().out.splitlines() == ["EXAMPLE", "Example", "example"]
