from pathlib import Path

DAY_PY = """from typing import TextIO

def first(input: TextIO) -> int:
    return -1


def second(input: TextIO) -> int:
    return -1

"""

TEST_DAY_PY = """import io

from advent.days.day{num:02} import first, second

data = \"\"\"\"\"\"


def test_first():
    assert first(io.StringIO(data)) == 0


def test_second():
    assert second(io.StringIO(data)) == 0

"""


def new_day(num: int) -> None:
    # write only if the file does not exist
    day_file = f"advent/days/day{num:02}.py"
    if not Path(day_file).is_file():
        with open(day_file, "w") as f:
            f.write(DAY_PY)
    test_file = f"tests/test_day{num:02}.py"
    if not Path(test_file).is_file():
        with open(test_file, "w") as f:
            f.write(TEST_DAY_PY.format(num=num))
    data_file = f"data/day{num:02}.txt"
    if not Path(data_file).is_file():
        with open(data_file, "w") as f:
            f.write("\n")
