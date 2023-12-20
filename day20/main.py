import collections
import dataclasses
import enum
import math
from typing import Deque


class Pulse(enum.IntEnum):
    LOW = 0
    HIGH = 1


class ModuleType(enum.IntEnum):
    EMPTY = 0
    BROADCASTER = 1
    FLIP_FLOP = 2
    CONJUNCTION = 3


@dataclasses.dataclass
class Module:
    name: str
    type: ModuleType
    destinations: list[str] = dataclasses.field(default_factory=list)
    state: bool = False
    inputs: dict[str, bool] = dataclasses.field(default_factory=dict)


def parse_input(input: str) -> dict[str, Module]:
    modules: dict[str, Module] = {}

    all_modules: set[str] = set()

    for line in input.strip().splitlines():
        from_, to = line.split(" -> ")

        destinations = to.split(", ")

        if from_.startswith("broadcaster"):
            name, type_ = "broadcaster", ModuleType.BROADCASTER
        elif from_.startswith("%"):
            name, type_ = from_[1:], ModuleType.FLIP_FLOP
        elif from_.startswith("&"):
            name, type_ = from_[1:], ModuleType.CONJUNCTION
        else:
            raise ValueError

        modules[name] = Module(name, type_, destinations)

        all_modules.add(name)
        all_modules.update(destinations)

    for module in all_modules - set(modules):
        modules[module] = Module(module, ModuleType.EMPTY)

    for module in modules.values():
        for destination in module.destinations:
            modules[destination].inputs[module.name] = False

    return modules


def solution(input: str, part: int) -> int:
    modules = parse_input(input)

    # part 1
    counter = {Pulse.LOW: 0, Pulse.HIGH: 0}
    i = 0

    if part == 2:
        parent = next(iter(modules["rx"].inputs))
        listen = {n: None for n in modules[parent].inputs}
        condition = lambda: None in listen.values()
    else:
        parent = None
        listen = {}
        condition = lambda: i < 1000

    button_presses = 0  # part2

    queue: Deque[tuple[str, str, Pulse]] = collections.deque()

    while condition():
        queue.append(("button", "broadcaster", Pulse.LOW))

        button_presses += 1  # part2

        while len(queue) > 0:
            source, name, pulse = queue.popleft()

            counter[pulse] += 1  # part1

            module = modules[name]

            if module.type is ModuleType.FLIP_FLOP:
                if pulse is Pulse.HIGH:
                    continue
                module.state = not module.state

            elif module.type is ModuleType.CONJUNCTION:
                module.inputs[source] = pulse
                module.state = not all(module.inputs.values())

                # part2
                if name == parent:
                    for k in filter(
                        lambda i: (i, listen[i], pulse) == (source, None, Pulse.HIGH),
                        listen,
                    ):
                        listen[k] = button_presses

            for destination in module.destinations:
                queue.append((name, destination, Pulse(module.state)))

        i += 1  # part1

    if part == 2:
        return math.prod(listen.values())
    else:
        return counter[Pulse.HIGH] * counter[Pulse.LOW]


def part1(input: str) -> int:
    return solution(input, 1)


def part2(input: str) -> int:
    return solution(input, 2)


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
