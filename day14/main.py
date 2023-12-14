import enum
from typing import NamedTuple


class Rocks(NamedTuple):
    size: tuple[int, int]
    rounded: tuple[list[bool], ...]
    cube: tuple[list[bool], ...]


class Direction(enum.IntEnum):
    NORTH = 0
    WEST = 1
    SOUTH = 2
    EAST = 3


def get_direction(direction: Direction) -> tuple[int, int]:
    match direction:
        case Direction.NORTH:
            return (-1, 0)
        case Direction.WEST:
            return (0, -1)
        case Direction.SOUTH:
            return (1, 0)
        case Direction.EAST:
            return (0, 1)


def parse_input(input: str) -> Rocks:
    rows = input.strip().splitlines()

    return Rocks(
        size=(len(rows), len(rows[0])),
        rounded=tuple(list(i == "O" for i in row) for row in rows),
        cube=tuple(list(i == "#" for i in row) for row in rows),
    )


def tilt_rocks(rocks: Rocks, direction: Direction) -> None:
    h, w = rocks.size

    rounded, cube = rocks.rounded, rocks.cube

    y_range = range(h - 1, -1, -1) if direction == Direction.SOUTH else range(h)
    x_range = range(w - 1, -1, -1) if direction == Direction.EAST else range(w)

    y_dir, x_dir = get_direction(direction)

    for y in y_range:
        for x in x_range:
            if rounded[y][x]:
                x_, y_ = x, y

                while (
                    0 <= (x_temp := x_ + x_dir) < w
                    and 0 <= (y_temp := y_ + y_dir) < h
                    and rounded[y_temp][x_temp] == False
                    and cube[y_temp][x_temp] == False
                ):
                    x_ += x_dir
                    y_ += y_dir

                if x != x_ or y != y_:
                    rounded[y][x] = False
                    rounded[y_][x_] = True


def calculate_total_load(rocks: Rocks) -> int:
    h, w = rocks.size

    return sum(h - y for y in range(h) for x in range(w) if rocks.rounded[y][x])


def part1(input: str) -> int:
    rocks = parse_input(input)

    tilt_rocks(rocks, Direction.NORTH)

    return calculate_total_load(rocks)


def part2(input: str) -> int:
    rocks = parse_input(input)

    cache: dict[tuple[tuple[bool, ...], ...], int] = {}

    i = 1_000_000_000
    while 0 < i:
        for dir in Direction:
            tilt_rocks(rocks, dir)

        key = tuple(tuple(row) for row in rocks.rounded)
        if key in cache:
            i %= cache[key] - i
        else:
            cache[key] = i

        i -= 1

    return calculate_total_load(rocks)


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
