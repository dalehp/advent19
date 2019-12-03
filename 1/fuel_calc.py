def fuel_required(mass: int) -> int:
    print(mass)
    fuel = (mass // 3) - 2
    if fuel < 0:
        return 0

    delta_fuel = fuel_required(fuel)
    if delta_fuel > 0:
        fuel += delta_fuel

    return fuel
    


if __name__ == "__main__":
    fuel = 0
    with open('input.txt') as f:
        for mass in f:
            fuel += fuel_required(int(mass))

    print(f"Total fuel requirement: {fuel}")
