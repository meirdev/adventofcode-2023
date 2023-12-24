from .main import part1, part2


INPUT = """
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""


def test_part1():
    assert part1(INPUT, 7, 27) == 2


def test_part2():
    assert part2(INPUT) == 47


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 18184
    assert part2(input) == 557789988450159
