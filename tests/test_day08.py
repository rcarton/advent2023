import io

from advent.days.day08 import first, second
from advent.utils import get_data_for_day

data = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""


def test_first():
    assert first(io.StringIO(data)) == 6


data_2 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""


def test_second():
    assert second(io.StringIO(data_2)) == 6


def test_second_real():
    assert second(get_data_for_day(8)) == 6
