import heapq
from typing import Literal, Optional, TextIO

from advent.matrix import Coord, Matrix
from advent.utils import tadd

Direction = Literal["up", "down", "left", "right"]


def backwards(d1: Optional[Direction], d2: Optional[Direction]) -> bool:
    if d1 is None or d2 is None:
        return False

    d = (d1, d2) if d1 < d2 else (d2, d1)
    return d in [("left", "right"), ("down", "up")]


class CityMap(Matrix[int]):
    def nb(
        self, coord: Coord, direction: Optional[Direction], is_ultra: bool = False
    ) -> list[tuple[Coord, Direction, int]]:
        if is_ultra:
            return self.nb_ultra(coord, direction)

        row, col = coord
        neighbors: list[tuple[Coord, Direction]] = [
            ((row, col - 1), "left"),
            ((row - 1, col), "up"),
            ((row, col + 1), "right"),
            ((row + 1, col), "down"),
        ]
        return [
            (c, n_direction, 1)
            for c, n_direction in neighbors
            if self.is_valid_coord(c) and not backwards(direction, n_direction)
        ]

    def nb_ultra(
        self, coord: Coord, direction: Optional[Direction]
    ) -> list[tuple[Coord, Direction, int]]:
        row, col = coord
        deltas: list[tuple[Coord, Direction]] = [
            ((0, -1), "left"),
            ((-1, 0), "up"),
            ((0, 1), "right"),
            ((1, 0), "down"),
        ]

        nn = []
        for i in range(4, 10 + 1):
            for delta, delta_dir in deltas:
                if backwards(direction, delta_dir):
                    continue
                c = row + delta[0] * i, col + delta[1] * i
                if not self.is_valid_coord(c):
                    continue
                nn.append((c, delta_dir, i))
        return nn

    def compute_heatloss(self, start: Coord, end: Coord) -> int:
        """Do not include the start, but include the end."""
        r1, c1 = start
        r2, c2 = end

        total_heatloss = 0

        if r1 == r2:
            delta = (0, 1) if c1 < c2 else (0, -1)
        else:
            delta = (1, 0) if r1 < r2 else (-1, 0)

        curr = start
        while True:
            curr = tadd(curr, delta)
            total_heatloss += self[curr]
            if curr == end:
                return total_heatloss


# movements done, direction
LineCheck = tuple[int, Optional[Direction]]
# Items are ordered by heat loss
Item = tuple[int, Coord, LineCheck]


def min_heat_loss(cm: CityMap, is_ultra: bool = False) -> int:
    destination = (cm.height - 1, cm.width - 1)

    max_distance = 10 if is_ultra else 3

    # Djikstra
    coord = (0, 0)
    # Doesn't matter initially
    line_check: LineCheck = (0, None)
    heap: list[Item] = []
    item = (0, coord, line_check)
    heapq.heappush(heap, item)

    # Prevent visiting the same again, technically we only need to prevent visiting
    # the same coord with a >= line check for that direction
    # TODO optimize instead of dummy set
    seen = set()

    count = 0
    while heap:
        count += 1
        # if count > 10_000:
        #     raise Exception("Bork")

        item = heapq.heappop(heap)

        if item[1:] in seen:
            continue
        seen.add(item[1:])

        heat_loss, coord, line_check = item
        # print(f"heat_loss={heat_loss}, coord={coord}, line_check={line_check}")
        if coord == destination:
            return heat_loss

        for n_coord, direction, distance in cm.nb(coord, line_check[1], is_ultra):
            new_line_check = (
                (distance, direction)
                if direction != line_check[1]
                else (line_check[0] + distance, direction)
            )

            # Do the line check, if we've already moved 3/10 blocks in one direction, this is not a valid neighbor
            if new_line_check[0] > max_distance:
                continue

            # Add the neighbor to the heap
            next_item = (
                heat_loss + cm.compute_heatloss(coord, n_coord),
                n_coord,
                new_line_check,
            )

            if next_item[1:] not in seen:
                heapq.heappush(heap, next_item)

    raise Exception("Destination not found")


def first(input: TextIO) -> int:
    city_map: CityMap = CityMap.from_string(input.read().strip(), lambda v: int(v))

    return min_heat_loss(city_map)


def second(input: TextIO) -> int:
    city_map: CityMap = CityMap.from_string(input.read().strip(), lambda v: int(v))

    return min_heat_loss(city_map, is_ultra=True)
