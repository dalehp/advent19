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
        # Y direction is down so negate y
        self.theta = atan2(-y, x)
        # Transform theta to match problem - starting up and clockwise rather than a/c
        self.theta = - self.theta + pi / 2
        if self.theta < 0.0:
            self.theta += 2 * pi

    def difference(self, other) -> Coordinate:
        return Coordinate(other.x - self.x, other.y - self.y)

    def __add__(self, o: Coordinate) -> Coordinate:
        return Coordinate(self.x + o.x, self.y + o.y)

    def __repr__(self):
        return f"Coordinate(x={self.x}, y={self.y})"


if __name__ == "__main__":
    asteroids: Set[Coordinate] = set()
    with open("input.txt") as f:
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
        coords.sort(key=lambda x: x.r, reverse=True)

    destruction_order = []
    while any(coordinates for coordinates in best_angles.values()):
        for angle in sorted(best_angles.keys()):
            if best_angles[angle]:
                destruction_order.append(best_angles[angle].pop())
    winner = destruction_order[199] + best_coord
    print([c + best_coord for c in destruction_order])
    print(winner.x * 100 + winner.y)
