"""Deterministic password-mutation generation for Distort."""

from collections.abc import Iterable, Mapping

MIN_LEVEL = 0
MAX_LEVEL = 9
DEFAULT_LEVEL = 5

# The order and contents mirror the original script. Under the historical
# level slicing rule, entries 5-8 are unreachable for valid levels 0-9.
# They remain here to make that compatibility detail explicit rather than
# silently deleting legacy transformation data.
LEET_PATTERNS: tuple[Mapping[str, str], ...] = (
    {},
    {"e": "3", "a": "4", "o": "0", "i": "1", "l": "1", "s": "$"},
    {"e": "3", "a": "@", "o": "0", "i": "1", "l": "1", "s": "$"},
    {"e": "3", "a": "4", "o": "0", "i": "!", "l": "1", "s": "$"},
    {"e": "3", "a": "@", "o": "0", "i": "!", "l": "1", "s": "$"},
    {"e": "3", "a": "4", "o": "0", "i": "1", "l": "1", "s": "5"},
    {"e": "3", "a": "@", "o": "0", "i": "1", "l": "1", "s": "5"},
    {"e": "3", "a": "4", "o": "0", "i": "!", "l": "1", "s": "5"},
    {"e": "3", "a": "@", "o": "0", "i": "!", "l": "1", "s": "5"},
)

_SUFFIXES_LEVEL_5 = ("1", "123", "!", ".", "2")
_SUFFIXES_LEVEL_7 = ("?", "_", "69", "23", "25", "8", "10", "13", "3", "4", "6", "7")
_SUFFIXES_LEVEL_8 = ("07", "09", "14", "15", "17", "18", "19", "77", "88", "99", "12345")
_SUFFIXES_LEVEL_9 = ("00", "02", "06", "19", "20", "25", "007", "111", "777", "666", "2024")


def validate_level(level: int) -> None:
    """Raise ``ValueError`` when *level* is outside Distort's supported range."""
    if not MIN_LEVEL <= level <= MAX_LEVEL:
        raise ValueError(f"mutation level must be between {MIN_LEVEL} and {MAX_LEVEL}")


def normalize_word(word: str) -> str:
    """Normalize input using the original strip-and-lowercase behavior."""
    return word.strip().lower()


def capitalize_variants(word: str) -> set[str]:
    """Return the original capitalization variants for *word*."""
    return {word, word.upper(), word.capitalize(), word.lower()}


def _apply_leet_pattern(word: str, pattern: Mapping[str, str]) -> str:
    return "".join(pattern.get(char, char) for char in word)


def leet_variants(word: str, level: int) -> set[str]:
    """Return legacy-compatible leetspeak transformations for *word* and *level*."""
    validate_level(level)
    if level <= 4:
        return set()
    return {
        _apply_leet_pattern(word, pattern)
        for pattern in LEET_PATTERNS[: level - 4]
    }


def _base_variants(word: str, level: int) -> set[str]:
    variants: set[str] = set()
    for capitalized in capitalize_variants(word):
        variants.add(capitalized)
        variants.update(leet_variants(capitalized, level))
    return variants


def suffixes_for_level(level: int) -> tuple[str, ...]:
    """Return suffixes enabled by *level* using the original threshold rules."""
    validate_level(level)
    suffixes: list[str] = []
    if level > 4:
        suffixes.extend(_SUFFIXES_LEVEL_5)
    if level > 6:
        suffixes.extend(_SUFFIXES_LEVEL_7)
    if level > 7:
        suffixes.extend(_SUFFIXES_LEVEL_8)
    if level > 8:
        suffixes.extend(_SUFFIXES_LEVEL_9)
    return tuple(suffixes)


def generate_variants(word: str, level: int = DEFAULT_LEVEL) -> set[str]:
    """Generate unique mutation candidates for one normalized seed word."""
    validate_level(level)
    normalized = normalize_word(word)
    if not normalized:
        return set()

    distorted = _base_variants(normalized, level)
    for suffix in suffixes_for_level(level):
        for capitalized in capitalize_variants(normalized):
            distorted.update(_base_variants(capitalized + suffix, level))
    return distorted


def generate_wordlist(words: Iterable[str], level: int = DEFAULT_LEVEL) -> list[str]:
    """Generate a duplicate-free, lexicographically sorted candidate wordlist.

    Blank or whitespace-only inputs are ignored. Sorting makes user-visible output
    reproducible across runs and Python hash-randomization seeds.
    """
    validate_level(level)
    candidates: set[str] = set()
    for word in words:
        normalized = normalize_word(word)
        if normalized:
            candidates.update(generate_variants(normalized, level))
    return sorted(candidates)
