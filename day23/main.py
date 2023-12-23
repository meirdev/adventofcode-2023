import collections
import enum
from typing import Deque, NamedTuple, TypeAlias


class Tile(enum.StrEnum):
    PATH = "."
    FOREST = "#"
    SLOPE_UP = "^"
    SLOPE_DOWN = "v"
    SLOPE_RIGHT = ">"
    SLOPE_LEFT = "<"


Point: TypeAlias = tuple[int, int]


class Map(NamedTuple):
    start: Point
    end: Point
    tiles: dict[Point, Tile]


DIRECTION_OPPOSITE_SLOPE = {
    (0, 1): Tile.SLOPE_LEFT,
    (1, 0): Tile.SLOPE_UP,
    (0, -1): Tile.SLOPE_RIGHT,
    (-1, 0): Tile.SLOPE_DOWN,
}


def parse_input(input: str) -> Map:
    rows = input.strip().splitlines()

    return Map(
        start=(0, 1),
        end=(len(rows) - 1, len(rows[0]) - 2),
        tiles={
            (y, x): Tile(col) for y, row in enumerate(rows) for x, col in enumerate(row)
        },
    )


def solution(input: str, slopes: bool) -> int:
    start, end, tiles = parse_input(input)

    longest_hike = 0

    queue: Deque[tuple[int, Point, set[Point]]] = collections.deque([(0, start, set())])

    while len(queue):
        steps, point, visited = queue.popleft()

        if point == end:
            longest_hike = max(longest_hike, steps)
            continue

        y, x = point

        for dir in DIRECTION_OPPOSITE_SLOPE:
            y_, x_ = dir
            next_point = (y + y_, x + x_)

            if (
                tiles.get(next_point, Tile.FOREST) is not Tile.FOREST
                and next_point not in visited
                and (
                    not slopes or tiles[next_point] is not DIRECTION_OPPOSITE_SLOPE[dir]
                )
            ):
                queue.append((steps + 1, next_point, visited | {next_point}))

    return longest_hike


def part1(input: str) -> int:
    return solution(input, True)


def part2(input: str) -> int:
    return solution(input, False)


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
