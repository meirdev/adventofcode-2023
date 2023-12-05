import itertools
import re
from dataclasses import dataclass
from typing import NamedTuple, Optional

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


@dataclass
class Range:
    start: int
    end: int

    def intersection(self, other: "Range") -> Optional["Range"]:
        if (self.start >= other.start and self.start < other.end) or (
            self.start <= other.start and self.end > other.start
        ):
            return Range(max(self.start, other.start), min(self.end, other.end))
        
        return None

    def intersection_remainder(self, other: "Range") -> tuple[Optional["Range"], list["Range"]]:
        intersection = self.intersection(other)
        if intersection is None:
            return None, [self]

        remainders = []
        if self.start < intersection.start:
            remainders.append(Range(self.start, intersection.start))
        if self.end > intersection.end:
            remainders.append(Range(intersection.end, self.end))
        return intersection, remainders

    def shift(self, n) -> None:
        self.start += n
        self.end += n


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

    min_range: list[Range] = [
        Range(start, start + range_)
        for start, range_ in itertools.batched(almanac.seeds, 2)
    ]

    for label in LABELS:
        unchanged_seeds = min_range
        changed_seeds = []

        for map_ in almanac.maps[label]:
            new_unchanged_seeds = []

            for seed in unchanged_seeds:
                map_range = Range(map_.source, map_.source + map_.range)

                intersection, remainders = seed.intersection_remainder(map_range)
                if intersection:
                    intersection.shift(map_.destination - map_.source)
                    changed_seeds.append(intersection)

                new_unchanged_seeds += remainders

            unchanged_seeds = new_unchanged_seeds

        min_range = unchanged_seeds + changed_seeds

    return min(min_range, key=lambda a: a.start).start


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
