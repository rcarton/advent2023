from typing import TextIO
from dataclasses import dataclass

from advent.utils import chunk, intersect


@dataclass(frozen=True)
class MapEntry:
    source: int
    destination: int
    range: int

    @classmethod
    def from_string(cls, s: str):
        _dest, _source, _range = map(int, s.strip().split(" "))
        return cls(_source, _dest, _range)

    def __lt__(self, other) -> bool:
        return self.source < other.source


@dataclass
class AlmanacMap:
    name: str
    entries: list[MapEntry]


def parse_almanac_map(s: str) -> AlmanacMap:
    s_name, *s_entries = s.split("\n")
    name = s_name.split(" ")[0]
    entries = [MapEntry.from_string(e.strip()) for e in s_entries]
    return AlmanacMap(name, sorted(entries))


def parse_all(s: str) -> tuple[list[int], list[AlmanacMap]]:
    s_seeds, *s_maps = s.strip().split("\n\n")
    seeds = [int(i) for i in s_seeds.strip().split(" ")[1:]]
    maps = [parse_almanac_map(m) for m in s_maps]

    return seeds, maps


def process_map(nums: list[int], amap: AlmanacMap) -> list[int]:
    nums = iter(sorted(nums))
    entries = iter(amap.entries)

    new_nums = []

    num = next(nums, None)
    entry = next(entries, None)
    while num:
        if entry is None:
            new_nums.append(num)
        elif num < entry.source:
            new_nums.append(num)
        elif num < (entry.source + entry.range):
            new_nums.append(entry.destination + num - entry.source)
        else:
            entry = next(entries, None)
            continue

        num = next(nums, None)

    return new_nums


Range = tuple[int, int]


def process_map2(ranges: list[Range], amap: AlmanacMap) -> list[Range]:
    ranges = iter(sorted(ranges))
    entries = iter(amap.entries)

    new_ranges = []
    range = next(ranges, None)
    entry = next(entries, None)
    while range:
        start, end = range

        if entry is None:
            new_ranges.append(range)
            range = next(ranges, None)
            continue

        e_start, e_end = entry.source, entry.source + entry.range - 1

        # The entry is too small, next
        if start > e_end:
            entry = next(entries, None)
            continue

        # Initial case if the range is below the first entry
        if start < e_start:
            # There's an overlap, keep the last part of the range
            if end >= e_start:
                new_ranges.append((start, e_start - 1))
                range = (e_start, end)
            # No overlap, move to the next range
            else:
                range = next(ranges, None)
                new_ranges.append((start, end))
            continue

        # We can match some of the range
        elif start >= e_start:
            delta = entry.destination - entry.source
            new_start = start + delta

            # We can fit the full range in the entry, move to the next, same entry
            if end <= e_end:
                new_ranges.append((new_start, end + delta))
                range = next(ranges, None)
                continue

            # We have to split the range, and move to the next entry
            else:
                new_ranges.append((new_start, e_end + delta))
                range = (e_end + 1, end)
                entry = next(entries, None)
                continue
        else:
            raise Exception("Shouldn\t happen")

    return new_ranges


def first(input: TextIO) -> int:
    current, maps = parse_all(input.read())

    for map in maps:
        current = process_map(current, map)

    return sorted(current)[0]


def second(input: TextIO) -> int:
    current, maps = parse_all(input.read())
    current = chunk(tuple(current), 2)
    current = [(r[0], r[0] + r[1] - 1) for r in current]

    print("")
    for map in maps:
        # sm = [
        #     f"{e.source},{e.source+e.range-1}->{e.destination},{e.destination + e.range-1}"
        #     for e in map.entries
        # ]
        # print(sorted(current), sm)
        current = process_map2(current, map)

    return sorted(current)[0][0]
