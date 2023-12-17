import io

from advent.days.day14 import Reflector, first, second
from advent.utils import get_data_for_day

data = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""


tilted_north = """OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#...."""

one_spin = """.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#...."""


def test_tilt_north():
    r = Reflector.from_string(data)
    r.tilt_north()
    assert str(r) == str(Reflector.from_string(tilted_north))


def test_spin_cycle():
    r = Reflector.from_string(data)
    r.spin_cycle(1)
    assert str(r) == str(Reflector.from_string(one_spin))


def test_first():
    assert first(io.StringIO(data)) == 136


def test_second():
    assert second(io.StringIO(data)) == 64


def test_second_data():
    for i in [1000000000]:
        print(second(get_data_for_day(14), i))
