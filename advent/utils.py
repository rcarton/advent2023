import io
import operator
from functools import reduce
from pathlib import Path
from typing import List, Optional, Sequence, TextIO, TypeVar, Union

from advent.matrix import Coord


T = TypeVar("T")


def prod(iterable):
    """Equivalent of sum() for multiplying"""
    return reduce(operator.mul, iterable, 1)


def tadd(*tuples: T) -> T:
    return tuple(sum(l) for l in zip(*tuples))


def binseq_to_int(binseq: Sequence[Union[str, int, bool]]) -> int:
    """Turn a sequence that can be mapped to bits into its integer representation:

    Examples:
        - '101' -> 5
        - [True, False, True] -> 5
        - [1, 0, 1] -> 5

    """
    return sum(int(j) << i for i, j in enumerate(reversed(binseq)))


def add_wrap(val: int, incr: int, max_val: int, start_at_one: Optional[bool] = True):
    """Add incr to val, and wrap around at 1 if val+incr > max_val"""
    return (val + incr - 1) % max_val + (1 if start_at_one else 0)


def chunk(s: Sequence[T], count: int) -> List[Sequence[T]]:
    return [s[count * i : count * i + count] for i in range(len(s) // count)]


def get_input_filename_for_day(day_num: int) -> Path:
    """Return the Path to the input file for a given day."""
    return Path(Path(__file__).parent.parent.absolute(), "data", f"day{day_num:02}.txt")


def get_data_for_day(day_num: int) -> TextIO:
    """Get data for tests typically."""

    with open(get_input_filename_for_day(day_num)) as reader:
        return io.StringIO(reader.read())


def intersect(r1: tuple[int, int], r2: tuple[int, int]) -> Optional[tuple[int, int]]:
    # Sort by first number ascending
    r1, r2 = sorted([r1, r2])

    r1s, r1e = r1
    r2s, r2e = r2

    if r1e < r2s:
        # No intersection
        return None

    return max(r1s, r2s), min(r1e, r2e)


def manhattan_distance(c1: Coord, c2: Coord) -> int:
    return abs(c2[0] - c1[0]) + abs(c2[1] - c1[1])
