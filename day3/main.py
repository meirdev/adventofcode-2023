import math
import re
from collections import defaultdict
from typing import DefaultDict, Iterator, NamedTuple


class Number(NamedTuple):
    y: int
    start: int
    end: int
    value: int


class Symbol(NamedTuple):
    y: int
    x: int


def get_value(number: Number) -> int:
    return number.value


def get_numbers_symbols(input: str, pattern: str) -> Iterator[tuple[Number, Symbol]]:
    lines = input.splitlines()

    for y, line in enumerate(lines):
        for match in re.finditer(r"\d+", line):
            start, end = match.span()
            value = int(match.group(0))

            for y_ in range(max(0, y - 1), min(len(lines), y + 2)):
                for x_ in range(max(0, start - 1), min(len(line), end + 1)):
                    if re.fullmatch(pattern, lines[y_][x_]):
                        yield Number(y, start, end, value), Symbol(y_, x_)


def part1(input: str) -> int:
    numbers_symbols = get_numbers_symbols(input, r"[^\d\.]+")

    return sum(map(get_value, set(n for n, _ in numbers_symbols)))


def part2(input: str) -> int:
    symbols_numbers: DefaultDict[Symbol, list[Number]] = defaultdict(list)

    for number, symbol in get_numbers_symbols(input, r"\*"):
        symbols_numbers[symbol].append(number)

    return sum(
        math.prod(map(get_value, n)) for n in symbols_numbers.values() if len(n) == 2
    )


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
