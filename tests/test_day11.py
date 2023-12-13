import io
import pytest
from advent.days.day11 import Space, first, get_distance, parse_space, second

data = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""


@pytest.mark.parametrize(
    "c1, c2, expected",
    [
        ((0, 3), (8, 7), 15),
    ],
)
def test_get_distance(c1, c2, expected):
    space = Space.from_string(io.StringIO(data).read().strip())
    empty_rows, empty_cols, galaxies = parse_space(space)
    assert get_distance(c1, c2, empty_rows, empty_cols) == expected


def test_first():
    assert first(io.StringIO(data)) == 374


def test_second():
    assert second(io.StringIO(data), 10) == 1030
