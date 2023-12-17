from dataclasses import dataclass
from typing import Generic, Optional, TextIO, TypeVar
from functools import reduce
import re


T = TypeVar("T")


@dataclass
class Element(Generic[T]):
    label: str
    value: T

    next_el: Optional["Element[T]"] = None


class HashMapLinkedList(Generic[T]):
    head: Optional[Element[T]] = None

    def __setitem__(self, label: str, value: T) -> None:
        prev = None
        curr = self.head
        while curr:
            if curr.label == label:
                curr.value = value
                break
            prev, curr = curr, curr.next_el
        else:
            el = Element(label, value)
            if self.head is None:
                self.head = el
            else:
                prev.next_el = el

    def __delitem__(self, label: str) -> Optional[T]:
        prev = None
        curr = self.head
        while curr:
            if curr.label == label:
                if prev is None:
                    self.head = curr.next_el
                else:
                    prev.next_el = curr.next_el
                return curr.value
            prev, curr = curr, curr.next_el
        # not found

    def __iter__(self) -> T:
        curr = self.head
        while curr:
            yield curr.value
            curr = curr.next_el

    def __len__(self) -> int:
        total = 0
        for _ in self:
            total += 1
        return total

    def items(self) -> tuple[str, T]:
        curr = self.head
        while curr:
            yield curr.label, curr.value
            curr = curr.next_el

    def __repr__(self):
        return " ".join(f"[{label} {value}]" for label, value in self.items())


class BoxMap(Generic[T]):
    boxes: list[HashMapLinkedList[T]]

    def __init__(self):
        self.boxes = [HashMapLinkedList() for _ in range(256)]

    def __setitem__(self, label: str, value: T) -> None:
        self.boxes[hhash(label)][label] = value

    def __delitem__(self, label: str) -> None:
        del self.boxes[hhash(label)][label]

    def focusing_power(self):
        return sum(
            (j + 1) * sum((i + 1) * v for i, v in enumerate(b))
            for j, b in enumerate(self.boxes)
        )


Box = HashMapLinkedList[int]


def hhash(s: str) -> int:
    return reduce(lambda p, c: ((p + ord(c)) * 17) % 256, s, 0)


def first(input: TextIO) -> int:
    return sum(hhash(s) for s in input.read().strip().split(","))


def second(input: TextIO) -> int:
    init_seq = input.read().strip().split(",")
    init_seq = [
        re.match(r"(?P<label>\w+)(?P<instr>[=-])(?P<value>\d+)?", i).groupdict()
        for i in init_seq
    ]

    boxes = BoxMap()

    for step in init_seq:
        label = step["label"]
        lens = int(step["value"]) if step["value"] is not None else None
        instr = step["instr"]
        if instr == "=":
            boxes[label] = lens
        elif instr == "-":
            del boxes[label]
        else:
            raise Exception("Unknown instruction")

    return boxes.focusing_power()
