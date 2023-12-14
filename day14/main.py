import enum
from typing import TypeAlias


class Type(enum.StrEnum):
    EMPTY = "."
    ROUNDED = "O"
    CUBE = "#"


Platform: TypeAlias = dict[int, dict[int, Type]]


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


def parse_input(input: str) -> Platform:
    rows = input.strip().splitlines()

    return {
        y: {x: Type(col) for x, col in enumerate(row)} for y, row in enumerate(rows)
    }


def tilt_platform(platform: Platform, direction: Direction) -> None:
    h, w = len(platform), len(platform[0])

    y_range = range(h - 1, -1, -1) if direction == Direction.SOUTH else range(h)
    x_range = range(w - 1, -1, -1) if direction == Direction.EAST else range(w)

    y_dir, x_dir = get_direction(direction)

    for y in y_range:
        for x in x_range:
            if platform[y][x] == Type.ROUNDED:
                x_, y_ = x, y

                while (
                    platform.get(y_ + y_dir, {}).get(x_ + x_dir, Type.CUBE)
                    == Type.EMPTY
                ):
                    x_ += x_dir
                    y_ += y_dir

                if x != x_ or y != y_:
                    platform[y][x] = Type.EMPTY
                    platform[y_][x_] = Type.ROUNDED


def calculate_total_load(platform: Platform) -> int:
    h = len(platform)

    return sum(
        h - y for y in platform for x in platform[y] if platform[y][x] == Type.ROUNDED
    )


def print_platform(platform: Platform) -> None:
    for row in platform.values():
        print("".join(row.values()))
    print()


def part1(input: str) -> int:
    platform = parse_input(input)

    tilt_platform(platform, Direction.NORTH)

    return calculate_total_load(platform)


def part2(input: str) -> int:
    platform = parse_input(input)

    cache: dict[tuple[tuple[int, int, Type], ...], int] = {}

    i = 1_000_000_000
    while 0 < i:
        for dir in Direction:
            tilt_platform(platform, dir)

        key = tuple((y, x, platform[y][x]) for y in platform for x in platform[y])
        if key in cache:
            i %= cache[key] - i
        else:
            cache[key] = i

        i -= 1

    return calculate_total_load(platform)


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
