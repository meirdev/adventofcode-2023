from .main import part1, part2


INPUT = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""


def test_part1():
    assert part1(INPUT) == 114


def test_part2():
    assert part2(INPUT) == 2


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 1930746032
    assert part2(input) == 1154
