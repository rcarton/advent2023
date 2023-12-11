import itertools as it
import re
from typing import TextIO
from collections import defaultdict
from math import lcm

Network = dict[str, tuple[str, str]]


def parse_network(s: str) -> Network:
    network: Network = {}
    for line in s.split("\n"):
        m = re.match(
            r"^(?P<name>\w+) = \((?P<left>\w+), (?P<right>\w+)\)", line
        ).groupdict()
        network[m["name"]] = (m["left"], m["right"])
    return network


def first(input: TextIO) -> int:
    s_instructions, s_net = input.read().strip().split("\n\n")

    instructions = it.cycle(s_instructions.strip())
    network = parse_network(s_net)

    count = 0
    current = "AAA"
    while current != "ZZZ":
        instr = next(instructions)
        current = network[current][0 if instr == "L" else 1]
        count += 1

    return count


def second(input: TextIO) -> int:
    s_instructions, s_net = input.read().strip().split("\n\n")

    instructions = it.cycle(s_instructions.strip())
    network = parse_network(s_net)

    count = 0
    currents = [c for c in network.keys() if c[-1] == "A"]
    done = False
    cycles = defaultdict(lambda: 0)
    while not done:
        instr = next(instructions)
        currents = [network[c][0 if instr == "L" else 1] for c in currents]
        count += 1

        for i, c in enumerate(currents):
            if c[-1] == "Z" and i not in cycles:
                cycles[i] = count
        done = len(cycles) == len(currents)

    return lcm(*cycles.values())
