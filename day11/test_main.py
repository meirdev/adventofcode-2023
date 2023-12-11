from .main import part1, part2, solution


INPUT = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""


def test_part1():
    assert part1(INPUT) == 374


def test_part2():
    assert solution(INPUT, 10) == 1030
    assert solution(INPUT, 100) == 8410

    assert part2(INPUT) == 82000210


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 10033566
    assert part2(input) == 560822911938
