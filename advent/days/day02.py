from typing import TextIO, Literal, List
from dataclasses import dataclass
import re

from advent.utils import prod

Color = Literal["red", "blue", "green"]
Hand = dict[Color, int]
Bag = Hand
Minimum = Hand


@dataclass(frozen=True)
class Game:
    id: int
    hands: List[Hand]


def parse_hand(s_hand: str) -> Hand:
    h = {}
    for count_and_color in s_hand.strip().split(", "):
        s_count, color = count_and_color.split(" ")
        h[color] = int(s_count)
    return h


def parse_hands(s_hands: str) -> List[Hand]:
    return [parse_hand(s_hand) for s_hand in s_hands.split("; ")]


def parse_game(s: str) -> Game:
    game_num, s_hands = s.split(": ")
    id = int(re.search(r"\d+", game_num)[0])
    hands = parse_hands(s_hands)
    return Game(id, hands)


def is_possible(g: Game, b: Bag) -> bool:
    for hand in g.hands:
        for color, count in hand.items():
            if count > b[color]:
                return False
    return True


def get_minimum_for_game(g: Game) -> Minimum:
    m = dict(red=0, green=0, blue=0)
    for h in g.hands:
        for color, count in h.items():
            m[color] = max(m[color], count)
    return m


def first(input: TextIO) -> int:
    bag = dict(red=12, green=13, blue=14)
    games = [parse_game(l) for l in input.readlines()]
    return sum(g.id for g in games if is_possible(g, bag))


def second(input: TextIO) -> int:
    games = [parse_game(l) for l in input.readlines()]
    return sum(prod(get_minimum_for_game(g).values()) for g in games)
