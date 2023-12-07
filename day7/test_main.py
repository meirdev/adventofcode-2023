from .main import part1, part2


INPUT = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""


def test_part1():
    assert part1(INPUT) == 6440


def test_part2():
    assert part2(INPUT) == 5905


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 250370104
    assert part2(input) == 251735672
