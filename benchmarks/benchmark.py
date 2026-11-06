#!/usr/bin/env python3
"""Reproducible synthetic benchmark for Distort mutation generation."""

from __future__ import annotations

import platform
import sys
from statistics import median
from time import perf_counter

from distort.mutations import generate_wordlist

CASES = (
    (1, 5),
    (1, 9),
    (100, 5),
    (100, 9),
    (1_000, 5),
    (1_000, 9),
)
REPEATS = 3


def synthetic_words(count: int) -> list[str]:
    """Create deterministic, non-sensitive benchmark input words."""
    return [f"example{index:04d}" for index in range(count)]


def benchmark_case(input_count: int, level: int) -> tuple[int, float, float]:
    """Return unique candidate count, median seconds, and throughput."""
    words = synthetic_words(input_count)
    durations: list[float] = []
    candidate_count: int | None = None

    for _ in range(REPEATS):
        started = perf_counter()
        candidates = generate_wordlist(words, level)
        durations.append(perf_counter() - started)
        if candidate_count is None:
            candidate_count = len(candidates)
        elif len(candidates) != candidate_count:
            raise RuntimeError("candidate count changed between benchmark repetitions")

    elapsed = median(durations)
    rate = candidate_count / elapsed if elapsed else float("inf")
    return candidate_count, elapsed, rate


def main() -> int:
    """Run all synthetic mutation-generation benchmark cases."""
    print("Distort mutation-generation benchmark")
    print("Synthetic inputs only; no password cracking is performed.")
    print(f"Python: {platform.python_version()} ({sys.implementation.name})")
    print(
        "Operating system: "
        f"{platform.system()} {platform.release()} ({platform.machine()})"
    )
    print(f"Measurement: median of {REPEATS} runs per case")
    print("Timings vary by hardware, operating system, Python version, and workload.")
    print()
    print(
        f"{'words':>8} {'level':>7} {'unique candidates':>18} "
        f"{'median seconds':>16} {'candidates/s':>14}"
    )

    for input_count, level in CASES:
        count, elapsed, rate = benchmark_case(input_count, level)
        print(
            f"{input_count:8d} {level:7d} {count:18d} "
            f"{elapsed:16.6f} {rate:14.0f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
