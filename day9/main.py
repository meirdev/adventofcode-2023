import functools
import re
from typing import Callable, TypeAlias


ListInts: TypeAlias = list[int]

LineHistory: TypeAlias = list[ListInts]


def parse_input(input: str) -> list[ListInts]:
    lines: list[ListInts] = []

    for line in input.splitlines():
        if line:
            lines.append(list(map(int, re.findall(r"(-?\d+)", line))))

    return lines


def solution(input: str, sum_function: Callable[[LineHistory], int]) -> int:
    lines = parse_input(input)

    sum_ = 0

    for line in lines:
        line_history = [line]

        while sum(line) != 0:
            line_history.append([line[i] - line[i - 1] for i in range(1, len(line))])
            line = line_history[-1]

        sum_ += sum_function(line_history)

    return sum_


def part1(input: str) -> int:
    return solution(
        input,
        lambda line_history: sum(list_ints[-1] for list_ints in line_history),
    )


def part2(input: str) -> int:
    return solution(
        input,
        lambda list_history: functools.reduce(
            lambda k, i: list_history[i][0] - k,
            range(len(list_history) - 2, -1, -1),
            0,
        ),
    )


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
