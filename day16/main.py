import collections
import enum
import functools
import itertools
from typing import NamedTuple


class Tile(enum.StrEnum):
    EMPTY_SPACE = "."
    MIRROR_RIGHTWARD = "/"
    MIRROR_LEFTWARD = "\\"
    SPLITTER_HORIZONTAL = "-"
    SPLITTER_VERTICAL = "|"


class Point(NamedTuple):
    y: int
    x: int


class Direction(Point, enum.Enum):
    RIGHT = Point(0, 1)
    LEFT = Point(0, -1)
    UP = Point(-1, 0)
    DOWN = Point(1, 0)


class Grid(NamedTuple):
    height: int
    width: int
    tiles: dict[Point, Tile]


BEAM_DIRECTIONS = {
    # MIRROR_RIGHTWARD
    (Tile.MIRROR_RIGHTWARD, Direction.LEFT): [Direction.DOWN],
    (Tile.MIRROR_RIGHTWARD, Direction.RIGHT): [Direction.UP],
    (Tile.MIRROR_RIGHTWARD, Direction.UP): [Direction.RIGHT],
    (Tile.MIRROR_RIGHTWARD, Direction.DOWN): [Direction.LEFT],
    # MIRROR_LEFTWARD
    (Tile.MIRROR_LEFTWARD, Direction.LEFT): [Direction.UP],
    (Tile.MIRROR_LEFTWARD, Direction.RIGHT): [Direction.DOWN],
    (Tile.MIRROR_LEFTWARD, Direction.UP): [Direction.LEFT],
    (Tile.MIRROR_LEFTWARD, Direction.DOWN): [Direction.RIGHT],
    # SPLITTER_HORIZONTAL
    (Tile.SPLITTER_HORIZONTAL, Direction.UP): [Direction.LEFT, Direction.RIGHT],
    (Tile.SPLITTER_HORIZONTAL, Direction.DOWN): [Direction.LEFT, Direction.RIGHT],
    # SPLITTER_VERTICAL
    (Tile.SPLITTER_VERTICAL, Direction.LEFT): [Direction.UP, Direction.DOWN],
    (Tile.SPLITTER_VERTICAL, Direction.RIGHT): [Direction.UP, Direction.DOWN],
}


@functools.cache
def get_next_points(
    point: Point, from_: tuple[Tile, Direction]
) -> list[tuple[Point, Direction]]:
    return [
        (Point(point.y + direction.y, point.x + direction.x), direction)
        for direction in BEAM_DIRECTIONS.get(from_, [from_[1]])
    ]


def parse_input(input: str) -> Grid:
    rows = input.strip().splitlines()

    return Grid(
        height=len(rows),
        width=len(rows[0]),
        tiles={
            Point(y, x): Tile(col)
            for y, row in enumerate(rows)
            for x, col in enumerate(row)
        },
    )


def solve(tiles: dict[Point, Tile], start: tuple[Point, Direction]) -> int:
    queue = collections.deque([start])

    visited = set()

    while len(queue) > 0:
        item = queue.popleft()

        point, direction = item
        tile = tiles[point]

        visited.add(item)

        for point, direction in get_next_points(point, (tile, direction)):
            next_point = point, direction

            if point in tiles and next_point not in visited:
                queue.append(next_point)

    return len(set(point for point, _ in visited))


def part1(input: str) -> int:
    grid = parse_input(input)

    return solve(grid.tiles, (Point(0, 0), Direction.RIGHT))


def part2(input: str) -> int:
    grid = parse_input(input)

    starts = itertools.chain.from_iterable(
        (
            (Point(0, i), Direction.DOWN),
            (Point(i, 0), Direction.RIGHT),
            (Point(grid.width - 1, i), Direction.UP),
            (Point(i, grid.width - 1), Direction.LEFT),
        )
        for i in range(grid.height)
    )

    return max(map(lambda i: solve(grid.tiles, i), starts))


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
