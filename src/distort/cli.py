"""Command-line interface for Distort."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from . import __version__
from .io import DistortIOError, read_words, write_candidates
from .mutations import DEFAULT_LEVEL, MAX_LEVEL, MIN_LEVEL, generate_wordlist

_DESCRIPTION = """\
Distort generates deterministic password-mutation candidate wordlists for
authorized credential auditing, password-policy testing, and security labs.
"""

_EPILOG = """\
Input modes:
  distort WORD                  mutate one seed word
  distort -i FILE               mutate each usable line in a UTF-8 wordlist

Mutation levels:
  0-4  capitalization/lowercase/uppercase variants (legacy-equivalent range)
  5    add the first legacy suffix group
  6    add the first effective leetspeak mapping
  7    add another leet mapping and an extended suffix group
  8    add another leet mapping and additional suffixes
  9    add the final legacy-reachable leet mapping and suffix group

Output:
  Candidates are duplicate-free and lexicographically sorted. Without -o,
  candidates are written only to stdout. Status/statistics are written to stderr.

Examples:
  distort example --level 5
  distort -i examples/input.txt --level 7
  distort -i examples/input.txt -l 9 -o candidates.txt

Responsible use:
  Use only on systems you own or are explicitly authorized to assess, and stay
  within applicable laws, contracts, rules of engagement, and authorization.
"""


def _level(value: str) -> int:
    try:
        level = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("level must be an integer from 0 to 9") from exc
    if not MIN_LEVEL <= level <= MAX_LEVEL:
        raise argparse.ArgumentTypeError(
            f"level must be between {MIN_LEVEL} and {MAX_LEVEL}"
        )
    return level


def build_parser() -> argparse.ArgumentParser:
    """Build and return the Distort argument parser without parsing arguments."""
    parser = argparse.ArgumentParser(
        prog="distort",
        description=_DESCRIPTION,
        epilog=_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("word", nargs="?", metavar="WORD", help="single seed word to mutate")
    parser.add_argument(
        "-l",
        "--level",
        type=_level,
        default=DEFAULT_LEVEL,
        metavar="0-9",
        help=f"mutation level {MIN_LEVEL}-{MAX_LEVEL} (default: {DEFAULT_LEVEL})",
    )
    parser.add_argument("-i", "--input", metavar="FILE", help="read seed words from FILE")
    parser.add_argument("-o", "--output", metavar="FILE", help="write candidates to FILE")
    parser.add_argument(
        "--stats",
        action="store_true",
        help="write input/candidate counts to stderr",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="suppress output-file confirmation",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def _print_stats(input_count: int, level: int, candidate_count: int) -> None:
    print(f"Input words: {input_count}", file=sys.stderr)
    print(f"Mutation level: {level}", file=sys.stderr)
    print(f"Unique candidates: {candidate_count}", file=sys.stderr)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line interface and return a process-style exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.word is not None and args.input is not None:
        parser.error("WORD and --input cannot be used together")
    if args.word is None and args.input is None:
        parser.error("provide either WORD or --input FILE")
    if args.word is not None and not args.word.strip():
        parser.error("WORD must contain at least one non-whitespace character")

    try:
        words = [args.word] if args.word is not None else read_words(args.input)
        candidates = generate_wordlist(words, args.level)

        if args.output:
            write_candidates(args.output, candidates)
            if not args.quiet:
                print(f"Written to: {args.output}", file=sys.stderr)
        else:
            if candidates:
                sys.stdout.write("\n".join(candidates) + "\n")

        if args.stats:
            _print_stats(len(words), args.level, len(candidates))
        return 0
    except DistortIOError as exc:
        print(f"distort: error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
