from functools import cache
from typing import Callable, List, Literal, Optional, TextIO
import itertools as it


from advent.matrix import Coord, Matrix, T

TOTAL_STEPS = 26501365


class Garden(Matrix[str]):
    start: Coord
    unlimited: bool = False
    __hash: int

    def __init__(self, data: List[T], width: int, height: int):
        super().__init__(data, width, height)
        self.__hash = hash("".join(data))

        for c, v in self.items():
            if v == "S":
                self[c] = "."
                self.start = c

    @classmethod
    def from_string(
        cls, data: str, fn: Optional[Callable[[str], T]] = None
    ) -> "Garden":
        rows = data.splitlines()
        height = len(rows)
        width = len(rows[0])
        data_as_array = [fn(v) if fn else v for v in it.chain(*rows)]
        return cls(data_as_array, width, height)

    def __getitem__(self, coord: Coord) -> str:
        return self.data[self.__get_index(coord)]

    def __get_index(self, coord: Coord):
        if not self.unlimited:
            row, col = coord
            if not self.is_valid_coord(coord):
                raise IndexError(f"Coord out of range {coord}")
            return row * self.width + col

        row, col = coord

        col = (self.width + col) % self.width if col < 0 else col % self.width

        # TODO
        row = (self.height + row) % self.height if row < 0 else row % self.height

        return row * self.width + col

    def is_valid_coord(self, coord: Coord) -> bool:
        if self.unlimited:
            return True
        return super().is_valid_coord(coord)

    def __hash__(self):
        return self.__hash


MEMO: dict[(int, Coord):int] = {}


def count_reachable(garden: Garden, steps: int, start: Optional[Coord] = None) -> int:
    assert steps >= 0

    if steps == 0:
        # Current tile is the only one
        return 1

    sc = garden.start if start is None else start

    # 261 is the safety number, but it needs to be odd/even, can't change evenness
    cache_key = (min(261 if steps % 2 == 1 else 262, steps), sc)
    # cache_key = (steps, sc)
    # global MEMO
    # if cache_key in MEMO:
    #     # print(f"steps={steps} entry={sc} MEMO={MEMO[cache_key]}")
    #     return MEMO[cache_key]

    if steps == 1:
        return len({nc for nc in garden.nbc4(sc) if garden[nc] == "."})

    reachable: list[set[Coord]] = [set() for _ in range(steps + 1)]
    reachable[0] = {sc}
    seen = {sc}

    for i in range(1, steps + 1):
        if len(reachable[i - 1]) == 0:
            break
        for c in reachable[i - 1]:
            new_c = {
                nc for nc in garden.nbc4(c) if garden[nc] == "." and nc not in seen
            }
            seen |= new_c
            reachable[i] |= new_c

    val = sum(len(tiles) for tiles in reachable[steps % 2 :: 2])
    # MEMO[cache_key] = val
    # print(f"steps={steps} entry={sc} count={val}")
    return val


Corner = Literal["NW", "NE", "SW", "SE"]
Midpoint = Literal["W", "N", "E", "S"]
Start = Literal["O"]
Entry = Corner | Midpoint | Start

ENTRIES: dict[Entry, Coord] = {
    "N": (0, 65),
    "S": (130, 65),
    "W": (65, 0),
    "E": (65, 130),
    "NW": (0, 0),
    "NE": (0, 130),
    "SW": (130, 0),
    "SE": (130, 130),
    "O": (65, 65),
}


def steps_left_in_garden(gx: int, gy: int, total_steps: int) -> tuple[int, int, Entry]:
    """Number of steps left when getting to the garden"""
    # We don't want to bother with the starting square
    if gx == 0 and gy == 0:
        return 0, total_steps, "O"

    # Figure out entry
    entry: Entry = ""
    if gy != 0:
        entry += "S" if gy > 0 else "N"
    if gx != 0:
        entry += "E" if gx < 0 else "W"

    on_axis = len(entry) == 1

    # Steps to get there:
    #  - on an axis, 66 + gx * 131
    #  - else 65+65+2 + gy * 131 + gx * 131
    gx = abs(gx)
    gy = abs(gy)
    if on_axis:
        # one of the 2 is zero anyway
        steps_there = (gx + gy) * 131 - 65
    else:
        steps_there = (gx + gy) * 131 - (65 + 65)

    steps_left = total_steps - steps_there
    return steps_there, steps_left, entry


"""
Info:
    steps: 26501365
    width: 131
    height: 131
    mid point: 65
    # visitable: 15075, but then it depends on starting + step count % 2
    from a corner, need 261 steps left to visit all
    from a center point, need 261-65 = 196
    

Calculation:
    for each axis, <number of complete gardens (same for each)> x 15075, + however can be visited in the last garden (maybe last 2 gardens)
    for each quadrant <number of complete gardens (same for each)> x 15075 + however can be visited on the gardens with < 261 steps left,
        ie. the ones on the edge of the circle. So pretty much integral of the quadrant and then some

"""


