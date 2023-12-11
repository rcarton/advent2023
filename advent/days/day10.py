import itertools as it
from collections import deque
from typing import Literal, Optional, TextIO

from advent.matrix import Coord, Matrix

Dir = Literal["top", "right", "bottom", "left"]
Pipe = Literal["|", "F", "7", "J", "L", "-"]


PRETTIFY = {
    "L": "┗",
    "J": "┛",
    "7": "┓",
    "F": "┏",
    "|": "┃",
    "-": "━",
    "S": "S",
}

# Current direction -> new direction
PIPES_DIR_CHANGE: dict[Dir, dict[Pipe, Dir]] = {
    "top": {
        "|": "top",
        "F": "right",
        "7": "left",
    },
    "bottom": {
        "|": "bottom",
        "L": "right",
        "J": "left",
    },
    "left": {
        "-": "left",
        "L": "top",
        "F": "bottom",
    },
    "right": {
        "-": "right",
        "7": "bottom",
        "J": "top",
    },
}

Sketch = Matrix[Pipe]

MOVES: dict[Dir, Coord] = {
    "top": (-1, 0),
    "right": (0, 1),
    "bottom": (1, 0),
    "left": (0, -1),
}

# Since we are going clockwise, inside should be consistent
INSIDE_CW: dict[Pipe, dict[Dir, list[Coord]]] = {
    "|": {
        "top": [(0, 1)],
        "bottom": [(0, -1)],
    },
    "-": {
        "left": [(-1, 0)],
        "right": [(1, 0)],
    },
    "J": {
        "left": [(-1, -1)],
        "top": [(1, 0), (1, 1), (0, 1)],
    },
    "7": {
        "bottom": [(1, -1)],
        "left": [(-1, 0), (-1, 1), (0, 1)],
    },
    "F": {
        "right": [(1, 1)],
        "bottom": [(0, -1), (-1, -1), (-1, 0)],
    },
    "L": {
        "top": [(-1, 1)],
        "right": [(0, -1), (1, -1), (1, 0)],
    },
}


def replace_start_with_pipe(sketch: Sketch, sc: Coord) -> Pipe:
    in_out = []
    for dir, delta in MOVES.items():
        new_c = (sc[0] + delta[0], sc[1] + delta[1])
        if not sketch.is_valid_coord(new_c):
            continue

        value = sketch[new_c]
        if value in PIPES_DIR_CHANGE[dir]:
            in_out.append(dir)
    assert len(in_out) == 2
    in_out = tuple(sorted(in_out))

    replacements: dict[tuple[Dir, Dir], Pipe] = {
        ("bottom", "top"): "|",
        ("left", "right"): "-",
        ("left", "top"): "J",
        ("bottom", "right"): "F",
        ("right", "top"): "L",
        ("bottom", "left"): "7",
    }

    return replacements[in_out]


def find_start(sketch: Sketch, inverse: bool = False) -> tuple[Coord, Dir]:
    sc = None
    for c in sketch.all_coords():
        if sketch[c] == "S":
            sc = c
    assert sc is not None

    boop = 0
    # We should be going clockwise, but really we don't know, that's what inverse is for
    for dir, delta in MOVES.items():
        new_c = (sc[0] + delta[0], sc[1] + delta[1])
        if not sketch.is_valid_coord(new_c):
            continue

        value = sketch[new_c]
        if value in PIPES_DIR_CHANGE[dir]:
            if not inverse or boop == 1:
                return sc, dir
            boop += 1

    raise Exception("Error finding start coords and direction")


def move_next(sketch: Sketch, curr: Coord, dir: Dir) -> tuple[Coord, Dir]:
    # Find the next pipe section
    delta = MOVES[dir]
    new_c = (curr[0] + delta[0], curr[1] + delta[1])

    value = sketch[new_c]
    if value == "S":
        # Return the same as the starting direction
        value = replace_start_with_pipe(sketch, new_c)

    new_dir = PIPES_DIR_CHANGE[dir][value]

    return new_c, new_dir


