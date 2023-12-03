from typing import TextIO, Tuple

import re
from advent.matrix import Coord, Matrix
from advent.utils import prod


class Engine(Matrix[str]):
    pass


SYMBOLS = {"#", "$", "%", "&", "*", "+", "-", "/", "=", "@"}
Part = Tuple[int, Coord]


def is_symbol(c: str):
    return c in SYMBOLS


def is_gear(c: str):
    return c == "*"


def is_digit(c: str):
    return re.match(r"^\d$", c)


def expand_part(engine: Engine, coord: Coord) -> Part:
    row, col = coord
    snum = engine[coord]
    curr = (row, col - 1)
    min_col = col
    while engine.is_valid_coord(curr) and is_digit(engine[curr]):
        snum = engine[curr] + snum
        min_col = curr[1]
        curr = (row, curr[1] - 1)
    curr = (row, col + 1)
    while engine.is_valid_coord(curr) and is_digit(engine[curr]):
        snum = snum + engine[curr]
        curr = (row, curr[1] + 1)

    return int(snum), (row, min_col)


def find_adjacent_parts(engine: Engine, coord: Coord) -> set[Part]:
    parts = set()
    for nc in engine.nbc8(coord):
        if is_digit(engine[nc]):
            parts.add(expand_part(engine, nc))

    return parts


def first(input: TextIO) -> int:
    engine = Matrix.from_string(input.read())
    parts: set[Part] = set()

    for coord in engine.all_coords():
        c = engine[coord]
        if not is_symbol(c):
            continue

        parts |= find_adjacent_parts(engine, coord)

    return sum(n for n, _ in parts)


def second(input: TextIO) -> int:
    engine = Matrix.from_string(input.read())
    total = 0

    for coord in engine.all_coords():
        c = engine[coord]
        if not is_gear(c):
            continue

        parts = find_adjacent_parts(engine, coord)
        if len(parts) != 2:
            continue

        total += prod(n for n, _ in parts)

    return total
