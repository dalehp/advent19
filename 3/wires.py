from collections import defaultdict
from dataclasses import dataclass
from enum import Enum, auto
from typing import DefaultDict, Iterable, Iterator, List, Set, Tuple


Index = Tuple[int, int]
Wires = Set[int]


class Direction(Enum):
    U = auto()
    L = auto()
    D = auto()
    R = auto()


DIRECTION_MAP = {
    Direction.U: (0, 1),
    Direction.L: (-1, 0),
    Direction.D: (0, -1),
    Direction.R: (1, 0),
}


@dataclass
class WireSegment:
    direction: Direction
    length: int


class WireGrid:
    def __init__(self):
        self.grid: DefaultDict[Index, Wires] = defaultdict(set)

    def add_wire(self, wire: Iterable[WireSegment], wire_id: int):
        x, y = 0, 0
        self.grid[(x, y)].add(wire_id)
        for segment in wire:
            delta = DIRECTION_MAP[segment.direction]
            for i in range(segment.length):
                x, y = x + delta[0], y + delta[1]
                self.grid[(x, y)].add(wire_id)

    def find_closest_crossing(self, wires: Iterable[int]) -> Index:
        # TODO: Find a way to definitely terminate
        i = 1
        wire_set = set(wires)
        while True:
            for index in indices_at_distance(i):
                if self.grid[index] == wire_set:
                    return index
            i += 1


def indices_at_distance(distance: int) -> Set[Index]:
    indices = set()
    for i in range(distance):
        indices.add((i, distance - i))
        indices.add((i, i - distance))
        indices.add((distance - i, i))
        indices.add((distance - i, -i))
        indices.add((-i, distance - i))
        indices.add((-i, i - distance))
        indices.add((i - distance, i))
        indices.add((i - distance, -i))
    return indices


def parse_wire(wire_str: str) -> Iterator[WireSegment]:
    segments = wire_str.split(",")
    for segment in segments:
        d, l = segment[0], segment[1:]
        yield WireSegment(direction=Direction[d], length=int(l))


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = f.readlines()

    wire_strs = [w.strip() for w in lines]
    grid = WireGrid()
    for idx, wire_str in enumerate(wire_strs):
        wire = parse_wire(wire_str)
        grid.add_wire(wire, idx)

    crossing = grid.find_closest_crossing([1, 0])
    print(f"Closest: {crossing}")
    print(f"Distance: {abs(crossing[0]) + abs(crossing[1])}")
