from __future__ import annotations

from collections import defaultdict
from math import atan2, sqrt
from typing import DefaultDict, List, Set, Tuple



Index = Tuple[int, int]

class Coordinate:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.r = sqrt(x*x + y*y)
        self.theta = atan2(y, x)

    def difference(self, other) -> Coordinate:
        return Coordinate(other.x - self.x, other.y - self.y)


if __name__ == "__main__":
    asteroids: Set[Coordinate] = set()
    with open("input.txt") as f:
        for y, line in enumerate(f):
            for x, ast in enumerate(line):
                if ast == "#":
                    asteroids.add(Coordinate(x, y))

    highest_count = 0
    for asteroid in asteroids:
        angles: DefaultDict[float, Coordinate] = defaultdict(set)
        for other in (asteroids - {asteroid}):
            diff = asteroid.difference(other)
            angles[diff.theta].add(other)
        highest_count = max(highest_count, len(angles))
    print(highest_count)
        
