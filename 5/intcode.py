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
    JUMP_TRUE = 5
    JUMP_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
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
    Operation.JUMP_TRUE: 2,
    Operation.JUMP_FALSE: 2,
    Operation.LESS_THAN: 3,
    Operation.EQUALS: 3,
}

JUMP_OPS = {Operation.JUMP_TRUE, Operation.JUMP_FALSE}


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


def get_value(code: List[int], mode: Mode, value: int) -> int:
    if mode == Mode.POSITION:
        return code[value]
    elif mode == Mocpde.IMMEDIATE:
        return value
    else:
        raise ValueError(f"Unknown mode type {mode}")


def intcode(code: List[int]) -> List[int]:
    new_code = copy(code)

    i = 0
    instruction = get_instruction(new_code[i])
    while instruction.operation != Operation.END:
        pointer_modified = False
        if instruction.operation == Operation.ADD:
            lh, rh, result = new_code[i + 1 : i + 4]
            lh_value = get_value(new_code, instruction.parameters[0], lh)
            rh_value = get_value(new_code, instruction.parameters[1], rh)
            new_code[result] = lh_value + rh_value
        elif instruction.operation == Operation.MULTIPLY:
            lh, rh, result = new_code[i + 1 : i + 4]
            lh_value = get_value(new_code, instruction.parameters[0], lh)
            rh_value = get_value(new_code, instruction.parameters[1], rh)
            new_code[result] = lh_value * rh_value
        elif instruction.operation == Operation.INPUT:
            pos = new_code[i + 1]
            new_code[pos] = int(input("Please input..."))
        elif instruction.operation == Operation.OUTPUT:
            pos = new_code[i + 1]
            print(new_code[pos])
        elif instruction.operation in JUMP_OPS:
            check, pointer = new_code[i + 1 : i + 3]
            check_value = get_value(new_code, instruction.parameters[0], check)
            pointer_value = get_value(new_code, instruction.parameters[1], pointer)

            if (check_value and instruction.operation == Operation.JUMP_TRUE) or (
                not check_value and instruction.operation == Operation.JUMP_FALSE
            ):
                i = pointer_value
                pointer_modified = True
        elif instruction.operation == Operation.LESS_THAN:
            lh, rh, result = new_code[i + 1 : i + 4]
            lh_value = get_value(new_code, instruction.parameters[0], lh)
            rh_value = get_value(new_code, instruction.parameters[1], rh)
            new_code[result] = int(lh_value < rh_value)
        elif instruction.operation == Operation.EQUALS:
            lh, rh, result = new_code[i + 1 : i + 4]
            lh_value = get_value(new_code, instruction.parameters[0], lh)
            rh_value = get_value(new_code, instruction.parameters[1], rh)
            new_code[result] = int(lh_value == rh_value)

        if not pointer_modified:
            i += len(instruction.parameters) + 1

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
    intcode(code)
