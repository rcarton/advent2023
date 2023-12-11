import io

from advent.days.day06 import first, second

data = """Time:      7  15   30
Distance:  9  40  200"""


def test_first():
    data_io = io.StringIO(data)
    assert first(data_io) == 288


def test_second():
    data_io = io.StringIO(data)
    assert second(data_io) == 71503
