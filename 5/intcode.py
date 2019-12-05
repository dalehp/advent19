from copy import copy
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional, Tuple


TARGET = 19690720


class Operation(Enum):
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    END = 99


class Mode(Enum):
    POSITION = 0
    IMMEDIATE = 1


OP_PARAMETER_MAP = {
    Operation.ADD: 3,
    Operation.MULTIPLY: 3,
    Operation.INPUT: 1,
    Operation.OUTPUT: 1,
    Operation.END: 0,
}


@dataclass
class Instruction:
    operation: Operation
    parameters: List[Mode]


def get_instruction(instruction_number: int) -> Instruction:
    code = str(instruction_number)
    op = Operation(int(code[-2:]))
    params = list(reversed([Mode(int(i)) for i in code[:-2]]))
    missing_params = OP_PARAMETER_MAP[op] - len(params)
    if missing_params:
        params = params + [Mode(0)] * missing_params
    return Instruction(operation=op, parameters=params)


def get_value(code: List[int], mode: Mode, value: int) -> Optional[int]:
    if mode == Mode.POSITION:
        return code[value]
    elif mode == Mode.IMMEDIATE:
        return value
    else:
        raise ValueError(f"Unknown mode type {mode}")


def intcode(code: List[int]) -> List[int]:
    new_code = copy(code)

    i = 0
    instruction = get_instruction(new_code[i])
    while instruction.operation != Operation.END:
        if operation == Operation.ADD:
            lh, rh, result = new_code[i + 1 : i + 4]
            new_code[result] = get_value(lh) + get_value(rh)
        elif operation == Operation.MULTIPLY:
            lh, rh, result = new_code[i + 1 : i + 4]
            new_code[result] = get_value(lh) * get_value(rh)
        elif operation == Operation.INPUT:
            pos = new_code[i + 1]
            new_code[pos]

        i += 4
        instruction = get_instruction(new_code[i])

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
