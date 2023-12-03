import math
import re
from collections import defaultdict
from typing import DefaultDict, NamedTuple


class Node(NamedTuple):
    y: int
    x: int
    value: int | str


def get_graph(input: str, pattern: re.Pattern[str]) -> DefaultDict[Node, list[Node]]:
    graph: DefaultDict[Node, list[Node]] = defaultdict(list)

    lines = input.splitlines()

    for y, line in enumerate(lines):
        for match in re.finditer(r"\d+", line):
            start, end = match.span()
            value = int(match.group(0))

            number = Node(y, start, value)

            for y_ in range(max(0, y - 1), min(len(lines), y + 2)):
                for x_ in range(max(0, start - 1), min(len(line), end + 1)):
                    if pattern.fullmatch(lines[y_][x_]):
                        symbol = Node(y_, x_, lines[y_][x_])

                        graph[number].append(symbol)
                        graph[symbol].append(number)

    return graph


def part1(input: str) -> int:
    graph = get_graph(input, re.compile(r"[^\d.]+"))

    return sum(i.value for i in graph if isinstance(i.value, int))


def part2(input: str) -> int:
    graph = get_graph(input, re.compile(r"\*"))

    return sum(
        math.prod(int(n.value) for n in graph[i])
        for i in graph
        if isinstance(i.value, str) and len(graph[i]) == 2
    )


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
