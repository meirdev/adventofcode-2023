import enum
import heapq
from typing import NamedTuple


class Point(NamedTuple):
    y: int
    x: int


class Map(NamedTuple):
    height: int
    width: int
    map: dict[Point, int]


class Direction(Point, enum.Enum):
    UP = Point(-1, 0)
    DOWN = Point(1, 0)
    LEFT = Point(0, -1)
    RIGHT = Point(0, 1)
    NONE = Point(0, 0)


def solution(input: str, min_steps: int, max_steps: int) -> int:
    map_ = parse_input(input)

    target = Point(map_.height - 1, map_.width - 1)

    queue = [(0, Point(0, 0), Direction.NONE)]

    visited: set[tuple[Point, Direction]] = set()

    heat = 0

    while len(queue) > 0:
        heat, pos, dir = heapq.heappop(queue)

        if pos == target:
            break

        if (pos, dir) in visited:
            continue

        visited.add((pos, dir))

        match dir:
            case Direction.UP | Direction.DOWN:
                dirs = [Direction.RIGHT, Direction.LEFT]
            case Direction.RIGHT | Direction.LEFT:
                dirs = [Direction.DOWN, Direction.UP]
            case _:
                dirs = list(Direction)

        for dir_ in dirs:
            heat_ = heat
            for step in range(1, max_steps + 1):
                pos_ = Point(pos.y + (dir_.y * step), pos.x + (dir_.x * step))
                if pos_ in map_.map:
                    heat_ += map_.map[pos_]
                    if step >= min_steps:
                        heapq.heappush(queue, (heat_, pos_, dir_))

    return heat


def parse_input(input: str) -> Map:
    rows = input.strip().splitlines()

    return Map(
        height=len(rows),
        width=len(rows[0]),
        map={
            Point(y, x): int(heat_loss)
            for y, row in enumerate(rows)
            for x, heat_loss in enumerate(row)
        },
    )


def part1(input: str) -> int:
    return solution(input, 1, 3)


def part2(input: str) -> int:
    return solution(input, 4, 10)


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
