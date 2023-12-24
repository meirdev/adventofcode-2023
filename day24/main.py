import itertools
import sys
from typing import NamedTuple

from z3 import Int, Solver  # type: ignore


class Point(NamedTuple):
    x: float
    y: float


class Position(NamedTuple):
    x: int
    y: int
    z: int


class Velcoity(NamedTuple):
    x: int
    y: int
    z: int


class Hailstone(NamedTuple):
    position: Position
    velcoity: Velcoity


def parse_input(input: str) -> list[Hailstone]:
    hailstones = []

    for line in input.strip().splitlines():
        position, velcoity = line.split("@")
        hailstones.append(
            Hailstone(
                Position(*map(int, position.split(","))),
                Velcoity(*map(int, velcoity.split(","))),
            )
        )

    return hailstones


def find_intersection(a: Hailstone, b: Hailstone) -> Point | None:
    (px1, py1, _), (vx1, vy1, _) = a
    (px2, py2, _), (vx2, vy2, _) = b

    m1 = vy1 / vx1
    m2 = vy2 / vx2

    if abs(m2 - m1) < sys.float_info.epsilon:
        return None

    x = (m1 * px1 - m2 * px2 + py2 - py1) / (m1 - m2)
    y = (m1 * m2 * (px2 - px1) + m2 * py1 - m1 * py2) / (m2 - m1)

    if (vx1 < 0.0 and x > px1) or (vx1 > 0.0 and x < px1):
        return

    if (vx2 < 0.0 and x > px2) or (vx2 > 0.0 and x < px2):
        return

    return Point(x, y)


def part1(input: str, min: float = 2e14, max: float = 4e14) -> int:
    hailstones = parse_input(input)

    return sum(
        1
        for point in itertools.starmap(
            find_intersection, itertools.combinations(hailstones, r=2)
        )
        if point and (min <= point.x <= max and min <= point.y <= max)
    )


def part2(input: str) -> int:
    hailstones = parse_input(input)

    vars = {
        f"{k}{i}": Int(f"{k}{i}")
        for k, v in {
            "P": ("x", "y", "z"),
            "V": ("x", "y", "z"),
            "T": range(len(hailstones)),
        }.items()
        for i in v
    }

    solver = Solver()

    for i, (position, velcoity) in enumerate(hailstones):
        t = vars[f"T{i}"]

        solver.add(vars["Px"] + t * vars["Vx"] - position.x - t * velcoity.x == 0)
        solver.add(vars["Py"] + t * vars["Vy"] - position.y - t * velcoity.y == 0)
        solver.add(vars["Pz"] + t * vars["Vz"] - position.z - t * velcoity.z == 0)

    assert str(solver.check()) == "sat"

    return solver.model().eval(vars["Px"] + vars["Py"] + vars["Pz"])


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
