from collections import defaultdict, deque
from typing import Callable, Iterable, Literal, Optional, TextIO, DefaultDict

from advent.matrix import Coord, Matrix
from advent.utils import tadd

MIRRORS_AND_SPLITTERS = {"-", "|", "/", "\\"}


Direction = Literal["up", "down", "left", "right"]

Beam = tuple[Coord, Direction]


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

    def get_next_in_direction(
        self, coord: Coord, direction: Direction
    ) -> tuple[Coord, str]:
        deltas: dict[Direction, tuple[int, int]] = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1),
        }

        delta = deltas[direction]
        curr = coord
        while True:
            # curr = (curr[0] + delta[0], curr[1] + delta[1])
            curr = tadd(curr, delta)
            if not self.is_valid_coord(curr):
                break
            yield curr, self[curr]

    def process_mirror(self, coord: Coord, direction: Direction) -> list[Beam]:
        val = self[coord]

        if val == "\\":
            if direction == "left":
                return [(coord, "up")]
            if direction == "right":
                return [(coord, "down")]
            if direction == "up":
                return [(coord, "left")]
            if direction == "down":
                return [(coord, "right")]
        if val == "/":
            if direction == "left":
                return [(coord, "down")]
            if direction == "right":
                return [(coord, "up")]
            if direction == "up":
                return [(coord, "right")]
            if direction == "down":
                return [(coord, "left")]
        if val == "|":
            if direction == "up" or direction == "down":
                return [(coord, direction)]
            return [(coord, "down"), (coord, "up")]
        if val == "-":
            if direction == "left" or direction == "right":
                return [(coord, direction)]
            return [(coord, "left"), (coord, "right")]
        raise Exception(
            f"Error processing mirror at coord={coord}, val={val}, direction={direction}"
        )

    def beam(
        self, start_coord: Coord = (0, 0), start_direction: Direction = "right"
    ) -> int:
        start_beams: list[Beam] = (
            [(start_coord, start_direction)]
            if self[start_coord] not in MIRRORS_AND_SPLITTERS
            else self.process_mirror(start_coord, start_direction)
        )

        # Used to prevent loops, it keeps tracks of mirrors/splitters seen with a given direction
        seen: set[Beam] = (
            set()
            if self[start_coord] not in MIRRORS_AND_SPLITTERS
            else {(start_coord, start_direction)}
        )
        energized: set[Coord] = {start_coord}

        to_see = deque(start_beams)
        while to_see:
            curr = to_see.pop()
            if curr in seen:
                continue

            seen.add(curr)
            coord, direction = curr

            for coord, value in self.get_next_in_direction(*curr):
                energized.add(coord)
                if value in MIRRORS_AND_SPLITTERS:
                    to_see.extend(self.process_mirror(coord, direction))
                    break

        return len(energized)


def first(input: TextIO) -> int:
    contraption = Contraption.from_string(input.read().strip())
    return contraption.beam()


def second(input: TextIO) -> int:
    all_start_beams: list[Beam] = []
    contraption = Contraption.from_string(input.read().strip())
    for row in range(contraption.height):
        all_start_beams.append(((row, 0), "right"))
        all_start_beams.append(((row, contraption.width - 1), "left"))
    for col in range(contraption.width):
        all_start_beams.append(((0, col), "down"))
        all_start_beams.append(((contraption.height - 1, col), "up"))

    return max(
        contraption.beam(coord, direction) for coord, direction in all_start_beams
    )
