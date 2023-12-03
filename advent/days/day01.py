from typing import TextIO
import re

def first(input: TextIO) -> int:
    lines = [re.findall(r'\d', l) for l in input.readlines()]
    lines_firstlast = [int(l[0] + l[-1]) for l in lines]
    return sum(lines_firstlast)


# The lookahead allows overlapping matches (eightwo -> 8, 2)
PATTERN_DIGIT_OR_LETTERS = r'(?=(one|two|three|four|five|six|seven|eight|nine|\d))'
NUMBERS = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}

def second(input: TextIO) -> int:
    lines = [re.findall(PATTERN_DIGIT_OR_LETTERS, l) for l in input.readlines()]
    lines_as_digits = [list(map(lambda s: NUMBERS.get(s, s), l)) for l in lines]
    return sum(int(l[0] + l[-1]) for l in lines_as_digits)
