import io

import pytest

from advent.days.day10 import first, second
from advent.utils import get_data_for_day

data = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""

data_2 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""

data_2_easy = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""

data_2_sneaky = """..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
.........."""


"""
........
.┏━━━━┓.
.┃┏━━┓┃.
.┃┃.┏┛┃.
.┃┗┓┗S┛.
.┗┓┗┓...
..┗━┛...
"""
data_2_loopy = """........
.F----7.
.|F--7|.
.||.FJ|.
.|L7LSJ.
.L7L7...
..L-J..."""


def test_first():
    assert first(io.StringIO(data)) == 8


def test_second():
    print()
    assert second(io.StringIO(data_2)) == 10


def test_second_easy():
    print()
    assert second(io.StringIO(data_2_easy)) == 4


def test_second_sneaky():
    print()
    assert second(io.StringIO(data_2_sneaky)) == 4


def test_second_loopy():
    print()
    assert second(io.StringIO(data_2_loopy)) == 0


def test_second_data():
    print()
    assert second(get_data_for_day(10)) == -1


# @pytest.mark.parametrize("dir1, dir2, expected", [
#     ("top", "bottom", "|"),
#     ("top", "left", "J"),
#     ("left", "top", "J"),
#     ("top", "bottom", "|"),
# ])
