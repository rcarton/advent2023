import io

from advent.days.day03 import first, second

data = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""


def test_first():
    data_io = io.StringIO(data)
    assert first(data_io) == 4361


def test_second():
    data_io = io.StringIO(data)
    assert second(data_io) == 467835
