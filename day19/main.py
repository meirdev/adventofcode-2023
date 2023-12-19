import enum
import math
import re
from typing import NamedTuple, TypeAlias


CATEGORIES = ["x", "m", "a", "s"]


Part: TypeAlias = dict[str, int]


class Op(enum.IntEnum):
    LT = 0
    GT = 1


class Condition(NamedTuple):
    category: str
    op: Op


class System(NamedTuple):
    parts: list[Part]
    workflows: dict[str, list[tuple[Condition | None, int, str]]]


def parse_input(input: str) -> System:
    parts = []
    workflows = {}

    for line in input.strip().splitlines():
        match = re.match(r"(\w+)?\{(.*?)\}", line)

        if not match:
            continue

        name = match.group(1)
        items = match.group(2).split(",")

        if name is None:
            categories = {}

            for item in items:
                category, value = item.split("=")
                categories[category] = int(value)

            parts.append(categories)

        else:
            rules = []

            for rule in items:
                if ":" in rule:
                    condition, target = rule.split(":")
                    if ">" in condition:
                        category, value = condition.split(">")
                        condition, value = Condition(category, Op.GT), int(value)
                    else:
                        category, value = condition.split("<")
                        condition, value = Condition(category, Op.LT), int(value)
                else:
                    target = rule
                    condition, value = None, 0

                rules.append((condition, value, target))

            workflows[name] = rules

    return System(parts, workflows)


def part1(input: str) -> int:
    system = parse_input(input)

    def cmp(condition: Condition | None, value: int, part: Part) -> bool:
        if condition is None:
            return True

        if condition.op == Op.GT:
            return part[condition.category] > value
        else:
            return part[condition.category] < value

    sum_ = 0

    for part in system.parts:
        loop = True
        workflow = "in"

        while loop:
            for condition, value, target in system.workflows[workflow]:
                if cmp(condition, value, part):
                    match target:
                        case "A":
                            sum_ += sum(part.values())
                            loop = False
                        case "R":
                            loop = False
                        case _:
                            workflow = target
                    break

    return sum_


def part2(input: str) -> int:
    system = parse_input(input)

    def inner(workflow: str, conditions: dict[Condition, int]) -> int:
        if workflow == "R":
            return 0

        if workflow == "A":
            return math.prod(
                max(
                    0,
                    conditions[Condition(i, Op.LT)]
                    - conditions[Condition(i, Op.GT)]
                    - 1,
                )
                for i in CATEGORIES
            )

        result = 0
        for condition, value, target in system.workflows[workflow]:
            if condition:
                category, op = condition

                if op == Op.GT:
                    value = max(value, conditions[condition])
                else:
                    value = min(value, conditions[condition])

                result += inner(target, conditions | {condition: value})

                if op == Op.LT:
                    value -= 1
                    op = Op.GT
                else:
                    value += 1
                    op = Op.LT

                conditions[Condition(category, op)] = value
            else:
                result += inner(target, conditions)

        return result

    conditions = {}

    for i in CATEGORIES:
        conditions[Condition(i, Op.GT)] = 0
        conditions[Condition(i, Op.LT)] = 4001

    return inner("in", conditions)


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