# 261 from a corner, 196 from a mid, doesn't matter where the entry is pretty much
# 15075 total, so if you enter a square from a corner with 261 steps left, you can visit all of them
# If you enter from a mid point (so only squares on the axis will be like that), you need 196 steps to visit all
# Function that tells you how many steps you'll have left would be nice

# The entry point doesn't matter if corner and > 261 steps left (all of them would be a corner except on axis)
# For axis, it's always the mid point

# So calculate how many reached: going NSWE only, then every full square * 15075 (total number visitable)


# 202300 gardens exactly can be reached if you go straight the whole time (or 202301 ?)


def garden_range(garden: Garden, total_steps: int) -> int:
    """Return the max range of visitable gardens if going straight."""
    assert garden.width == garden.height

    w = garden.width
    h = garden.width // 2
    # steps_there = n * w - h
    return (total_steps + h) // w


def total_visitable_old(garden: Garden, total_steps: int = TOTAL_STEPS) -> int:
    grange = garden_range(garden, total_steps)
    count = 0

    stopper = 0
    for gx in range(-grange, grange + 1):
        # Now we're going vertically by doing both +/- gy
        gy = 0
        stopper += 1
        while True:
            used, left, entry = steps_left_in_garden(gx, gy, total_steps)
            if used > total_steps:
                break

            print(f"gx={gx} gy={gy} entry={entry} left={left}")
            if stopper == 5:
                return -1

            # Add the counts for both +/- gy
            count += count_reachable(garden, left, ENTRIES[entry])

            if gy > 0:
                _, _, entry = steps_left_in_garden(gx, -gy, total_steps)
                count += count_reachable(garden, left, ENTRIES[entry])

            gy += 1
    return count


def total_visitable(garden: Garden, total_steps: int = TOTAL_STEPS) -> int:
    # This only works in certain conditions
    assert garden.width == 131
    assert (total_steps - garden.width // 2) % garden.width == 0

    quadrant_width = (total_steps - garden.width // 2) // garden.width
    odd = even = 0

    # This could be 2 sums of terms but I'm lazy
    for n in range(1, quadrant_width - 1):
        # This works only if total steps is even, otherwise flip
        if n % 2 == 1:
            even += n
        else:
            odd += n

    # Flip if the total number of steps is odd
    if total_steps % 2 == 1:
        odd, even = even, odd

    print(f"odd={odd} even={even}")

    count = 0

    # Quadrants
    quadrants: list[Corner] = ["NE", "NW", "SE", "SW"]
    for corner in quadrants:
        # Outer edge
        quadrant_total = quadrant_width * count_reachable(garden, 64, ENTRIES[corner])
        quadrant_total += (quadrant_width - 1) * count_reachable(
            garden, 195, ENTRIES[corner]
        )
        quadrant_total += even * count_reachable(garden, 326, ENTRIES[corner])
        quadrant_total += odd * count_reachable(garden, 457, ENTRIES[corner])
        count += quadrant_total

    # Axis
    mids: list[Midpoint] = ["W", "N", "E", "S"]

    odd = even = quadrant_width // 2
    if total_steps % 2 == 1:
        even -= 1
    assert odd + even + 1 == quadrant_width

    for entry in mids:
        axis_count = count_reachable(garden, 130, ENTRIES[entry])
        axis_count += odd * count_reachable(garden, 261, ENTRIES[entry])
        axis_count += even * count_reachable(garden, 392, ENTRIES[entry])
        count += axis_count

    # The center tile, number of steps doesn't matter really as long as total_steps % 2, it's full
    count += count_reachable(garden, total_steps, ENTRIES["O"])

    return count


def first(input: TextIO, steps: int = 64) -> int:
    garden = Garden.from_string(input.read().strip())

    return count_reachable(garden, steps)


def second(input: TextIO, steps: int = TOTAL_STEPS) -> int:
    garden = Garden.from_string(input.read().strip())

    return total_visitable(garden, steps)


# HELP METHODS
def how_many_steps_to_visit_all_from_entry(garden: Garden, entry: Coord) -> int:
    unvisited = {c for c, v in garden.items() if v != "#"}
    steps = 0
    unvisited.remove(entry)

    to_visit = {entry}
    while to_visit:
        steps += 1
        new_to_visit = set()
        for plot in to_visit:
            new_to_visit |= {
                nc for nc in garden.nbc4(plot) if garden[nc] == "." and nc in unvisited
            }
            unvisited -= new_to_visit
        to_visit = new_to_visit
    return steps


def how_many_visitable(garden: Garden) -> int:
    """This is a debug method that tells the max number of visitable squares for a given garden"""
    start = (0, 0)
    seen = {start}
    to_visit = [start]
    while to_visit:
        new_to_visit = set()
        for plot in to_visit:
            new_to_visit |= {
                nc for nc in garden.nbc4(plot) if garden[nc] == "." and nc not in seen
            }
            seen |= new_to_visit
        to_visit = new_to_visit
    return len(seen)
