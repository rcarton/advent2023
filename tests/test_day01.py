import io

from advent.days.day01 import first, second

data = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""


data_2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

def test_first():
    data_io = io.StringIO(data)
    assert first(data_io) == 142


def test_second():
    assert second(io.StringIO(data_2)) == 281
