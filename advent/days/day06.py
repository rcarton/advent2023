import re
from typing import TextIO
import math

from advent.utils import prod

# Time, distance
Race = tuple[int, int]


def how_many_ways(race: Race) -> int:
    t = float(race[0])
    d = float(race[1])

    a = -1
    b = t
    c = -d

    delta = b**2 - 4 * a * c

    if delta <= 0:
        return 0

    x1 = (-b - delta**0.5) / (2 * a)
    x2 = (-b + delta**0.5) / (2 * a)
    x1, x2 = sorted([x1, x2])

    x1 = math.ceil(x1 if x1 != int(x1) else x1 + 1)
    x2 = math.floor(x2 if x2 != int(x2) else x2 - 1)

    if x2 < x1:
        return 0

    return x2 - x1 + 1


def first(input: TextIO) -> int:
    s_times, s_distances = input.readlines()
    to_int_list = lambda s: [int(i) for i in re.findall(r"\d+", s)]
    races: list[Race] = list(zip(to_int_list(s_times), to_int_list(s_distances)))

    return prod(how_many_ways(r) for r in races)


def second(input: TextIO) -> int:
    s_times, s_distances = input.readlines()
    time = int("".join(re.findall(r"\d+", s_times)))
    distance = int("".join(re.findall(r"\d+", s_distances)))
    return how_many_ways((time, distance))
