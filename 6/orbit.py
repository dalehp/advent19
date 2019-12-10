from typing import Dict, List, Optional


class Planet:
    def __init__(self, name: str):
        self.name = name
        self.orbiting = None

    def count_orbits(self) -> int:
        orbits = 0
        planet = self
        while planet.orbiting:
            orbits += 1
            planet = planet.orbiting
        return orbits

    def orbits(self) -> List[str]:
        orbits = []
        planet = self
        while planet.orbiting:
            orbits.append(planet.name)
            planet = planet.orbiting
        return orbits

planets: Dict[str, Planet] = {}

def orbital_transfers(a: Planet, b: Planet) -> int:
    a_orbits = a.orbits()
    b_orbits = b.orbits()
    while a_orbits[-1] == b_orbits[-1]:
        a_orbits.pop()
        b_orbits.pop()
    return len(a_orbits) + len(b_orbits)


if __name__ == "__main__":
    with open("input.txt") as f:
        orbits = [line.strip().split(')') for line in f]

    for orbitee, orbiter in orbits:
        orbitee_planet = planets.get(orbitee)
        orbiter_planet = planets.get(orbiter)
        if orbitee_planet is None:
            orbitee_planet = Planet(name=orbitee)
            planets[orbitee] = orbitee_planet
        if orbiter_planet is None:
            orbiter_planet = Planet(name=orbiter)
            planets[orbiter] = orbiter_planet

        orbiter_planet.orbiting = orbitee_planet

    orbit_counts = {name: planet.count_orbits() for name, planet in planets.items()}
    
    print(sum(planet.count_orbits() for planet in planets.values()))

    print(f"Distance from me to santa: {orbital_transfers(planets['SAN'].orbiting, planets['YOU'].orbiting)}")
