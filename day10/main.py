import enum
from typing import NamedTuple, TypeAlias

import matplotlib.path as mpl_path


class Connection(enum.IntEnum):
    NONE = 0b0000
    NORTH = 0b0001
    SOUTH = 0b0010
    EAST = 0b0100
    WEST = 0b1000
    ALL = 0b1111


Point: TypeAlias = tuple[int, int]


class Grid(NamedTuple):
    start: Point
    tiles: dict[Point, int]


def parse_input(input: str) -> Grid:
    tiles = {}

    start = (-1, -1)

    for y, line in enumerate(input.strip("\n\r").splitlines()):
        for x, pipe in enumerate(line):
            tile: int

            match pipe:
                case "S":
                    start = (y, x)
                    tile = Connection.ALL
                case "|":
                    tile = Connection.NORTH | Connection.SOUTH
                case "-":
                    tile = Connection.EAST | Connection.WEST
                case "L":
                    tile = Connection.NORTH | Connection.EAST
                case "J":
                    tile = Connection.NORTH | Connection.WEST
                case "7":
                    tile = Connection.SOUTH | Connection.WEST
                case "F":
                    tile = Connection.SOUTH | Connection.EAST
                case _:
                    tile = Connection.NONE

            tiles[(y, x)] = tile

    if start == (-1, -1):
        raise ValueError("Missing start point")

    return Grid(start, tiles)


def get_loop(grid: Grid) -> list[Point]:
    points: list[Point] = [grid.start]

    point, prev_point = grid.start, None

    while grid.start != point or prev_point is None:
        y, x = point

        for current_conn, next_conn, next_point in (
            (Connection.NORTH, Connection.SOUTH, (y - 1, x)),
            (Connection.SOUTH, Connection.NORTH, (y + 1, x)),
            (Connection.WEST, Connection.EAST, (y, x - 1)),
            (Connection.EAST, Connection.WEST, (y, x + 1)),
        ):
            if (
                prev_point != next_point
                and grid.tiles.get(point, 0) & current_conn
                and grid.tiles.get(next_point, 0) & next_conn
            ):
                point, prev_point = next_point, point
                break

        points.append(point)

    return points


def part1(input: str) -> int:
    grid = parse_input(input)

    points = get_loop(grid)

    return len(points) // 2


def part2(input: str) -> int:
    grid = parse_input(input)

    points = get_loop(grid)

    polygon = mpl_path.Path(points)

    return sum(
        1
        for point in grid.tiles
        if point not in points and polygon.contains_point(point)
    )


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
