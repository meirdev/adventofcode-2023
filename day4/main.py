import re
import functools
from dataclasses import dataclass


@dataclass
class Card:
    id: int
    winning_numbers: list[str]
    numbers: list[str]

    @functools.cached_property
    def wins(self) -> int:
        return len(set(self.winning_numbers) & set(self.numbers))


def parse_input(input: str) -> list[Card]:
    cards: list[Card] = []

    for line in input.splitlines():
        match = re.match(r"Card\s+(?P<id>\d+): (?P<numbers>.+)", line)
        if match:
            numbers = match.group("numbers").split("|")

            cards.append(
                Card(
                    id=int(match.group("id")),
                    winning_numbers=re.findall(r"\d+", numbers[0]),
                    numbers=re.findall(r"\d+", numbers[1]),
                )
            )

    return cards


def part1(input: str) -> int:
    cards = parse_input(input)

    return sum(2 ** (card.wins - 1) for card in cards if card.wins > 0)


def part2(input: str) -> int:
    cards: dict[int, int] = {card.id: card.wins for card in parse_input(input)}

    instances = [1] * len(cards)
    for i in range(len(instances)):
        for j in range(i + 1, min(i + 1 + cards[i + 1], len(instances))):
            instances[j] += instances[i]

    return sum(instances)


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
