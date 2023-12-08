import enum
import itertools
import math
import re
from typing import Iterator, NamedTuple, TypeAlias


class Instruction(enum.IntEnum):
    LEFT = 0
    RIGHT = 1


NodeId: TypeAlias = str


class Node(NamedTuple):
    id: NodeId
    left: NodeId
    right: NodeId


class Input(NamedTuple):
    instructions: list[Instruction]
    network: dict[NodeId, Node]


def parse_input(input: str) -> Input:
    match = re.search(r"([LR]+)", input)
    if match is None:
        raise ValueError("Missing instructions")

    instructions = [
        Instruction.LEFT if i == "L" else Instruction.RIGHT for i in match.group(0)
    ]

    nodes = re.findall(r"(\w+) = \((\w+), (\w+)\)", input)

    network = {i[0]: Node(*i) for i in nodes}

    return Input(instructions, network)


def iter_nodes(input: Input, node_id: NodeId) -> Iterator[tuple[int, NodeId]]:
    counter = 0
    instruction = itertools.cycle(input.instructions)

    while True:
        node = input.network[node_id]

        if next(instruction) == Instruction.LEFT:
            node_id = node.left
        else:
            node_id = node.right

        counter += 1

        yield counter, node_id


def part1(input: str) -> int:
    input_data = parse_input(input)

    return next(i for i, n in iter_nodes(input_data, "AAA") if n == "ZZZ")


def part2(input: str) -> int:
    input_data = parse_input(input)

    node_ids_a = (i for i in input_data.network if i[-1] == "A")

    counters_z: list[int] = []

    for node_id in node_ids_a:
        node_id_z: dict[NodeId, int] = {}

        for counter, node_id in iter_nodes(input_data, node_id):
            if node_id[-1] == "Z":
                if node_id in node_id_z:
                    counters_z.append(counter - node_id_z[node_id])
                    break
                else:
                    node_id_z[node_id] = counter

    return math.lcm(*counters_z)


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
