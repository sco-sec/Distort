import pytest

from distort.mutations import (
    capitalize_variants,
    generate_variants,
    generate_wordlist,
    leet_variants,
    normalize_word,
    suffixes_for_level,
)


def test_normalize_word_strips_and_lowercases() -> None:
    assert normalize_word("  ExAmPle\t") == "example"


def test_capitalize_variants() -> None:
    assert capitalize_variants("example") == {"example", "Example", "EXAMPLE"}


def test_base_generation_level_zero() -> None:
    assert generate_variants("example", 0) == {"example", "Example", "EXAMPLE"}


def test_lowercase_and_uppercase_input_normalize_to_same_candidates() -> None:
    assert generate_variants("ExAmPlE", 6) == generate_variants("example", 6)


def test_first_effective_leet_substitution_arrives_at_level_six() -> None:
    assert leet_variants("sea", 5) == {"sea"}
    assert "$34" in leet_variants("sea", 6)


def test_legacy_unreachable_s_to_five_patterns_remain_inactive_at_level_nine() -> None:
    variants = leet_variants("s", 9)
    assert "$" in variants
    assert "5" not in variants


def test_suffix_rules_at_level_boundaries() -> None:
    assert suffixes_for_level(4) == ()
    assert suffixes_for_level(5) == ("1", "123", "!", ".", "2")
    assert "?" not in suffixes_for_level(6)
    assert "?" in suffixes_for_level(7)
    assert "07" not in suffixes_for_level(7)
    assert "07" in suffixes_for_level(8)
    assert "00" not in suffixes_for_level(8)
    assert "00" in suffixes_for_level(9)


@pytest.mark.parametrize(
    ("level", "expected_count"),
    [
        (0, 3),
        (4, 3),
        (5, 18),
        (6, 30),
        (7, 126),
        (8, 203),
        (9, 266),
    ],
)
def test_legacy_example_counts_across_important_boundaries(
    level: int, expected_count: int
) -> None:
    assert len(generate_wordlist(["example"], level)) == expected_count


def test_duplicate_input_words_do_not_duplicate_candidates() -> None:
    once = generate_wordlist(["example"], 7)
    repeated = generate_wordlist(["example", "EXAMPLE", " example "], 7)
    assert repeated == once


def test_output_is_sorted_and_deterministic() -> None:
    first = generate_wordlist(["security", "testing"], 8)
    second = generate_wordlist(["security", "testing"], 8)
    assert first == second
    assert first == sorted(first)


def test_blank_and_whitespace_only_words_are_ignored() -> None:
    assert generate_wordlist(["", "  ", "\t", "example"], 5) == generate_wordlist(
        ["example"], 5
    )


@pytest.mark.parametrize("level", [-1, 10])
def test_invalid_level_raises(level: int) -> None:
    with pytest.raises(ValueError, match="between 0 and 9"):
        generate_wordlist(["example"], level)


def test_generate_variants_returns_empty_for_blank_seed() -> None:
    assert generate_variants("  ", 5) == set()
