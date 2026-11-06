# Distort

Distort is a small Python utility that turns a seed word or seed wordlist into deterministic password-mutation candidates for authorized credential auditing, password-policy testing, red-team engagements, and security labs.

Distort is a **wordlist generator**. It does not authenticate to services, collect credentials or hashes, discover targets, or crack passwords itself.

## What Distort Does

Distort preserves the original project's mutation model: lowercase/uppercase/capitalized variants, legacy leetspeak substitutions, level-controlled suffixes, and duplicate suppression. The refactored implementation separates mutation logic, file handling, and CLI behavior so each part can be tested independently.

User-visible candidate output is now deterministic: candidates are deduplicated and then sorted lexicographically before being written.

## Responsible Use

Use Distort only on systems you own or have explicit permission to assess, including approved penetration tests, authorized red-team engagements, password-policy audits, CTF/lab environments, and defensive security research. You are responsible for complying with applicable laws, contracts, rules of engagement, organizational policies, and authorization boundaries.

See [RESPONSIBLE_USE.md](RESPONSIBLE_USE.md) for the concise project policy.

## Features

- Single-word or file-based seed input
- Mutation levels `0` through `9`
- Capitalization, lowercase, uppercase, leetspeak, and suffix transformations
- Duplicate suppression with deterministic output ordering
- UTF-8 file handling and clear validation errors
- Optional output statistics on stderr
- Installable `distort` console command
- Compatibility wrapper for `./distort.py`
- Unit and CLI tests with `pytest`
- Lightweight synthetic mutation-generation benchmark
- GitHub Actions Python-version matrix with test and coverage job summaries
- No runtime dependencies outside the Python standard library

## Installation

Distort requires Python 3.10 or newer.

```bash
python -m pip install -e .
```

Then verify the console command:

```bash
distort --help
```

For development:

```bash
python -m pip install -e ".[dev]"
```

## Quick Start

Mutate a single synthetic seed word using the default level (`5`):

```bash
distort example
```

Choose a mutation level explicitly:

```bash
distort example --level 5
```

Read seed words from a file:

```bash
distort -i examples/input.txt --level 7
```

Write candidates to a file:

```bash
distort -i examples/input.txt -l 9 -o candidates.txt
```

## CLI Reference

```text
usage: distort [-h] [-l 0-9] [-i FILE] [-o FILE] [--stats] [--quiet]
               [--version]
               [WORD]
```

Core options:

- `WORD`: mutate one seed word.
- `-i, --input FILE`: read seed words from a UTF-8 text file.
- `-l, --level 0-9`: choose the mutation level; default is `5`.
- `-o, --output FILE`: write candidates to a file instead of stdout.
- `--stats`: report input count, level, and unique candidate count to stderr.
- `--quiet`: suppress non-error status messages such as output-file confirmation.
- `--version`: print the installed Distort version.

`WORD` and `--input` are mutually exclusive. Levels outside `0-9` fail with an argparse error instead of being silently clamped.

## Mutation Levels

The level thresholds intentionally preserve the original script's **effective** behavior.

| Level | Effective behavior |
| --- | --- |
| `0-4` | Base capitalization/lowercase/uppercase variants. These levels are legacy-equivalent. |
| `5` | Adds the first suffix group. The historical empty leet mapping means no effective leet change yet. |
| `6` | Adds the first effective leetspeak mapping. |
| `7` | Adds another leet mapping and the second suffix group. |
| `8` | Adds another leet mapping and the third suffix group. |
| `9` | Adds the final legacy-reachable leet mapping and fourth suffix group. |

The original source contains four additional leetspeak pattern dictionaries that cannot be reached with the historical `level - 4` slice while the valid level range is `0-9`. They are retained in the source as documented legacy data, but the refactor does not silently make them active because that would change level-9 output.

## Examples

Synthetic input:

```bash
distort example --level 5
```

The exact output is deterministic. A short excerpt is:

```text
EXAMPLE
EXAMPLE!
EXAMPLE.
EXAMPLE1
Example
Example!
```

Higher levels generate more candidates. Actual candidate counts depend on both the seed text and selected level.

### Statistics

```bash
distort example -l 7 --stats > candidates.txt
```

Candidates remain on stdout, while statistics are emitted to stderr:

```text
Input words: 1
Mutation level: 7
Unique candidates: 126
```

## File Input

Input files are read as UTF-8 text. Blank or whitespace-only lines are ignored. Each usable seed is stripped and lowercased before mutation, matching the original script's normalization behavior. Duplicate seeds are allowed, but duplicate generated candidates are removed.

Expected input errors—such as a missing file, directory path, invalid UTF-8 file, or file containing no usable words—produce a concise error without a traceback.

## Writing Output

Without `--output`, Distort writes only candidate lines to stdout, so normal shell redirection remains safe:

```bash
distort example -l 7 > candidates.txt
```

With `--output`, the file is written as UTF-8 with one candidate per line and a final newline:

```bash
distort example -l 7 -o candidates.txt
```

Status messages and `--stats` output use stderr rather than contaminating candidate stdout.

