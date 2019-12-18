import math
from collections import defaultdict
from dataclasses import dataclass
from typing import DefaultDict, Dict, List, Tuple


Chemicals = DefaultDict[str, int]
Chemical = Tuple[str, int]


@dataclass
class Reaction:
    ingredients: Chemicals
    result: Chemical


def parse_chemical(chemical_str: str) -> Tuple[int, str]:
    quantity_str, chemical = chemical_str.split(" ")
    return (int(quantity_str), chemical)


def parse_reaction(reaction_str: str) -> Tuple[str, Reaction]:
    ingredients_str, _, result_str = reaction_str.partition(" => ")
    ingredients: Chemicals = defaultdict(int)
    for ingredient_str in ingredients_str.split(", "):
        ing_quantity, ingredient = parse_chemical(ingredient_str)
        ingredients[ingredient] = ing_quantity
    res_quantity, result_chem = parse_chemical(result_str)
    return (
        result_chem,
        Reaction(ingredients=ingredients, result=(result_chem, res_quantity)),
    )

def react(chemicals: Chemicals, chemical: str, reactions: Dict[str, Reaction]):
    qty = chemicals[chemical]
    needed = reactions[chemical].result[1]
    changed = False
    if qty >= needed:
        changed = True
        num_reactions = qty // needed
        chemicals[chemical] -= needed * num_reactions
        for ingredient, i_qty in reactions[chemical].ingredients.items():
            chemicals[ingredient] += i_qty * num_reactions
    return changed

def inefficient_react(chemicals: Chemicals, chemical: str, reactions: Dict[str, Reaction]):
    qty = chemicals[chemical]
    needed = reactions[chemical].result[1]
    changed = False
    num_reactions = math.ceil(qty / needed)
    chemicals[chemical] -= needed * num_reactions
    for ingredient, i_qty in reactions[chemical].ingredients.items():
        chemicals[ingredient] += i_qty * num_reactions

def has_dependent(chemicals: Chemicals, chemical: str, reactions: Dict[str, Reaction]) -> bool:
    for reaction in reactions.values():
        if chemical in reaction.ingredients.keys():
            if chemicals[reaction.result[0]] > 0:
                return True
    return False

def ore_for_fuel(fuel: int, reactions: Dict[str, Reaction]) -> int:
    chemicals: Chemicals = defaultdict(int, (("FUEL", fuel),))

    while True:
        changed = False
        chems = list(c for c, q in chemicals.items() if q > 0)
        for chemical in chems:
            if chemical in reactions:
                if not has_dependent(chemicals, chemical, reactions):
                    changed = True
                    inefficient_react(chemicals, chemical, reactions)
                else:
                    changed = react(chemicals, chemical, reactions) or changed

        if not changed:
            break

    return chemicals['ORE']




if __name__ == "__main__":
    reactions: Dict[str, Reaction] = {}
    with open("input.txt") as f:
        for line in f:
            result, reaction = parse_reaction(line.strip())
            reactions[result] = reaction

    chemicals: Chemicals = defaultdict(int, (("FUEL", 1),))

    print(ore_for_fuel(100, reactions))

    guess = 100
    target = 1000000000000
    ore_guess = ore_for_fuel(guess, reactions)
    found_upper = ore_guess > target
    last_guess = None
    while True:
        guess *= 2
        ore_guess = ore_for_fuel(guess, reactions)
        found_upper = ore_guess > target
        if found_upper:
            upper_bound = ore_guess
            break
    
    lower_bound = 0
    while lower_bound <= upper_bound:
        mid = (lower_bound + upper_bound) // 2
        ore_guess = ore_for_fuel(mid, reactions)
        if ore_guess < target:
            lower_bound = mid + 1
        elif ore_guess > target:
            upper_bound = mid - 1
        else:
            break
        print(mid, ore_guess)

    if ore_guess > target:
        mid -= 1
        ore_guess = ore_for_fuel(mid, reactions) 
    print(mid, ore_guess)

