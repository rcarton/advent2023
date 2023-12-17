from typing import Optional, TextIO

from advent.utils import binseq_to_int

Rows = list[int]
Cols = list[int]
Pattern = tuple[Rows, Cols]


def parse_pattern(s: str) -> Pattern:
    rows = [list(map(lambda x: 0 if x == "." else 1, r)) for r in s.splitlines()]
    cols = zip(*rows)

    return [binseq_to_int(r) for r in rows], [binseq_to_int(c) for c in cols]


def has_one_bit_different(a: int, b: int) -> bool:
    xored = a ^ b
    return xored & (xored - 1) == 0


def find_reflection_in_list(l: list[int], smudge: bool = False) -> Optional[int]:
    for i in range(1, len(l)):
        size = min(i, len(l) - i)

        if not smudge:
            if all(a == b for a, b in zip(l[i - size : i], reversed(l[i : i + size]))):
                return i - 1
        else:
            equal = sum(
                a == b for a, b in zip(l[i - size : i], reversed(l[i : i + size]))
            )
            one_bit_diff = sum(
                a != b and has_one_bit_different(a, b)
                for a, b in zip(l[i - size : i], reversed(l[i : i + size]))
            )

            if equal == size - 1 and one_bit_diff == 1:
                return i - 1


def find_reflection_summary(p: Pattern, smudge: bool = False) -> int:
    rows, cols = p
    reflection = find_reflection_in_list(rows, smudge)
    if reflection is not None:
        return (reflection + 1) * 100

    reflection = find_reflection_in_list(cols, smudge)

    if reflection is not None:
        return reflection + 1

    raise Exception(f"Reflection not found in pattern={p}")


def first(input: TextIO) -> int:
    patterns = [parse_pattern(s) for s in input.read().strip().split("\n\n")]
    return sum(find_reflection_summary(p) for p in patterns)


def second(input: TextIO) -> int:
    patterns = [parse_pattern(s) for s in input.read().strip().split("\n\n")]
    return sum(find_reflection_summary(p, True) for p in patterns)
