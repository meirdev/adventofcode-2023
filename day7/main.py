import collections
import functools
import enum
import re
from typing import NamedTuple, Type, TypeAlias

Hand: TypeAlias = str


class HandType(enum.IntEnum):
    FIVE_OF_A_KIND = 1
    FOUR_OF_A_KIND = 2
    FULL_HOUSE = 3
    THREE_OF_A_KIND = 4
    TWO_PAIR = 5
    ONE_PAIR = 6
    HIGH_CARD = 7


class Pair(NamedTuple):
    hand: Hand
    bid: int


CardPart1 = enum.IntEnum(
    "CardPart1", ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
)

CardPart2 = enum.IntEnum(
    "CardPart1", ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
)


@functools.cache
def get_hand_strength(
    hand: Hand, box: Type[enum.IntEnum]
) -> tuple[HandType, tuple[int, ...]]:
    cards = collections.Counter(hand)

    if box is CardPart2:
        if jokers := cards.pop("J", 0):
            if len(cards) == 0:
                cards["J"] = jokers
            else:
                cards[cards.most_common(1)[0][0]] += jokers

    match sorted(cards.values(), reverse=True):
        case [5]:
            hand_type = HandType.FIVE_OF_A_KIND
        case [4, 1]:
            hand_type = HandType.FOUR_OF_A_KIND
        case [3, 2]:
            hand_type = HandType.FULL_HOUSE
        case [3, 1, 1]:
            hand_type = HandType.THREE_OF_A_KIND
        case [2, 2, 1]:
            hand_type = HandType.TWO_PAIR
        case [2, 1, 1, 1]:
            hand_type = HandType.ONE_PAIR
        case _:  # [1, 1, 1, 1, 1]
            hand_type = HandType.HIGH_CARD

    return hand_type, tuple(getattr(box, i) for i in hand)


def parse_input(input: str) -> list[Pair]:
    return [Pair(hand, int(bid)) for hand, bid in re.findall(r"(\w+) (\d+)", input)]


def solution(input: str, box: Type[enum.IntEnum]) -> int:
    pairs = parse_input(input)

    def key(pair: Pair):
        return get_hand_strength(pair.hand, box)

    return sum(
        i * pair.bid
        for i, pair in enumerate(sorted(pairs, key=key, reverse=True), start=1)
    )


def part1(input: str) -> int:
    return solution(input, CardPart1)


def part2(input: str) -> int:
    return solution(input, CardPart2)


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
