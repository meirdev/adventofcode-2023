import math
import re
from typing import NamedTuple


class Race(NamedTuple):
    time: int
    distance: int


def parse_input(input: str) -> list[Race]:
    match_time = re.search(r"Time:(.+)", input)
    if match_time is None:
        raise ValueError("Time is missing")

    match_distance = re.search(r"Distance:(.+)", input)
    if match_distance is None:
        raise ValueError("Distance is missing")

    times = re.findall(r"(\d+)", match_time.group(1))
    distances = re.findall(r"(\d+)", match_distance.group(1))

    return [Race(int(time), int(distance)) for time, distance in zip(times, distances)]


def part1(input: str) -> int:
    races = parse_input(input)

    return math.prod(
        sum(i * (race.time - i) > race.distance for i in range(1, race.time))
        for race in races
    )


def part2(input: str) -> int:
    races = parse_input(input)

    time = int("".join(str(race.time) for race in races))
    distance = int("".join(str(race.distance) for race in races))

    a = (-time + math.sqrt(time**2 - 4 * distance)) // -2
    b = (-time - math.sqrt(time**2 - 4 * distance)) // -2

    return int(b - a)


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
