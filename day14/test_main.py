from .main import part1, part2


INPUT = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""


def test_part1():
    assert part1(INPUT) == 136


def test_part2():
    assert part2(INPUT) == 64


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 107053
    assert part2(input) == 88371
