from .main import part1, part2


INPUT = """
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""


def test_part1():
    assert part1(INPUT, 6) == 16


def test_part2():
    pass


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 3503
    assert part2(input) == 584211423220706
