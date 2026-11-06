"""Golden candidate-set checks against the earliest verified Distort archive."""

from pathlib import Path

import pytest

from distort.mutations import generate_wordlist

FIXTURE_DIR = Path(__file__).parent / "fixtures"
SEED_WORDS = ("example", "security", "testing")
LEGACY_LEVELS = (0, 1, 4, 5, 6, 7, 8, 9)


@pytest.mark.parametrize("level", LEGACY_LEVELS)
def test_candidate_set_matches_legacy_fixture(level: int) -> None:
    fixture = FIXTURE_DIR / f"legacy_level_{level}.txt"
    expected = set(fixture.read_text(encoding="utf-8").splitlines())

    actual = generate_wordlist(SEED_WORDS, level)
    repeated = generate_wordlist(SEED_WORDS, level)
    duplicate_inputs = generate_wordlist((*SEED_WORDS, *SEED_WORDS), level)

    missing = expected - set(actual)
    unexpected = set(actual) - expected
    assert not missing, f"level {level}: missing legacy candidates: {sorted(missing)}"
    assert not unexpected, (
        f"level {level}: unexpected additional candidates: {sorted(unexpected)}"
    )
    assert len(actual) == len(set(actual)), f"level {level}: duplicate candidates"
    assert actual == sorted(actual), f"level {level}: output is not sorted"
    assert repeated == actual, f"level {level}: repeated execution changed output"
    assert duplicate_inputs == actual, (
        f"level {level}: duplicate seed words changed the candidate set"
    )
