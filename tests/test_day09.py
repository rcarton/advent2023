import io

from advent.days.day09 import first, second

data = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""


def test_first():
    assert first(io.StringIO(data)) == 114


def test_second():
    assert second(io.StringIO(data)) == 2
