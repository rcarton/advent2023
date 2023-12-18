import io

from advent.days.day16 import first, second
from advent.utils import get_data_for_day

data = """.|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|...."""


def test_first():
    assert first(io.StringIO(data)) == 46


def test_first_data():
    assert first(get_data_for_day(16)) == 8551


def test_second():
    assert second(io.StringIO(data)) == 51
