from .main import part1, part2


INPUT1 = """
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""

INPUT2 = """
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""


def test_part1():
    assert part1(INPUT1) == 32000000
    assert part1(INPUT2) == 11687500


def test_part2():
    pass


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 818649769
    assert part2(input) == 246313604784977
