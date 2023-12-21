import collections
import enum
import functools
from typing import DefaultDict, Iterable, NamedTuple, TypeAlias


class Type(enum.StrEnum):
    GARDEN_PLOT = "."
    ROCK = "#"


Point: TypeAlias = tuple[int, int]  # y, x


class Points(collections.UserDict[Point, Type]):
    def get_or_none(self, key: Point) -> Type | None:
        y, x = key
        return super().get((y % self.height, x % self.width))

    @functools.cached_property
    def height(self) -> int:
        return max(y for y, _ in self.data) + 1

    @functools.cached_property
    def width(self) -> int:
        return max(x for _, x in self.data) + 1


class Map(NamedTuple):
    points: Points
    start: Point


def parse_input(input: str) -> Map:
    points = Points()

    start = (-1, -1)

    for y, row in enumerate(input.strip().splitlines()):
        for x, col in enumerate(row):
            if col == "S":
                start = (y, x)
                col = "."

            points[(y, x)] = Type(col)

    return Map(
        points=points,
        start=start,
    )


def bfs(points: Points, start: Point, steps_to_walk: int) -> Iterable[int]:
    queue = collections.deque([(steps_to_walk, start)])

    visited: DefaultDict[Point, int] = collections.defaultdict(int)

    while len(queue):
        steps, point = queue.popleft()

        y, x = point

        for next_point in ((y + 1, x), (y, x + 1), (y - 1, x), (y, x - 1)):
            if points.get_or_none(next_point) == Type.GARDEN_PLOT:
                if next_point not in visited and steps - 1 >= 0:
                    queue.append((steps - 1, next_point))
                    visited[next_point] = visited[point] + 1

    return visited.values()


def part1(input: str, steps: int = 64) -> int:
    return sum(i % 2 == 0 for i in bfs(*parse_input(input), steps))


def part2(input: str, steps: int = 26501365) -> int:
    points, start = parse_input(input)

    p0, p1, p2 = [
        sum((j + i % 2) % 2 == 0 for j in bfs(points, start, i))
        for i in range(points.height * 3)
        if i % points.height == points.height // 2
    ]

    n = steps // points.height

    return int(p0 + n * (p1 - p0) + n * (n - 1) / 2 * ((p2 - p1) - (p1 - p0)))


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
