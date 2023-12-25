import math

import networkx as nx  # type: ignore


def parse_input(input: str) -> dict[str, list[str]]:
    graph: dict[str, list[str]] = {}

    for line in input.strip().splitlines():
        key, connections = line.split(": ")
        graph[key] = connections.split(" ")

    return graph


def part1(input: str) -> int:
    graph = parse_input(input)

    G = nx.Graph((key, node) for key in graph for node in graph[key])

    G.remove_edges_from(nx.minimum_edge_cut(G))

    return math.prod(map(len, nx.connected_components(G)))


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))


if __name__ == "__main__":
    main()
