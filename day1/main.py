import re


DIGITS = {
    word: str(num)
    for num, word in enumerate(
        ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"],
        start=1,
    )
}


def find_number(line: str, digits: list[str]) -> int:
    nums = []
    for d in digits:
        nums += [(m.start(0), DIGITS.get(d, d)) for m in re.finditer(d, line)]

    _, min_num = min(nums, key=lambda i: i[0])
    _, max_num = max(nums, key=lambda i: i[0])

    return int(min_num + max_num)


def solution(input: str, digits: list[str]) -> int:
    return sum(map(lambda line: find_number(line, digits), input.splitlines()))


def part1(input: str) -> int:
    return solution(input, [*DIGITS.values()])


def part2(input: str) -> int:
    return solution(input, [*DIGITS.keys(), *DIGITS.values()])


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