def find_loop(sketch: Sketch) -> list[Coord]:
    # Navigate the loop
    curr, dir = find_start(sketch)
    path = []
    while not path or sketch[curr] != "S":
        curr, dir = move_next(sketch, curr, dir)
        path.append(curr)

    return path


def explore(sketch: Sketch, loops: set[Coord], start: Coord) -> set[Coord]:
    seen = set()
    to_visit = deque([start])
    while to_visit:
        curr = to_visit.pop()
        if curr in seen:
            # Already visited, we're skipping
            continue

        seen.add(curr)
        to_visit.extend(set(sketch.neighbor_coords(curr)) - loops - seen)

    return seen


def explore_candidates(
    sketch: Sketch, loops: set[Coord], curr: Coord, dir: Dir
) -> set[Coord]:
    seen = set()
    pipe = sketch[curr]
    if pipe == "S":
        pipe = replace_start_with_pipe(sketch, curr)
    for delta in INSIDE_CW[pipe][dir]:
        inside_candidate = (curr[0] + delta[0], curr[1] + delta[1])
        if (
            not sketch.is_valid_coord(inside_candidate)
            or inside_candidate in seen
            or inside_candidate in loops
        ):
            continue
        seen |= explore(sketch, loops, inside_candidate)
    return seen


def find_inside(sketch: Sketch, loop: list[Coord], inverse: bool = False) -> set[Coord]:
    loops = set(loop)
    seen = set()

    # Navigate the loop, this time looking for inside points
    curr, dir = find_start(sketch, inverse)
    path = []
    while not path or sketch[curr] != "S":
        curr, dir = move_next(sketch, curr, dir)
        path.append(curr)

        pprint(sketch, seen, curr)
        # We found a point inside, expand from here
        seen |= explore_candidates(sketch, loops, curr, dir)

    inside = seen

    return inside


def first(input: TextIO) -> int:
    sketch = Sketch.from_string(input.read().strip())
    path = find_loop(sketch)

    # It should be an even number (odd number of pipes, + S), that's the full loop ending with the starting point
    assert len(path) % 2 == 0

    return len(path) // 2


def pprint(sketch: Sketch, inside: set[Coord], mark: Optional[Coord] = None) -> None:
    sketch = Sketch(sketch.data, sketch.width, sketch.height)
    loop = find_loop(sketch)
    sc, _ = find_start(sketch)
    # new_s = replace_start_with_pipe(sketch, sc)

    for c in sketch.all_coords():
        if c == mark:
            sketch[c] = "X"
        elif c in inside:
            sketch[c] = "I"
        elif c in loop:
            sketch[c] = PRETTIFY[sketch[c]]
            pass
        else:
            sketch[c] = "."

    print(sketch)
    # print(f"new_s={new_s}")
    # print(len(inside))
    print()


def is_clockwise(loop: list[Coord]) -> bool:
    # TODO math is wrong, but it should be doable
    return sum((b[1] - a[1]) * (b[0] - a[0]) for a, b in it.pairwise(loop)) > 0


def second(input: TextIO) -> int:
    sketch = Sketch.from_string(input.read().strip())
    loop = find_loop(sketch)

    print(f"is_clockwise={is_clockwise(loop)}")

    # Find points outside loop
    inside = find_inside(sketch, loop, True)
    pprint(sketch, inside)

    is_inverted = any(
        c[0] == 0 or c[0] == sketch.height - 1 or c[1] == 0 or c[1] == sketch.width - 1
        for c in inside
    )
    if is_inverted:
        _, original_dir = find_start(sketch)
        _, new_dir = find_start(sketch, True)
        inside = find_inside(sketch, loop, True)
        print(f"-> Is inverted, tried {original_dir} now trying {new_dir}")
        pprint(sketch, inside)

    return len(inside)
