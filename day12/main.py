from typing import NamedTuple


class Record(NamedTuple):
    springs: str
    sizes: list[int]


def parse_input(input: str) -> list[Record]:
    records = []

    for line in input.strip().splitlines():
        springs, sizes = line.split(" ")
        sizes_ints = list(map(int, sizes.split(",")))

        records.append(Record(springs, sizes_ints))

    return records


def solution(input: str, times: int) -> int:
    records = parse_input(input)

    sum_ = 0

    for record in records:
        springs = "?".join(record.springs for _ in range(times)) + "."
        sizes = record.sizes * times

        dp = [[None] * len(sizes) for _ in range(len(springs))]

        def inner(i: int, j: int) -> int:
            if j == len(sizes):
                if all(springs[k] != "#" for k in range(i, len(springs))):
                    return 1
                return 0

            if i == len(springs):
                return 0

            if dp[i][j] is not None:
                return dp[i][j]

            count = 0

            if springs[i] != "#":
                count += inner(i + 1, j)

            if (
                i + sizes[j] < len(springs)
                and all(springs[k] != "." for k in range(i, i + sizes[j]))
                and springs[i + sizes[j]] != "#"
            ):
                count += inner(i + sizes[j] + 1, j + 1)

            dp[i][j] = count

            return count

        sum_ += inner(0, 0)

    return sum_


def part1(input: str) -> int:
    return solution(input, 1)


def part2(input: str) -> int:
    return solution(input, 5)


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
