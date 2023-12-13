import enum
from typing import Callable, Iterator, NamedTuple, TypeAlias


class Char(enum.StrEnum):
    ASH = "."
    ROCK = "#"
    ALL = "*"


Pattern: TypeAlias = list[list[Char]]


class Line(enum.IntEnum):
    HORIZONTAL = 100
    VERTICAL = 1


class Smudge(NamedTuple):
    row_a: int
    row_b: int
    column: int


def parse_input(input: str) -> list[Pattern]:
    patterns: list[Pattern] = []

    pattern: Pattern = []
    for line in input.strip().splitlines():
        if line == "":
            patterns.append(pattern)
            pattern = []
        else:
            pattern.append(list(map(Char, line)))

    patterns.append(pattern)

    return patterns


def print_pattern(pattern: Pattern) -> None:
    print("\n".join("".join(row) for row in pattern))


def rotate_pattern(pattern: Pattern) -> Pattern:
    return list(map(list, zip(*pattern)))


def find_reflection(pattern: Pattern, start: int = -1, end: int = -1) -> int:
    start = 1 if start == -1 else start
    end = len(pattern) if end == -1 else end

    for i in range(start, end):
        j = 0
        while (
            i - j - 1 >= 0
            and i + j < len(pattern)
            and pattern[i - j - 1] == pattern[i + j]
        ):
            j += 1

        if j > 0 and (i - j - 1 < 0 or i + j == len(pattern)):
            return i

    return -1


def find_all_smudge(pattern: Pattern) -> Iterator[Smudge]:
    height = len(pattern)
    width = len(pattern[0])

    for i in range(height):
        for j in range(i + 1, height):
            diff = [
                Smudge(i, j, k) for k in range(width) if pattern[i][k] != pattern[j][k]
            ]

            if len(diff) == 1:
                yield diff[0]


def solution(
    input: str,
    function: Callable[[Pattern], Iterator[tuple[Pattern, int, int]]],
) -> int:
    patterns = parse_input(input)

    return sum(
        idx * line
        for pattern in patterns
        for line, pattern_ in zip(Line, (pattern, rotate_pattern(pattern)))
        for pattern_, i, j in function(pattern_)
        if (idx := find_reflection(pattern_, i, j)) != -1
    )


def part1(input: str) -> int:
    def inner(pattern) -> Iterator[tuple[Pattern, int, int]]:
        yield from ((pattern, -1, -1),)

    return solution(input, inner)


def part2(input: str) -> int:
    def inner(pattern) -> Iterator[tuple[Pattern, int, int]]:
        for smudge in find_all_smudge(pattern):
            i, j, k = smudge

            temp = pattern[i][k], pattern[j][k]

            pattern[i][k], pattern[j][k] = Char.ALL, Char.ALL
            yield pattern, i + 1, j + 1
            pattern[i][k], pattern[j][k] = temp

    return solution(input, inner)


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
