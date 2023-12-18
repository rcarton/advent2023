import io

from advent.days.day17 import first, second

data = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""


def test_first():
    assert first(io.StringIO(data)) == 102


def test_first_simple():
    simple = """311111
259251
749221
"""
    print()
    assert first(io.StringIO(simple)) == 10


def test_second():
    assert second(io.StringIO(data)) == 94
