import collections
import functools


def parse_input(input: str) -> list[str]:
    return input.strip().split(",")


def hash(value: str) -> int:
    return functools.reduce(
        lambda current, char: (current + ord(char)) * 17 % 256, value, 0
    )


def part1(input: str) -> int:
    seq = parse_input(input)

    return sum(map(hash, seq))


def part2(input: str) -> int:
    seq = parse_input(input)

    boxes = collections.defaultdict(dict)

    for i in seq:
        if i[-1] == "-":
            v = i[:-1]
            boxes[hash(v)].pop(v, None)
        else:
            v = i[:-2]
            boxes[hash(v)][v] = int(i[-1])

    return sum(
        (box + 1) * slot * focal_length
        for box in boxes
        for slot, focal_length in enumerate(boxes[box].values(), start=1)
    )


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
