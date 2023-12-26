import io
import re
from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Literal, Optional, TextIO, cast

from advent.utils import prod

Pulse = Literal[0, 1]


@dataclass
class Module:
    name: str
    # Name of destination modules
    dests: list[str]
    mtype: str

    def handle(self, pulse: Pulse, source: str) -> Optional[Pulse]:
        """Default module is a broadcaster basically"""
        return pulse

    def __repr__(self):
        return f"{self.mtype}{self.name}"


@dataclass
class Broadcaster(Module):
    mtype: str = "broadcaster"
    pass


@dataclass
class FlipFlop(Module):
    """Flip-flop modules (prefix %) are either on or off; they are initially off. If a flip-flop module receives a
    high pulse, it is ignored and nothing happens. However, if a flip-flop module receives a low pulse,
    it flips between on and off. If it was off, it turns on and sends a high pulse. If it was on, it turns off and
    sends a low pulse."""

    mtype: str = "%"
    state: bool = False

    def handle(self, pulse: Pulse, source: str) -> Optional[Pulse]:
        # Ignore high pulses
        if pulse == 1:
            return
        # low if on, high if off
        new_pulse: Pulse = 0 if self.state else 1
        # flip flop
        self.state = not self.state
        return new_pulse

    def __repr__(self):
        return super().__repr__() + f" state={self.state}"


@dataclass
class Conjunction(Module):
    """When a pulse is received, the conjunction module first updates its memory for that input. Then, if it
    remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.
    """

    mtype: str = "&"
    memory: dict[str, Pulse] = field(default_factory=dict)

    def add_input(self, name: str) -> None:
        self.memory[name] = 0

    def handle(self, pulse: Pulse, source: str) -> Optional[Pulse]:
        self.memory[source] = pulse

        if all(last_pulse == 1 for last_pulse in self.memory.values()):
            return 0
        return 1

    def __repr__(self):
        return (
            super().__repr__()
            + f" memory=[{','.join(f'{k}={v}' for k, v in self.memory.items())}]"
        )


MODULE_TYPES = {m.mtype: m for m in [Broadcaster, Conjunction, FlipFlop]}

Modules = dict[str, Module]


def parse_module(smod: str) -> Module:
    """
    broadcaster -> a, b, c
    %a -> b
    %b -> c
    %c -> inv
    &inv -> a
    """
    mtype, name, sdests = re.match(r"(broadcaster|%|&)(\w*) -> (.*)", smod).groups()
    name = name or "broadcaster"
    dests = sdests.split(", ")
    clz = MODULE_TYPES[mtype]
    return clz(name, dests)


def parse_input(input: TextIO) -> Modules:
    lines = input.read().strip().splitlines()
    modules: Modules = {}
    for line in lines:
        m = parse_module(line)
        modules[m.name] = m

    # Set the inputs for Conjunction modules
    for m in modules.values():
        for d_name in m.dests:
            d = modules.get(d_name, None)
            if isinstance(d, Conjunction):
                d.add_input(m.name)

    return modules


# source, dest, pulse
PulseToHandle = tuple[str, str, Pulse]
PulseQueue = Deque[PulseToHandle]


class RxException(Exception):
    low: int
    high: int

    def __init__(self, low: int, high: int):
        self.low = low
        self.high = high
        super().__init__()


def press(modules: Modules, stop_on: Optional[str] = None) -> tuple[int, int]:
    low_count = 0
    high_count = 0
    pq: PulseQueue = deque([("button", "broadcaster", 0)])
    while pq:
        source, dest, pulse = pq.popleft()
        # print(source, dest, pulse)

        if dest == stop_on and pulse == 0:
            raise RxException(low_count, high_count)

        if pulse:
            high_count += 1
        else:
            low_count += 1

        if dest not in modules:
            continue

        module = modules[dest]
        pulse = module.handle(pulse, source)
        if pulse is None:
            continue

        for dest in module.dests:
            pq.append((module.name, dest, pulse))
    return low_count, high_count


def first(input: TextIO) -> int:
    modules = parse_input(input)
    counts = [0, 0]
    for _ in range(1000):
        low, high = press(modules)
        counts[0] += low
        counts[1] += high
    return counts[0] * counts[1]


def counts_for_zero(input: TextIO, stop_on: str) -> int:
    modules = parse_input(input)
    low, high = 0, 0
    count = 0
    while True:
        try:
            count += 1
            nl, nh = press(modules, stop_on)

            low += nl
            high += nh
        except RxException as e:
            low += e.low
            high += e.high
            break

    return count


def second(input: TextIO) -> int:
    s = input.read()
    js = counts_for_zero(io.StringIO(s), "js")
    qs = counts_for_zero(io.StringIO(s), "qs")
    dt = counts_for_zero(io.StringIO(s), "dt")
    ts = counts_for_zero(io.StringIO(s), "ts")

    print(js, qs, dt, ts)
    return js * qs * dt * ts
