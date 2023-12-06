from .main import part1, part2


INPUT = """Time:      7  15   30
Distance:  9  40  200
"""


def test_part1():
    assert part1(INPUT) == 288


def test_part2():
    assert part2(INPUT) == 71503


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 4811940
    assert part2(input) == 30077773
