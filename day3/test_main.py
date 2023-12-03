from .main import part1, part2


INPUT = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""


def test_part1():
    assert part1(INPUT) == 4361


def test_part2():
    assert part2(INPUT) == 467835


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 539590
    assert part2(input) == 80703636
