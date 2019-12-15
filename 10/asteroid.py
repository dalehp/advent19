from __future__ import annotations

from collections import defaultdict
from math import atan2, sqrt, pi
from typing import DefaultDict, List, Set, Tuple



Index = Tuple[int, int]

class Coordinate:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.r = sqrt(x*x + y*y)
        self.theta = - atan2(y, x) - pi / 2
        if self.theta < 0.0:
            self.theta += 2 * pi

    def difference(self, other) -> Coordinate:
        return Coordinate(other.x - self.x, other.y - self.y)

    def __repr__(self):
        return f"Coordinate(x={self.x}, y={self.y})"


if __name__ == "__main__":
    asteroids: Set[Coordinate] = set()
    with open("test_input.txt") as f:
        for y, line in enumerate(f):
            for x, ast in enumerate(line):
                if ast == "#":
                    asteroids.add(Coordinate(x, y))

    highest_count = 0
    for asteroid in asteroids:
        angles: DefaultDict[float, List[Coordinate]] = defaultdict(list)
        for other in (asteroids - {asteroid}):
            diff = asteroid.difference(other)
            angles[diff.theta].append(diff)

        if len(angles) > highest_count:
            highest_count = len(angles)
            best_angles = angles
            best_coord = asteroid
    print(highest_count)
    print(best_coord)


    for angle, coords in best_angles.items():
        coords.sort(key=lambda x: x.r)
    print()
    print(sorted(best_angles.keys()))
    print(best_angles[0.0])

    destruction_order = []
    while any(coordinates for coordinates in best_angles.values()):
        for angle in sorted(best_angles.keys()):
            if best_angles[angle]:
                destruction_order.append(best_angles[angle].pop(0))
    winner = destruction_order[199]
    print([Coordinate(c.x + best_coord.x, c.y + best_coord.y) for c in destruction_order])
    print(winner.x * 100 + winner.y)