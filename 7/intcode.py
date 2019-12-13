import asyncio
from copy import copy
from dataclasses import dataclass
from enum import Enum, auto
from itertools import permutations
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


class IntcodeTerminated(Exception):
    pass

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
    elif mode == Mode.IMMEDIATE:
        return value
    else:
        raise ValueError(f"Unknown mode type {mode}")

class State(Enum):
    NOT_STARTED = auto()
    RUNNING = auto()
    WAITING = auto()
    HALTED = auto()


class Computer():

    def __init__(self, code: List[int], inputs: Optional[List[int]] = None):
        self.code = copy(code)
        if inputs:
            self.inputs = inputs
        else:
            self.inputs = []
        self.output: Optional[Computer] = None
        self.state = State.NOT_STARTED
        self.pt = 0
        self.final_output: Optional[int] = None

    async def add_input(self, input: int):
        if self.state == State.HALTED:
            raise IntcodeTerminated()

        self.inputs.append(input)
        if self.state == State.WAITING:
            await self.run()

    async def run(self) -> None:
        self.state = State.RUNNING
        instruction = get_instruction(self.code[self.pt])
        while instruction.operation != Operation.END:
            pointer_modified = False
            if instruction.operation == Operation.ADD:
                lh, rh, result = self.code[self.pt + 1 : self.pt + 4]
                lh_value = get_value(self.code, instruction.parameters[0], lh)
                rh_value = get_value(self.code, instruction.parameters[1], rh)
                self.code[result] = lh_value + rh_value
            elif instruction.operation == Operation.MULTIPLY:
                lh, rh, result = self.code[self.pt + 1 : self.pt + 4]
                lh_value = get_value(self.code, instruction.parameters[0], lh)
                rh_value = get_value(self.code, instruction.parameters[1], rh)
                self.code[result] = lh_value * rh_value
            elif instruction.operation == Operation.INPUT:
                if self.inputs:
                    pos = self.code[self.pt + 1]
                    self.code[pos] = self.inputs.pop(0)
                else:
                    self.state = State.WAITING
                    return None
            elif instruction.operation == Operation.OUTPUT:
                pos = self.code[self.pt + 1]
                out = self.code[pos]
                if self.output is not None:
                    try:
                        await self.output.add_input(out)
                    except IntcodeTerminated:
                        self.final_output = out
                        return
                else:
                    self.final_output = out
            elif instruction.operation in JUMP_OPS:
                check, pointer = self.code[self.pt + 1 : self.pt + 3]
                check_value = get_value(self.code, instruction.parameters[0], check)
                pointer_value = get_value(self.code, instruction.parameters[1], pointer)

                if (check_value and instruction.operation == Operation.JUMP_TRUE) or (
                    not check_value and instruction.operation == Operation.JUMP_FALSE
                ):
                    self.pt = pointer_value
                    pointer_modified = True
            elif instruction.operation == Operation.LESS_THAN:
                lh, rh, result = self.code[self.pt + 1 : self.pt + 4]
                lh_value = get_value(self.code, instruction.parameters[0], lh)
                rh_value = get_value(self.code, instruction.parameters[1], rh)
                self.code[result] = int(lh_value < rh_value)
            elif instruction.operation == Operation.EQUALS:
                lh, rh, result = self.code[self.pt + 1 : self.pt + 4]
                lh_value = get_value(self.code, instruction.parameters[0], lh)
                rh_value = get_value(self.code, instruction.parameters[1], rh)
                self.code[result] = int(lh_value == rh_value)

            if not pointer_modified:
                self.pt += len(instruction.parameters) + 1

            instruction = get_instruction(self.code[self.pt])

        self.state = State.HALTED

async def run():
    with open("input.txt") as f:
        for line in f:
            code = [int(i) for i in line.split(",")]
    
    highest_signal = 0
    for perm in permutations(range(5)):
        computers = [Computer(code, [phase]) for phase in perm]
        for i, computer in enumerate(computers[:-1]):
            computer.output = computers[i+1]
        computers[0].inputs.append(0)
        await asyncio.gather(*(comp.run() for comp in computers))

        highest_signal = max(computers[4].final_output, highest_signal)
    print(highest_signal)

    highest_signal = 0
    for perm in permutations(range(5, 10)):
        computers = [Computer(code, [phase]) for phase in perm]
        for i, computer in enumerate(computers):
            computer.output = computers[(i+1) % 5]
        computers[0].inputs.append(0)
        await asyncio.gather(*(comp.run() for comp in computers))
        highest_signal = max(computers[4].final_output, highest_signal)

    print(highest_signal)



if __name__ == "__main__":
    asyncio.run(run())



