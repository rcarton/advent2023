import itertools as it
import re
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import DefaultDict, Deque, TextIO

from termcolor import cprint

from advent.intervals import Interval
from advent.matrix import Coord, Direction, get_delta_dir
from advent.utils import tadd


@dataclass
class Instruction:
    direction: Direction
    count: int
    color: str


DigPlan = list[Instruction]

Trench = DefaultDict[Coord, list[Direction]]
Vertices = dict[Coord, list[Direction]]
Segment = tuple[Coord, Coord]

#  segments sorted by start row, col ascending
V_Segments = list[Segment]

# segments sorted by start row, col ascending
H_Segments = list[Segment]


def direction_from_letter(c: str) -> Direction:
    return {
        "R": "right",
        "D": "down",
        "U": "up",
        "L": "left",
    }[c]


def direction_from_number(i: int) -> Direction:
    directions: dict[int, Direction] = {
        0: "right",
        1: "down",
        2: "left",
        3: "up",
    }
    return directions[i]


def parse_input(input: TextIO, part_2: bool = False) -> DigPlan:
    dig_plan: DigPlan = []

    for line in input.read().strip().splitlines():
        s_dir, s_count, s_color = re.match(
            r"^([RDLU]) (\d+) \((#\w+)\)$", line
        ).groups()

        if not part_2:
            dig_plan.append(
                Instruction(direction_from_letter(s_dir), int(s_count), s_color)
            )
        else:
            hex_count = int(s_color[1:6], base=16)
            i_dir = int(s_color[6])
            dig_plan.append(
                Instruction(direction_from_number(i_dir), hex_count, s_color)
            )

    return dig_plan


def instruction_to_vertices(
    dig_plan: DigPlan,
) -> tuple[Vertices, H_Segments, V_Segments]:
    curr = (0, 0)
    vertices: DefaultDict[Coord, list[Direction]] = defaultdict(list)
    h_seg: H_Segments = []
    v_seg: V_Segments = []
    for instruction in dig_plan:
        start = curr
        delta = get_delta_dir(instruction.direction)
        delta = (delta[0] * instruction.count, delta[1] * instruction.count)
        end = tadd(start, delta)
        vertices[start].append(instruction.direction)
        vertices[end].append(instruction.direction)
        curr = end

        if instruction.direction in ("up", "down"):
            start, end = (start, end) if start[0] <= end[0] else (end, start)
            v_seg.append((start, end))
        else:
            start, end = (start, end) if start[1] <= end[1] else (end, start)
            h_seg.append((start, end))

    # Flip the directions for the start
    vertices[(0, 0)] = list(reversed(vertices[(0, 0)]))

    # Sort the segments
    h_seg = sorted(h_seg, key=lambda segs: segs[0])
    v_seg = sorted(v_seg, key=lambda segs: segs[0])

    return vertices, h_seg, v_seg


def dig_trench(dig_plan: DigPlan) -> Trench:
    start = (0, 0)
    trench = defaultdict(list)

    curr = start
    for instruction in dig_plan:
        trench[curr].append(instruction.direction)
        for _ in range(instruction.count):
            curr = tadd(curr, get_delta_dir(instruction.direction))
            trench[curr].append(instruction.direction)

    # Flip the start
    trench[0, 0] = list(reversed(trench[0, 0]))

    return trench


def dig_interior(dig_plan: DigPlan, trench: Trench) -> set[Coord]:
    min_row, min_col = next(iter(trench.keys()))
    max_row, max_col = min_row, min_col

    # Find the min/max row and column, these are all the cubes we're considering for digging
    for row, col in trench:
        min_row, max_row = min(min_row, row), max(max_row, row)
        min_col, max_col = min(min_col, col), max(max_col, col)

    inside: set[Coord] = set()

    # Not super efficient, we're looking at every point to figure out if it's inside using "ray tracing"
    # odd number of intersections => inside
    for c in it.product(range(min_row, max_row + 1), range(min_col, max_col + 1)):
        if c in trench:
            # It's already dug out, not inside nor outside
            continue

        row, col = c
        # Count intersections to the right
        count = 0
        for i_col in range(col + 1, max_col + 1):
            curr = (row, i_col)
            # Ignore horizontal rows in the count, but we do count corners
            if curr in trench and (
                trench[curr]
                not in (
                    ["left"],
                    ["right"],
                    ["right", "up"],
                    ["down", "left"],
                    ["down", "right"],
                    ["left", "up"],
                )
            ):
                count += 1

        # If odd number of intersections, then
        if count % 2 == 1:
            inside.add((row, col))

    return inside


