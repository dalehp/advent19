from __future__ import annotations

import math
from dataclasses import dataclass, fields
from itertools import combinations
from typing import List


@dataclass
class Coordinate:
    x: int
    y: int
    z: int

    def __add__(self, o: Coordinate) -> Coordinate:
        return Coordinate(
            *(getattr(self, d.name) + getattr(o, d.name) for d in fields(self))
        )

    def __sub__(self, o: Coordinate) -> Coordinate:
        return Coordinate(
            *(getattr(self, d.name) - getattr(o, d.name) for d in fields(self))
        )


@dataclass
class Moon:
    pos: Coordinate
    v: Coordinate = Coordinate(0, 0, 0)

    def move(self) -> None:
        self.pos += self.v

    def ke(self) -> int:
        return abs(self.pos.x) + abs(self.pos.y) + abs(self.pos.z)
    
    def pe(self) -> int:
        return abs(self.v.x) + abs(self.v.y) + abs(self.v.z)

    def energy(self) -> int:
        return self.ke() * self.pe()


def apply_gravity(a: Moon, b: Moon) -> None:
    diff = _gravity_vector(a.pos, b.pos)
    a.v += diff
    b.v -= diff

def _point_dir(a: int, b: int):
    if a > b:
        return -1
    elif a < b:
        return 1
    else:
        return 0

def _gravity_vector(a: Coordinate, b: Coordinate) -> Coordinate:
    return Coordinate(
        *(
            _point_dir(getattr(a, d.name), getattr(b, d.name))
            for d in fields(Coordinate)
        )
    )

def _parse_moon(moon_str: str) -> Moon:
    coords: List[int] = []
    for coord_str in moon_str[1:-1].split(", "):
        _, _, coord = coord_str.partition("=")
        coords.append(int(coord))
    return Moon(Coordinate(*(coords)))

if __name__ == "__main__":
    moons: List[Moon] = []
    with open("input.txt") as f:
        for line in f:
            moons.append(_parse_moon(line.strip()))
    
    for _ in range(1000):
        for a, b in combinations(moons, 2):
            apply_gravity(a, b)
        for moon in moons:
            moon.move()
    
    print(f"Total energy: {sum(moon.energy() for moon in moons)}")

    moons: List[Moon] = []
    with open("input.txt") as f:
        for line in f:
            moons.append(_parse_moon(line.strip()))

    states_x, states_y, states_z = set(), set(), set()
    x_repeat, y_repeat, z_repeat = None, None, None
    i = 0
    while True:
        
        for a, b in combinations(moons, 2):
            apply_gravity(a, b)
        for moon in moons:
            moon.move()
        state_x = tuple((moon.pos.x, moon.v.x) for moon in moons)
        state_y = tuple((moon.pos.y, moon.v.y) for moon in moons)
        state_z = tuple((moon.pos.z, moon.v.z) for moon in moons)
        
        if not x_repeat and state_x in states_x:
            print("Found x")
            x_repeat = i
        if not y_repeat and state_y in states_y:
            print("Found y")
            y_repeat = i
        if not z_repeat and state_z in states_z:
            print("Found z")
            z_repeat = i
        if x_repeat and y_repeat and z_repeat:
            break

        states_x.add(state_x)
        states_y.add(state_y)
        states_z.add(state_z)

        i += 1

    print(x_repeat, y_repeat, z_repeat)

        
