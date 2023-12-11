import re
from typing import TextIO

Nums = set[int]
Card = tuple[Nums, Nums]


def parse_nums(s_num: str) -> Nums:
    return set(map(int, re.split(r"\W+", s_num.strip())))


def parse_line(line: str) -> Card:
    win, actual = line.split(": ")[1].split(" | ")
    return parse_nums(win), parse_nums(actual)


def first(input: TextIO) -> int:
    lines = [parse_line(l.strip()) for l in input.readlines()]
    return sum(
        2 ** (win_count - 1)
        for win, actual in lines
        if ((win_count := len(win & actual)) > 0)
    )


def second(input: TextIO) -> int:
    lines = [parse_line(l.strip()) for l in input.readlines()]

    # Compute the scores
    card_scores = {}
    for i, (win, actual) in enumerate(lines):
        card_scores[i + 1] = len(win & actual)

    cards: dict[int, int] = {i: 1 for i in range(1, len(lines) + 1)}

    for i in range(1, len(lines) + 1):
        count = cards[i]
        score = card_scores[i]

        # Add the number of cards based on score
        for j in range(i + 1, i + score + 1):
            if j not in cards:
                break
            cards[j] += count

    return sum(cards.values())