def debug(trench: Trench, interior: set[Coord]) -> None:
    min_row, min_col = next(iter(trench.keys()))
    max_row, max_col = min_row, min_col

    # Find the min/max row and column, these are all the cubes we're considering for digging
    for row, col in trench:
        min_row, max_row = min(min_row, row), max(max_row, row)
        min_col, max_col = min(min_col, col), max(max_col, col)

    print()

    print_color = lambda x, color: cprint(x, color, end="")

    for row in range(min_row, max_row + 1):
        print()
        for col in range(min_col, max_col + 1):
            c = (row, col)
            to_print = "."
            if c in trench:
                to_print = "#"
            if c in interior:
                to_print = "*"
            if to_print == "*":
                print_color(to_print, "yellow")
            elif to_print == "#":
                if c == (0, 0):
                    print("X", end="")
                    continue
                if len(trench[c]) == 2:
                    if trench[c] in (
                        ["right", "up"],
                        ["down", "left"],
                        ["down", "right"],
                        ["left", "up"],
                    ):
                        print_color(to_print, "red")
                    else:
                        print_color(to_print, "green")
                else:
                    print(to_print, end="")
            else:
                print(to_print, end="")
    print()


def overlap(i1: Interval, i2: Interval) -> bool:
    i1, i2 = (i1, i2) if i1[0] < i2[0] else (i2, i1)
    return i2[0] <= i1[1]


def merge(i1: Interval, i2: Interval) -> list[Interval]:
    i1, i2 = (i1, i2) if i1[0] <= i2[0] else (i2, i1)

    s1, e1 = i1
    s2, e2 = i2
    s1, s2 = (s1, s2) if s1 < s2 else (s2, s1)
    e1, e2 = (e1, e2) if e1 < e2 else (e2, e1)

    if s2 == e1:
        return [(s1, e2)]

    r = [(s1, s2), (e1, e2)]
    return [(a, b) for a, b in r if (a < b)]


def update_intervals(
    intervals: list[Interval], segments: Deque[Segment]
) -> tuple[list[Interval], int]:
    # Grab all the next segments to consider
    first_seg = segments.popleft()
    current_row = first_seg[0][0]

    new_segments = [first_seg]
    while segments:
        segment = segments.popleft()
        if segment[0][0] > current_row:
            # put it back, break
            segments.appendleft(segment)
            break
        new_segments.append(segment)

    # Now we have all the segments to consider, in order
    existing_intervals = intervals
    new_intervals = [(start[1], end[1]) for start, end in new_segments]

    all_intervals = iter(sorted(existing_intervals + new_intervals))

    intervals = []

    current = next(all_intervals, None)

    while True:
        follow = next(all_intervals, None)
        if not current or not follow:
            # We're done
            if current:
                intervals.append(current)
            break

        assert current is not None

        # No overlap, add and move on
        if not overlap(current, follow):
            intervals.append(current)
            current = follow
            continue

        # Overlap, we need to merge
        merged = merge(current, follow)
        if len(merged) == 0:
            # Everything canceled
            current = next(all_intervals, None)
            continue
        if len(merged) == 1:
            current = merged[0]
            continue
        if len(merged) == 2:
            intervals.append(merged[0])
            current = merged[1]
            continue

    return intervals, current_row


def union(i1: Interval, i2: Interval) -> Interval:
    # They must overlap
    i1, i2 = (i1, i2) if i1[0] <= i2[0] else (i2, i1)

    s1, e1 = i1
    s2, e2 = i2
    s1, s2 = (s1, s2) if s1 < s2 else (s2, s1)
    e1, e2 = (e1, e2) if e1 < e2 else (e2, e1)
    return min(s1, s2), max(e1, e2)


def union_intervals(old_i: list[Interval], new_i: list[Interval]) -> list[Interval]:
    # We need a kind of union
    all_intervals = iter(sorted(old_i + new_i))

    intervals = []
    current = next(all_intervals, None)
    while True:
        follow = next(all_intervals, None)
        if not current or not follow:
            if current:
                intervals.append(current)
            break

        if not overlap(current, follow):
            intervals.append(current)
            current = follow
            continue

        current = union(current, follow)
    return intervals


def count(hsegs: H_Segments) -> int:
    assert len(hsegs) > 0

    segments = deque(hsegs)

    intervals = []

    total = 0
    last_row = None
    old_intervals = []
    while segments:
        intervals, new_row = update_intervals(intervals, segments)

        new_surface = 0
        if last_row is not None:
            # We stop a row early, we need to add the transition row differently
            diff = new_row - last_row - 1
            new_surface = diff * sum(1 + end - start for start, end in old_intervals)

            # Todo figure out how to add the transition row

        transition_intervals = union_intervals(old_intervals, intervals)
        transition_surface = sum(1 + end - start for start, end in transition_intervals)

        print(f"last_row={last_row} new_row={new_row} new_surface={new_surface}")
        total += new_surface + transition_surface

        last_row = new_row
        old_intervals = intervals

    return total


def first_unoptimized(input: TextIO) -> int:
    dig_plan = parse_input(input)
    trench = dig_trench(dig_plan)
    interior = dig_interior(dig_plan, trench)
    debug(trench, interior)
    return len(trench) + len(interior)


def first(input: TextIO) -> int:
    dig_plan = parse_input(input)
    vv, hseg, vseg = instruction_to_vertices(dig_plan)
    return count(hseg)


def second(input: TextIO) -> int:
    dig_plan = parse_input(input, part_2=True)
    vv, hseg, vseg = instruction_to_vertices(dig_plan)
    return count(hseg)
