from typing import Deque, Iterable, Sequence, TextIO
from collections import deque


Row = str
Counts = list[int]
Candidate = tuple[Row, Counts, str]


def get_candidates(candidate: Candidate) -> list[Candidate]:
    row, c, so_far = candidate

    left = iter(row)

    for spring in left:
        if len(c) == 0:
            s_left = spring + "".join(left)
            if "#" in s_left:
                return []
            return [("", [], so_far + len(s_left) * ".")]

        if spring == ".":
            so_far += "."
            continue

        elif spring == "#":
            so_far += "#"

            if len(c) == 0:
                return []

            next_count = c[0]
            c = c[1:]

            for _ in range(1, next_count):
                # Everything needs to be a # or a ?
                spring = next(left, None)
                if spring is None or spring == ".":
                    # Not working
                    return []
                # We assume #
                so_far += "#"

            # We finished the group of broken springs, the next one should be None or '.'
            spring = next(left, None)
            if spring is None:
                # We're done consuming, hopefully we're out of broken counts
                break

            if spring == "#":
                # Not good, should have been . or ?
                return []

            so_far += "."
        elif spring == "?":
            left = "".join(left)
            return [
                ("." + left, c, so_far),
                ("#" + left, c, so_far),
            ]

        else:
            raise Exception(f"Unexpected spring type={spring}")

    # No more springs
    if len(c) > 0:
        return []

    return [
        ("", [], so_far),
    ]


solved = 0


def solve(row: Row, counts: Counts) -> list[str]:
    found = []
    candidates = deque([(row, counts, "")])

    while candidates:
        c = candidates.pop()
        new_candidates = get_candidates(c)

        for new_c in new_candidates:
            if len(new_c[0]) == 0 and len(new_c[1]) == 0:
                found.append(new_c[2])
                continue
            else:
                candidates.append(new_c)

    global solved
    solved += 1
    print(solved)
    return found


def solve_fast_hopefully(row: Row, counts: Counts) -> int:
    found = 0
    candidates = deque([(row, counts, "")])

    # TODO we do depth first and memoize stuff that looks the same
    # TODO when guessing candidates (.|#), can look at how many #s needed and if . is possible
    # TODO when examining candidate, look at #s needed and whether it's possible

    while candidates:
        c = candidates.pop()
        new_candidates = get_candidates(c)

        for new_c in new_candidates:
            if len(new_c[0]) == 0 and len(new_c[1]) == 0:
                found += 1
                continue
            else:
                candidates.append(new_c)

    global solved
    solved += 1
    print(solved)
    return found


def parse_line(line: str) -> tuple[Row, Counts]:
    srow, scounts = line.split(" ")
    return srow, list(map(int, scounts.split(",")))


def parse_line2(line: str) -> tuple[Row, Counts]:
    srow, scounts = line.split(" ")
    srow = ((srow + "?") * 5)[:-1]
    scounts = ((scounts + ",") * 5)[:-1]
    return srow, list(map(int, scounts.split(",")))


def first(input: TextIO) -> int:
    lines = [parse_line(l) for l in input.read().strip().splitlines()]
    return sum(len(solve(row, counts)) for row, counts in lines)


def second(input: TextIO) -> int:
    lines = [parse_line2(l) for l in input.read().strip().splitlines()]
    return sum(solve_fast_hopefully(row, counts) for row, counts in lines)


"""
def trim(r: Row) -> Row:
    start = None
    end = None
    i = 0
    while start is None or end is None:
        if start is None and r[i] != ".":
            start = i
        if end is None and r[-i - 1] != ".":
            end = len(r) - i
        i += 1

    return r[start:end]
"""
