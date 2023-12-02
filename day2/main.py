import math
import re
from typing import Literal, TypedDict


Record = dict[Literal["blue", "red", "green"], int]


class Game(TypedDict):
    id: int
    records: list[Record]


def parse_record(s: str) -> Record:
    record = {}

    for cubes, color in re.findall(r"(?P<cubes>\d+) (?P<color>\w+)", s):
        record[color] = int(cubes)

    return record


def parse_game(s: str) -> Game:
    match = re.match(r"Game (?P<id>\d+): (?P<records>.+)", s)
    if match is None:
        raise ValueError("Invalid game")

    return {
        "id": int(match.group("id")),
        "records": list(map(parse_record, match.group("records").split(";"))),
    }


def parse_input(s: str) -> list[Game]:
    return list(map(parse_game, s.splitlines()))


def part1(input: str) -> int:
    games = parse_input(input)

    return sum(
        game["id"]
        for game in games
        if all(
            record.get("red", 0) <= 12
            and record.get("green", 0) <= 13
            and record.get("blue", 0) <= 14
            for record in game["records"]
        )
    )


def part2(input: str) -> int:
    games = parse_input(input)

    sum_power = 0

    for game in games:
        max_record: Record = {}

        for record in game["records"]:
            for color in record:
                max_record[color] = max(
                    max_record.get(color, record[color]), record[color]
                )

        sum_power += math.prod(max_record.values())

    return sum_power


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
