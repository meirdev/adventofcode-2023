from .main import part1, part2


INPUT = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


def test_part1():
    assert part1(INPUT) == 1320


def test_part2():
    assert part2(INPUT) == 145


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 516657
    assert part2(input) == 210906
