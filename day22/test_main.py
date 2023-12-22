from .main import part1, part2


INPUT = """
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""


def test_part1():
    assert part1(INPUT) == 5


def test_part2():
    assert part2(INPUT) == 7


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 441
    assert part2(input) == 80778
