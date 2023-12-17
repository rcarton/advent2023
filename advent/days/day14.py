from typing import Iterator, Optional, Sequence, TextIO

from advent.matrix import Coord, Matrix


class Reflector(Matrix[str]):
    def get_col_c(self, col: int) -> Iterator[Coord]:
        for row in range(self.height):
            yield (row, col)

    def get_row_c(self, row: int) -> Iterator[Coord]:
        for col in range(self.width):
            yield (row, col)

    def tilt_north(self):
        for col in range(self.width):
            self.tilt_sequence_left(list(self.get_col_c(col)))

    def spin_cycle(self, count=1):
        north = [list(self.get_col_c(col)) for col in range(self.width)]
        west = [list(self.get_row_c(row)) for row in range(self.height)]
        south = [list(reversed(cc)) for cc in north]
        east = [list(reversed(rr)) for rr in west]

        # Find the cycle length and offset, for instance if cycle starts at 151, and length 193-151
        cycle_length = 193 - 151
        cycle_offset = 151

        mem = []

        for i in range(cycle_offset + cycle_length):
            if cycle_offset <= i < cycle_offset + cycle_length:
                mem.append(self.data[:])
            # if i % (count // 100) == 0:
            #     print(f"{i // (count // 100)}%")
            print(f"i={i} load={self.load()}")
            for direction in [north, west, south, east]:
                for seq_coords in direction:
                    self.tilt_sequence_left(seq_coords)

        # TODO check that the math works
        if count >= cycle_offset + cycle_length:
            self.data = mem[(count - cycle_offset) % cycle_length]

    def tilt_sequence_left(self, coords: Sequence[Coord]) -> None:
        swappable: Optional[int] = None
        for i, c in enumerate(coords):
            val = self[c]
            if val == "#":
                swappable = None
            elif val == ".":
                if swappable is None:
                    swappable = i
                # Otherwise we keep the old one
            elif val == "O":
                if swappable is not None:
                    # We should be swapping with a .
                    assert self[coords[swappable]] == "."
                    self[coords[swappable]] = val
                    self[c] = "."
                    swappable += 1
            else:
                raise Exception(f"Unknown val={val}")

    def load(self) -> int:
        total = 0
        for c in self.all_coords():
            if self[c] == "O":
                total += self.height - c[0]
        return total


def first(input: TextIO) -> int:
    reflector = Reflector.from_string(input.read().strip())
    reflector.tilt_north()

    return reflector.load()


def second(input: TextIO, count: int = 1000000000) -> int:
    reflector = Reflector.from_string(input.read().strip())
    reflector.spin_cycle(count)

    return reflector.load()
