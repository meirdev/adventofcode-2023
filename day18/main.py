import re
from typing import Callable, Iterator, TypeAlias

from shapely.geometry import Polygon  # type: ignore


DigPlan: TypeAlias = list[tuple[str, str, str]]
Dig: TypeAlias = tuple[str, int]


def parse_input(input: str) -> DigPlan:
    return re.findall(r"(\w+) (\d+) \(#(\w+)\)", input)


def solution(input: str, func: Callable[[DigPlan], Iterator[Dig]]) -> int:
    dig_plan = parse_input(input)

    points, y, x, perimeter = [(0, 0)], 0, 0, 0

    for direction, meters in func(dig_plan):
        perimeter += meters

        match direction:
            case "R":
                x += meters
            case "D":
                y += meters
            case "U":
                y -= meters
            case "L":
                x -= meters

        points.append((y, x))

    return int(Polygon(points).area + perimeter // 2 + 1)


def part1(input: str) -> int:
    def values(dig_plan: DigPlan) -> Iterator[Dig]:
        for direction, meters, _ in dig_plan:
            yield direction, int(meters)

    return solution(input, values)


def part2(input: str) -> int:
    def values(dig_plan: DigPlan) -> Iterator[Dig]:
        directions = ["R", "D", "L", "U"]
        for _, _, hex in dig_plan:
            yield directions[int(hex[-1])], int(hex[:-1], base=16)

    return solution(input, values)


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
