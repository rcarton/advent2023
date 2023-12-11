from collections import Counter, defaultdict
from functools import cmp_to_key
from typing import TextIO
from dataclasses import dataclass
from enum import StrEnum

Card = str


CARDS = "A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2".split(", ")
CARDS_PART2 = "A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J".split(", ")


def cmp_cards(a: Card, b: Card) -> int:
    ia = CARDS.index(a)
    ib = CARDS.index(b)

    return -1 * (ia - ib)


def cmp_cards2(a: Card, b: Card) -> int:
    ia = CARDS_PART2.index(a)
    ib = CARDS_PART2.index(b)

    return -1 * (ia - ib)


class HandType(StrEnum):
    FIVE_OAK = "five_of_a_kind"
    FOUR_OAK = "four_of_a_kind"
    FULL = "full_house"
    THREE_OAK = "three_of_a_kind"
    TWO_PAIRS = "two_pairs"
    PAIR = "pair"
    HIGH_CARD = "high_card"


HAND_TYPE_ORDER = [
    HandType.FIVE_OAK,
    HandType.FOUR_OAK,
    HandType.FULL,
    HandType.THREE_OAK,
    HandType.TWO_PAIRS,
    HandType.PAIR,
    HandType.HIGH_CARD,
]


card_key_fn = cmp_to_key(cmp_cards)
card_key_fn2 = cmp_to_key(cmp_cards2)


def get_comparable_hand(cards: list[Card]) -> list[Card]:
    """
    32TT2 -> [T, 2, 3]
    AK2344 -> [4, A, K, 2, 3]
    """
    d = defaultdict(list)
    for card, count in Counter(cards).items():
        d[count].append(card)

    new_cards = []
    for k in sorted(d.keys(), reverse=True):
        for card in sorted(d[k], key=card_key_fn, reverse=True):
            new_cards.append(card)

    return new_cards


@dataclass
class Hand:
    cards: list[Card]
    bid: int
    part2: bool = False

    def __lt__(self, other) -> bool:
        ts = get_hand_type(self)
        to = get_hand_type(other)

        # Different types, highest type wins
        if ts != to:
            # If the index is higher, then the card is of lower value since the order is descending (FIVE_OAK = 0)
            return HAND_TYPE_ORDER.index(ts) > HAND_TYPE_ORDER.index(to)

        for a, b in zip(self.cards, other.cards):
            r = cmp_cards2(a, b) if self.part2 else cmp_cards(a, b)
            if r == 0:
                continue
            return r < 0

        # Normal poker logic below
        # # Same type, we need to group by count, and within a count sort by card value
        # ch_self = get_comparable_hand(self.cards)
        # ch_other = get_comparable_hand(other.cards)
        #
        # for a, b in zip(ch_self, ch_other):
        #     r = cmp_cards(a, b)
        #     if r == 0:
        #         continue
        #     return r < 0
        #
        # return True

    def __repr__(self):
        return f"{''.join(self.cards)}, {self.bid}"


def get_hand_type(h: Hand) -> HandType:
    counter = Counter(h.cards)

    if h.part2:
        j_count = counter["J"]
        if j_count == 5:
            return HandType.FIVE_OAK

        # Else we will replace Js with the best other card
        del counter["J"]
        best_card = get_comparable_hand(list(filter(lambda c: c != "J", h.cards)))[0]
        counter[best_card] += j_count

    counts = sorted(counter.values(), reverse=True)

    if counts[0] == 5:
        return HandType.FIVE_OAK
    if counts[0] == 4:
        return HandType.FOUR_OAK
    if counts[0] == 3:
        if counts[1] == 2:
            return HandType.FULL
        return HandType.THREE_OAK
    if counts[0] == 2:
        if counts[1] == 2:
            return HandType.TWO_PAIRS
        return HandType.PAIR
    return HandType.HIGH_CARD


def first(input: TextIO) -> int:
    lines = input.readlines()
    hands = []
    for l in lines:
        cards, sbid = l.strip().split(" ")
        hands.append(Hand(list(cards), int(sbid)))

    hands = sorted(hands)
    # for h in hands:
    #     print(
    #         f"{''.join(h.cards)}\t{''.join(get_comparable_hand(h.cards))}\t{get_hand_type(h)}\t{h.bid}"
    #     )
    return sum(h.bid * rank for rank, h in enumerate(hands, start=1))


def second(input: TextIO) -> int:
    lines = input.readlines()
    hands = []
    for l in lines:
        cards, sbid = l.strip().split(" ")
        hands.append(Hand(list(cards), int(sbid), True))

    hands = sorted(hands)
    # for h in hands:
    #     print(f"{''.join(h.cards)}\t{get_hand_type(h)}\t{h.bid}")
    return sum(h.bid * rank for rank, h in enumerate(hands, start=1))
