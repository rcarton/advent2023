from collections import deque
from typing import TextIO
import itertools as it


def extrapolate(nums: list[int]) -> int:
    stack = deque([nums])

    # Go down, we don't actually need the full array in the stack, but why not
    current = nums
    while not all(n == 0 for n in current):
        current = [b - a for a, b in it.pairwise(current)]
        stack.append(current)

    # Now go back up
    current = stack.pop()
    while stack:
        next_curr = stack.pop()
        next_curr.append(current[-1] + next_curr[-1])
        current = next_curr

    return current[-1]


def extrapolate_backwards(nums: list[int]) -> int:
    stack = deque([nums])

    current = nums
    while not all(n == 0 for n in current):
        current = [b - a for a, b in it.pairwise(current)]
        stack.append(current)

    # Now go back up
    current = stack.pop()
    while stack:
        next_curr = stack.pop()
        next_curr.insert(0, next_curr[0] - current[0])
        current = next_curr

    return current[0]


def first(input: TextIO) -> int:
    lines = [list(map(int, l.split(" "))) for l in input.readlines()]
    return sum(extrapolate(nums) for nums in lines)


def second(input: TextIO) -> int:
    lines = [list(map(int, l.split(" "))) for l in input.readlines()]
    return sum(extrapolate_backwards(nums) for nums in lines)
