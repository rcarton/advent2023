import io

import pytest

from advent.days.day12 import (
    Candidate,
    first,
    get_candidates,
    parse_line,
    second,
    solve,
)

data = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""


@pytest.mark.parametrize(
    "c, expected",
    [
        (("....#.#", [1, 1], ""), [("", [], "....#.#")]),
        ((".?..#.#", [1, 1], ""), [("...#.#", [1, 1], "."), ("#..#.#", [1, 1], ".")]),
        ((".#..#.#", [1, 1], ""), []),
        (
            (".##.#.#", [2, 1, 1], ""),
            [
                ("", [], ".##.#.#"),
            ],
        ),
    ],
)
def test_get_candidates(c: Candidate, expected):
    assert get_candidates(c) == expected


@pytest.mark.parametrize(
    "line, expected",
    [
        # ("???.### 1,1,3", 1),
        # (".??..??...?##. 1,1,3", 4),
        # ("?#?#?#?#?#?#?#? 1,3,1,6", 1),
        ("????.#...#... 4,1,1", 1),
        # ("????.######..#####. 1,6,5", 4),
        # ("?###???????? 3,2,1", 10),
    ],
)
def test_solve(line, expected):
    assert len(solve(*parse_line(line))) == expected


def test_solve_debug():
    assert len(solve(*parse_line("????.######..#####. 1,6,5"))) == 4


def test_first():
    assert first(io.StringIO(data)) == 21


def test_second():
    assert second(io.StringIO(data)) == 525152


"""

....#.#  1, 1 ->  ('', (), '....#.#')
....?.#  1, 1 ->  ('.#', (1, 1), .....') ('#', (1,), ....#.')


"""
