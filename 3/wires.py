from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import DefaultDict, Dict, Iterable, Iterator, List, Set, Tuple


Index = Tuple[int, int]
WireNum = int
Distance = int
Wires = Dict[WireNum, Distance]


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
        self.grid: DefaultDict[Index, Wires] = defaultdict(dict)

    def add_wire(self, wire: Iterable[WireSegment], wire_id: int):
        x, y = 0, 0
        length = 0
        self.grid[(x, y)][wire_id] = length
        for segment in wire:
            delta = DIRECTION_MAP[segment.direction]
            for i in range(segment.length):
                length += 1
                x, y = x + delta[0], y + delta[1]
                wires = self.grid[(x, y)]
                if wire_id in wires:
                    wires[wire_id] = min(wires[wire_id], length)
                else:
                    wires[wire_id] = length

    def find_closest_crossing_manhattan(
        self, wire_ids: Iterable[int]
    ) -> Tuple[Index, int]:
        wire_set = set(wire_ids)
        crossings = [
            idx
            for idx, wires in self.grid.items()
            if set(wires.keys()) == wire_set and idx != (0, 0)
        ]
        closest_pt = min(crossings, key=lambda x: abs(x[0]) + abs(x[1]))
        distance = abs(closest_pt[0]) + abs(closest_pt[1])
        return closest_pt, distance

    def find_closest_crossing_wire_distance(
        self, wire_ids: Iterable[int]
    ) -> Tuple[Index, int]:
        def _wire_distance(wires: Wires, wire_ids: Iterable[int]) -> int:
            return sum(wires[wire_id] for wire_id in wire_ids)

        wire_set = set(wire_ids)
        crossings = [
            (idx, wires)
            for idx, wires in self.grid.items()
            if set(wires.keys()) == wire_set and idx != (0, 0)
        ]
        closest_pt, closest_wires = min(
            crossings, key=lambda x: _wire_distance(x[1], wire_ids)
        )
        distance = _wire_distance(closest_wires, wire_ids)
        return closest_pt, distance


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
    now = datetime.now()
    crossing, distance = grid.find_closest_crossing_manhattan([0, 1])
    crossing, distance = grid.find_closest_crossing_wire_distance([0, 1])
    print(f"Time taken: {datetime.now() - now}")
    print(f"Closest: {crossing}")
    print(f"Distance: {distance}")
