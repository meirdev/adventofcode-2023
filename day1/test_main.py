from .main import part1, part2


def test_part1():
    input = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

    assert part1(input) == 142


def test_part2():
    input = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

    assert part2(input) == 281
