import io

import pytest

from advent.days.day07 import (
    Hand,
    HandType,
    first,
    get_comparable_hand,
    get_hand_type,
    second,
)

data = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""


@pytest.mark.parametrize(
    "cards, expected, part2",
    [
        ("AAAAA", HandType.FIVE_OAK, False),
        ("AA8AA", HandType.FOUR_OAK, False),
        ("23332", HandType.FULL, False),
        ("9T8TT", HandType.THREE_OAK, False),
        ("23432", HandType.TWO_PAIRS, False),
        ("A23A4", HandType.PAIR, False),
        ("23456", HandType.HIGH_CARD, False),
        # part 2
        ("32T3K", HandType.PAIR, True),
        ("KK677", HandType.TWO_PAIRS, True),
        ("T55J5", HandType.FOUR_OAK, True),
        ("KTJJT", HandType.FOUR_OAK, True),
        ("QQQJA", HandType.FOUR_OAK, True),
        ("A23A4", HandType.PAIR, True),
        ("23456", HandType.HIGH_CARD, True),
    ],
)
def test_get_hand_type(cards: str, expected: HandType, part2: bool):
    assert get_hand_type(Hand(list(cards), 0)) == expected


@pytest.mark.parametrize(
    "cards, expected",
    [
        ("AAAAA", "A"),
        ("AA8AA", "A8"),
        ("23332", "32"),
        ("9T8TT", "T98"),
        ("23432", "324"),
        ("A23A4", "A432"),
        ("23456", "65432"),
    ],
)
def test_get_comparable_hand(cards: str, expected: str):
    assert get_comparable_hand(list(cards)) == list(expected)


@pytest.mark.parametrize(
    "c1, c2, expected, part2",
    [
        ("33332", "2AAAA", False, False),
        ("77888", "77788", False, False),
        ("23332", "2AAAA", True, False),
        ("23456", "23457", True, False),
        ("22222", "9T8TT", False, False),
        ("25452", "35K53", True, False),
        ("25452", "25652", True, False),
        # part 2
        ("32T3K", "T55J5", True, True),
        ("T55J5", "KK677", False, True),
        ("T55J5", "32T3K", False, True),
        ("T55J5", "KTJJT", True, True),
        ("JKKK2", "QQQQ2", True, True),
        ("24344", "24J4A", False, True),
    ],
)
def test_hand_lt(c1: str, c2: str, expected: bool, part2: bool):
    assert (Hand(list(c1), 0, part2) < Hand(list(c2), 0, part2)) == expected


def test_first():
    data_io = io.StringIO(data)
    assert first(data_io) == 6440


def test_second():
    data_io = io.StringIO(data)
    print("")
    assert second(data_io) == 5905
