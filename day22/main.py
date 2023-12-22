import functools
from typing import NamedTuple, TypeAlias


class Coordinate(NamedTuple):
    x: int
    y: int
    z: int


class Brick(NamedTuple):
    start: Coordinate
    end: Coordinate


BrickCubes: TypeAlias = list[Coordinate]


def parse_input(input: str) -> list[Brick]:
    bricks: list[Brick] = []

    for line in input.strip().splitlines():
        bricks.append(
            Brick(*(Coordinate(*map(int, edge.split(","))) for edge in line.split("~")))
        )

    return bricks


def drop_bricks(bricks: list[BrickCubes]) -> tuple[list[BrickCubes], int]:
    final_bricks = []
    final_bricks_set = set()

    falls = 0
    for brick in bricks:
        old_brick = brick

        while True:
            next_brick = [Coordinate(x, y, z - 1) for x, y, z in brick]

            if all(i.z > 0 and i not in final_bricks_set for i in next_brick):
                brick = next_brick
            else:
                break

        final_bricks.append(brick)
        final_bricks_set |= set(brick)

        if brick is not old_brick:
            falls += 1

    return final_bricks, falls


@functools.cache
def solution(input: str) -> list[int]:
    bricks_ = parse_input(input)

    bricks = [
        [
            Coordinate(x, y, z)
            for z in range(min(start.z, end.z), max(start.z, end.z) + 1)
            for y in range(min(start.y, end.y), max(start.y, end.y) + 1)
            for x in range(min(start.x, end.x), max(start.x, end.x) + 1)
        ]
        for start, end in bricks_
    ]

    bricks.sort(key=lambda i: min(j.z for j in i))

    dropped, _ = drop_bricks(bricks)

    return [drop_bricks(dropped[:i] + dropped[i + 1 :])[1] for i in range(len(dropped))]


def part1(input: str) -> int:
    return sum(1 for i in solution(input) if i == 0)


def part2(input: str) -> int:
    return sum(solution(input))


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
