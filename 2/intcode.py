from copy import copy
from enum import Enum
from typing import List, Optional, Tuple


class Operation(Enum):
    ADD = 1
    MULTIPLY = 2
    END = 99

TARGET = 19690720


def intcode(code: List[int]) -> List[int]:
    new_code = copy(code)

    i = 0
    operation = Operation(new_code[i])
    while operation != Operation.END:
        lh_pos, rh_pos, result_pos = new_code[i + 1 : i + 4]
        if operation == Operation.ADD:
            new_code[result_pos] = new_code[lh_pos] + new_code[rh_pos]
        if operation == Operation.MULTIPLY:
            new_code[result_pos] = new_code[lh_pos] * new_code[rh_pos]
        i += 4
        operation = Operation(new_code[i])

    return new_code

def find_inputs(code: List[int], target: int) -> Tuple[Optional[int], Optional[int]]:
    for noun in range(100):
        for verb in range(100):
            code[1:3] = noun, verb
            output = intcode(code)
            if output[0] == target:
                return noun, verb

    return None, None

        

if __name__ == "__main__":
    with open("input.txt") as f:
        for line in f:
            code = [int(i) for i in line.split(",")]

    noun, verb = find_inputs(code, TARGET)
    if noun is not None and verb is not None:
        print(f"Noun: {noun}, verb: {verb}")
        print(f"100*noun + verb = {(100 * noun) + verb}")
