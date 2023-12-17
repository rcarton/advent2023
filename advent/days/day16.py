from collections import defaultdict
from typing import Callable, Optional, TextIO, DefaultDict

from advent.matrix import Coord, Matrix

MIRRORS_AND_SPLITTERS = {"-", "|", "/", "\\"}


class Contraption(Matrix[str]):
    row_mirrors: DefaultDict[int, list[str]] = defaultdict(list)
    col_mirrors: DefaultDict[int, list[str]] = defaultdict(list)

    @classmethod
    def from_string(
        cls, data: str, fn: Optional[Callable[[str], str]] = None
    ) -> "Contraption":
        inst = super().from_string(data, fn)

        for row, col in inst.all_coords():
            val = inst[row, col]
            if val in MIRRORS_AND_SPLITTERS:
                inst.row_mirrors[row].append(val)
                inst.col_mirrors[col].append(val)

        return inst


def first(input: TextIO) -> int:
    contraption = Contraption.from_string(input.read().strip())
    return -1


def second(input: TextIO) -> int:
    return -1
