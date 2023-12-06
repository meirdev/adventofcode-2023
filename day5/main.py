import itertools
import re
from typing import NamedTuple

from ranges import Range, RangeSet

LABELS: list[str] = [
    "seed-to-soil",
    "soil-to-fertilizer",
    "fertilizer-to-water",
    "water-to-light",
    "light-to-temperature",
    "temperature-to-humidity",
    "humidity-to-location",
]


class Map(NamedTuple):
    destination: int
    source: int
    range: int


class Almanac(NamedTuple):
    seeds: list[int]
    maps: dict[str, list[Map]]


def parse_input(input: str) -> Almanac:
    label_numbers: dict[str, list[list[int]]] = {}

    label = ""

    for line in input.splitlines():
        if match := re.match(r"([a-z-]+)", line):
            label = match.group(1)
            label_numbers[label] = []

        if numbers := re.findall(r"\d+", line):
            label_numbers[label].append(list(map(int, numbers)))

    seeds = label_numbers.pop("seeds")

    maps = {}
    for label, numbers in label_numbers.items():
        maps[label] = [Map(*i) for i in numbers]

    return Almanac(seeds[0], maps)


def part1(input: str) -> int:
    almanac = parse_input(input)

    min_idx = float("inf")

    for n in almanac.seeds:
        idx = n
        for label in LABELS:
            for map_ in almanac.maps[label]:
                if map_.source <= idx < map_.source + map_.range:
                    idx = idx - map_.source + map_.destination
                    break

        min_idx = min(min_idx, idx)

    return min_idx


def part2(input: str) -> int:
    almanac = parse_input(input)

    seeds = RangeSet(
        Range(start, start + range_)
        for start, range_ in itertools.batched(almanac.seeds, 2)
    )

    for label in LABELS:
        changed_seeds: list[Range] = []

        for entry in almanac.maps[label]:
            entry_range = Range(entry.source, entry.source + entry.range)
            diff = entry.destination - entry.source

            def shift(range_: "Range") -> "Range":
                range_.start += diff
                range_.end += diff
                return range_

            changed_seeds += map(shift, seeds & entry_range)
            seeds -= entry_range

        seeds += changed_seeds

    return min(i.start for i in seeds)


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
