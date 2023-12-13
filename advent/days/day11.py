import itertools as it
from typing import TextIO

from advent.matrix import Coord, Matrix
from advent.utils import manhattan_distance

Space = Matrix[str]


def parse_space(space: Space) -> tuple[list[int], list[int], list[Coord]]:
    """Empty rows, empty columns"""
    rows = set(range(space.height))
    columns = set(range(space.width))
    galaxies = []
    for row, column in space.all_coords():
        if space[row, column] == "#":
            if row in rows:
                rows.remove(row)
            if column in columns:
                columns.remove(column)
            galaxies.append((row, column))

    return (
        list(sorted(rows)),
        list(sorted(columns)),
        galaxies,
    )


def get_extra_distance(start: int, end: int, empties: list[int]) -> int:
    start, end = sorted((start, end))
    extra_distance = 0
    # Every empty row we cross must count double, they should also be sorted
    for i in empties:
        if i < start:
            continue
        if i > end:
            break
        # Else the row is in between the rows
        extra_distance += 1
    return extra_distance


def get_distance(
    c1: Coord,
    c2: Coord,
    empty_rows: list[int],
    empty_cols: list[int],
    expansion: int = 2,
) -> int:
    d = manhattan_distance(c1, c2)

    d += (expansion - 1) * get_extra_distance(c1[0], c2[0], empty_rows)
    d += (expansion - 1) * get_extra_distance(c1[1], c2[1], empty_cols)

    return d


def first(input: TextIO) -> int:
    space = Space.from_string(input.read().strip())
    empty_rows, empty_cols, galaxies = parse_space(space)

    return sum(
        get_distance(c1, c2, empty_rows, empty_cols)
        for c1, c2 in it.combinations(galaxies, 2)
    )


def second(input: TextIO, expansion: int = 1000000) -> int:
    space = Space.from_string(input.read().strip())
    empty_rows, empty_cols, galaxies = parse_space(space)

    return sum(
        get_distance(c1, c2, empty_rows, empty_cols, expansion)
        for c1, c2 in it.combinations(galaxies, 2)
    )
