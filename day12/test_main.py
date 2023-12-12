from .main import part1, part2


INPUT = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""


def test_part1():
    assert part1(INPUT) == 21


def test_part2():
    assert part2(INPUT) == 525152


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 6981
    assert part2(input) == 4546215031609
