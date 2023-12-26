import itertools as it
from typing import Callable, Generic, Iterator, List, Literal, Optional, Tuple, TypeVar

from advent.utils import tadd

T = TypeVar("T")


# row, col
Coord = Tuple[int, int]
Delta = Tuple[int, int]


Direction = Literal["up", "down", "left", "right"]


def get_coords_between_vertices(self, start: Coord, end: Coord) -> list[Coord]:
    r1, c1 = start
    r2, c2 = end
    assert r1 == r2 or c1 == c2

    if r1 == r2:
        delta = (0, 1) if c1 < c2 else (0, -1)
    else:
        delta = (1, 0) if r1 < r2 else (-1, 0)

    curr = start
    points: list[Coord] = []
    while True:
        curr = tadd(curr, delta)
        if curr == end:
            break
        points.append(curr)
    return points


def get_delta_dir(d: Direction) -> Delta:
    return {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1),
    }[d]


def manhattan_distance(c1: Coord, c2: Coord) -> int:
    return abs(c2[0] - c1[0]) + abs(c2[1] - c1[1])


def is_clockwise(vertices: list[Coord]) -> bool:
    # https://en.wikipedia.org/wiki/Curve_orientation#Orientation_of_a_simple_polygon
    assert len(vertices) > 0

    # Because we're using row, col instead of x, y, we have to convert
    def to_xy(c: Coord) -> Coord:
        return c[1], -c[0]

    vertices = [to_xy(c) for c in vertices]

    # Find the vertex with the lowest x
    min_i = None
    for i, (x, y) in enumerate(vertices):
        if min_i is None or (x <= vertices[i][0] and y < vertices[i][1]):
            min_i = i

    # Compute the determinant of the orientation matrix, just look at the wikipedia explanations
    xa, ya = vertices[min_i - 1]
    xb, yb = vertices[min_i]
    xc, yc = vertices[min_i + 1]

    det = (xb * yc + xa * yb + ya * xc) - (ya * xb + yb * xc + xa * yc)

    if det == 0:
        raise Exception("I don't know, it's a line or something")

    # Negative determinant => clockwise polygon
    return det < 0


class Matrix(Generic[T]):
    data: List[T]
    width: int
    height: int

    def __init__(self, data: List[T], width: int, height: int):
        self.data = list(data)
        assert len(self.data) == width * height
        self.width = width
        self.height = height

    def is_valid_coord(self, coord: Coord):
        return 0 <= coord[0] < self.height and 0 <= coord[1] < self.width

    def __get_index(self, coord: Coord):
        row, col = coord
        if not self.is_valid_coord(coord):
            raise IndexError(f"Coord out of range {coord}")
        return row * self.width + col

    def __getitem__(self, coord: Coord) -> T:
        return self.data[self.__get_index(coord)]

    def __setitem__(self, coord: Coord, value: T) -> None:
        self.data[self.__get_index(coord)] = value

    @classmethod
    def from_string(
        cls, data: str, fn: Optional[Callable[[str], T]] = None
    ) -> "Matrix[T]":
        rows = data.splitlines()
        height = len(rows)
        width = len(rows[0])
        data_as_array = [fn(v) if fn else v for v in it.chain(*rows)]
        return cls(data_as_array, width, height)

    def all_coords(self) -> Iterator[Coord]:
        for x in range(self.height):
            for y in range(self.width):
                yield x, y

    def neighbor_coords(
        self, coord: Coord, include_diagonals: bool = False
    ) -> List[Coord]:
        row, col = coord
        coords = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        if include_diagonals:
            coords += [
                (row - 1, col - 1),
                (row - 1, col + 1),
                (row + 1, col - 1),
                (row + 1, col + 1),
            ]

        return [c for c in coords if self.is_valid_coord(c)]

    def neighbors(self, coord: Coord, include_diagonals: bool = False) -> List[T]:
        return [
            self[c]
            for c in self.neighbor_coords(coord, include_diagonals)
            if self.is_valid_coord(c)
        ]

    def nbc4(self, coord: Coord) -> List[Coord]:
        return self.neighbor_coords(coord)

    def nb8(self, coord: Coord) -> List[T]:
        return self.neighbors(coord, include_diagonals=True)

    def nbc8(self, coord: Coord) -> List[Coord]:
        return self.neighbor_coords(coord, include_diagonals=True)

    def get_row(self, row: int) -> List[T]:
        row_start = row * self.width
        return self.data[row_start : row_start + self.width]

    def get_col(self, col: int) -> List[T]:
        return self.data[col :: self.width]

    def get_row_coords(self, row: int) -> List[T]:
        return []

    def items(self) -> Iterator[tuple[Coord, T]]:
        for c in self.all_coords():
            yield c, self[c]

    def __str__(self):
        out = ""
        for row in range(self.height):
            for col in range(self.width):
                out += str(self[row, col])
            out += "\n"
        return out[:-1]
