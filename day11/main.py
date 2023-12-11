import itertools
from typing import NamedTuple, TypeAlias

Position: TypeAlias = list[int]  # x, y


class Cosmos(NamedTuple):
    space: list[str]
    galaxies: list[Position]


def parse_input(input: str) -> Cosmos:
    space = input.strip().splitlines()

    galaxies = [
        [y, x]
        for y in range(len(space))
        for x in range(len(space[y]))
        if space[y][x] == "#"
    ]

    return Cosmos(space, galaxies)


def expend_galaxies(cosmos: Cosmos, expansion: int) -> list[Position]:
    space = cosmos.space

    rows = [y for y in range(len(space)) if "#" not in space[y]]
    columns = [x for x, col in enumerate(zip(*space)) if "#" not in col]

    galaxies, expansion = cosmos.galaxies[:], expansion - 1

    for idx, dim in enumerate((rows, columns)):
        for i, e in zip(dim, itertools.count(0, expansion)):
            for galaxy in galaxies:
                if galaxy[idx] > i + e:
                    galaxy[idx] += expansion

    return galaxies


def solution(input: str, expansion: int) -> int:
    space = parse_input(input)

    galaxies = expend_galaxies(space, expansion)

    return sum(
        abs(y1 - y2) + abs(x1 - x2)
        for (y1, x1), (y2, x2) in itertools.combinations(galaxies, 2)
    )


def part1(input: str) -> int:
    return solution(input, 2)


def part2(input: str) -> int:
    return solution(input, 1_000_000)


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