## Hashcat / John Integration

Distort remains focused on offline candidate generation. For example:

```bash
distort -i seeds.txt -l 7 -o candidates.txt
```

The resulting `candidates.txt` can then be supplied as a candidate wordlist to an **authorized** Hashcat or John the Ripper workflow. Distort intentionally does not add hash collection, network authentication, password spraying, credential stuffing, target discovery, or automated account access.

## Before and After

### Before

The original direct-script usage remains recognizable:

```bash
./distort.py -l 9 -i passwordlist.txt -o disortedlist.txt
```

### After

The installed CLI provides the same core workflow with clearer validation and deterministic output:

```bash
distort -i passwordlist.txt --level 9 --output distorted-list.txt
```

Single-word input is now a first-class documented mode:

```bash
distort example --level 5
```

The root compatibility wrapper still supports the original style:

```bash
./distort.py -l 9 -i passwordlist.txt -o distortedlist.txt
```

### Compatibility notes

The mutation candidate sets remain legacy-compatible for valid levels, with deterministic sorting added at the output boundary. Intentional behavior changes are limited to error handling and ambiguous/invalid input:

- Levels below `0` or above `9` now fail instead of being silently clamped.
- Supplying both `WORD` and `--input` now fails instead of silently ignoring the file.
- Blank input lines are ignored instead of being treated as an empty seed that can create suffix-only candidates.
- Expected file errors return non-zero status codes without a traceback.
- Output-file confirmation and statistics use stderr; candidate stdout stays pipeline-safe.

## Bundled Wordlists and Provenance

The legacy wordlists are preserved in the repository, but their origins and redistribution permissions are not all verified. A local heuristic review also flagged potentially structured/contact-like entries in `passwordlist.txt`; this is not proof of leaked data, but it requires manual review before further distribution.

See [WORDLISTS.md](WORDLISTS.md) for the file inventory, provenance leads, local scan summary, SHA-256 fingerprints, and release recommendations. The MIT licence for Distort's original source code does not automatically cover third-party wordlists. The lists are not required by the package or test suite; examples and tests use synthetic inputs.

## Benchmark Results

The benchmark measures **Distort mutation generation only** using synthetic input words. It does not measure password-cracking speed. The following results were measured on **2026-11-06** in this environment using the median of three runs per case.

**Environment:** Python 3.13.5 (CPython); Linux 6.18.57; x86_64.

| Input words | Level | Unique candidates | Median elapsed | Candidates/second |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 5 | 18 | 0.000062 s | 288,878 |
| 1 | 9 | 266 | 0.001802 s | 147,599 |
| 100 | 5 | 1,800 | 0.006474 s | 278,052 |
| 100 | 9 | 26,600 | 0.167145 s | 159,143 |
| 1,000 | 5 | 18,000 | 0.065683 s | 274,045 |
| 1,000 | 9 | 266,000 | 1.693341 s | 157,086 |

Reproduce the benchmark after installing the development package:

```bash
python benchmarks/benchmark.py
```

The script prints the Python and operating-system details and measures a median of three runs for each workload. Inputs are generated synthetic strings (`example0000`, etc.). Results vary with hardware, operating system, Python version, and workload; these figures are illustrative, not performance guarantees.

## Development

Install development dependencies:

```bash
python -m pip install -e ".[dev]"
```

The project intentionally keeps runtime dependencies empty.

## Running Tests

```bash
pytest
```

For local coverage:

```bash
pytest --cov=distort --cov-report=term-missing
```

Tests use temporary files and synthetic words. They do not require Hashcat, John the Ripper, network access, external password databases, or real credentials.

## Project Structure

```text
Distort/
├── .github/workflows/tests.yml
├── Wordlists/
│   ├── 10-million-password-list-top-1000000.txt
│   ├── 500-worst-passwords.txt
│   └── passwordlist.txt
├── benchmarks/benchmark.py
├── examples/
│   ├── README.md
│   └── input.txt
├── src/distort/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── io.py
│   └── mutations.py
├── tests/
│   ├── test_cli.py
│   ├── test_io.py
│   └── test_mutations.py
├── 10k-most-commonlist.txt
├── README.md
├── RESPONSIBLE_USE.md
├── WORDLISTS.md
├── distort.py
├── passwordlist.txt
├── pyproject.toml
├── requirements-dev.txt
└── .gitignore
```

## Contributing

Keep changes small, testable, deterministic, and scoped to offline candidate generation. New mutation behavior should include tests and clear documentation, especially when it changes an existing level's output.

Before opening a pull request, run:

```bash
pytest
```

## Responsible Disclosure / Security

For a vulnerability in Distort itself, avoid publishing sensitive exploit details before the maintainer has had an opportunity to review them. Use the repository's available private security-reporting channel when one is configured.

## License

Distort's original Python source code is released under the MIT License.

See the [LICENSE](LICENSE) file for the full licence text.

The MIT License applies to the original Distort source code; bundled wordlists and other third-party assets have separate, unresolved provenance and redistribution conditions. See [WORDLISTS.md](WORDLISTS.md) before redistributing those assets.
