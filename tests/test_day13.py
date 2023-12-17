import io

import pytest

from advent.days.day13 import find_reflection_in_list, first, second

data = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""


@pytest.mark.parametrize(
    "l, expected",
    [
        ("abba", 1),
        ("abccba", 2),
        ("abcd", None),
        ("cabba", 2),
        ("cabbacd", 2),
        ("aabcdef", 0),
        ("cdefaa", 4),
        ([83, 85, 12, 78, 38, 62, 62, 38, 78, 12, 85, 91, 91], 11),
    ],
)
def test_find_reflection_in_list(l, expected):
    assert find_reflection_in_list(l) == expected


def test_first():
    assert first(io.StringIO(data)) == 405


def test_second():
    assert second(io.StringIO(data)) == 400
