from copy import copy
from dataclasses import dataclass
from enum import Enum, auto
from itertools import permutations
from typing import List, Optional, Tuple, overload


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
    BASE = 9
    END = 99


class Mode(Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


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
    Operation.BASE: 1,
}

JUMP_OPS = {Operation.JUMP_TRUE, Operation.JUMP_FALSE}


@dataclass
class Instruction:
    operation: Operation
    parameters: List[Mode]


class IntcodeTerminated(Exception):
    pass

class InputRequested(Exception):
    pass


def get_instruction(instruction_number: int) -> Instruction:
    code = str(instruction_number)
    op = Operation(int(code[-2:]))
    params = list(reversed([Mode(int(i)) for i in code[:-2]]))
    missing_params = OP_PARAMETER_MAP[op] - len(params)
    if missing_params:
        params = params + [Mode(0)] * missing_params
    return Instruction(operation=op, parameters=params)


class State(Enum):
    NOT_STARTED = auto()
    RUNNING = auto()
    WAITING = auto()
    HALTED = auto()


class Computer:
    def __init__(self, code: List[int], output: Optional[List[int]] = None):
        self.code = copy(code)
        self.initial_code = copy(code)
        self.output = output
        self.state = State.NOT_STARTED
        self.pt = 0
        self.relative_base = 0
        self.inputs: List[int] = []

    def __setitem__(self, pos: int, value: int) -> None:
        try:
            self.code[pos] = value
        except IndexError as e:
            if pos < 0:
                raise
            extra_space = pos - len(self.code)
            self.code.extend([0] * extra_space + [value])

    @overload
    def __getitem__(self, pos: int) -> int:
        ...

    @overload
    def __getitem__(self, pos: slice) -> List[int]:
        ...

    def __getitem__(self, pos):
        if isinstance(pos, slice):
            # TODO: slicing past the end, maybe not needed.
            return self.code[pos.start : pos.stop]
        elif isinstance(pos, int):
            try:
                return self.code[pos]
            except IndexError:
                if pos < 0:
                    raise
                return 0
        else:
            raise TypeError

    def get_value(self, mode: Mode, value: int) -> int:
        if mode == Mode.POSITION:
            return self[value]
        elif mode == Mode.IMMEDIATE:
            return value
        elif mode == Mode.RELATIVE:
            return self[value + self.relative_base]
        else:
            raise ValueError(f"Unknown mode type {mode}")

    def get_output_pos(self, mode: Mode, pos: int) -> int:
        if mode == Mode.POSITION:
            return pos
        elif mode == Mode.RELATIVE:
            return pos + self.relative_base
        raise ValueError

    def run(self) -> int:
        self.state = State.RUNNING
        instruction = get_instruction(self[self.pt])
        while instruction.operation != Operation.END:
            pointer_modified = False
            if instruction.operation == Operation.ADD:
                lh, rh, result = self[self.pt + 1 : self.pt + 4]
                lh_value = self.get_value(instruction.parameters[0], lh)
                rh_value = self.get_value(instruction.parameters[1], rh)
                result_pos = self.get_output_pos(instruction.parameters[2], result)
                self[result_pos] = lh_value + rh_value
            elif instruction.operation == Operation.MULTIPLY:
                lh, rh, result = self[self.pt + 1 : self.pt + 4]
                lh_value = self.get_value(instruction.parameters[0], lh)
                rh_value = self.get_value(instruction.parameters[1], rh)
                result_pos = self.get_output_pos(instruction.parameters[2], result)
                self[result_pos] = lh_value * rh_value
            elif instruction.operation == Operation.INPUT:
                pos = self[self.pt + 1]
                out_pos = self.get_output_pos(instruction.parameters[0], pos)
                if self.inputs:
                    self[out_pos] = self.inputs.pop(0)
                else:
                    raise InputRequested()
            elif instruction.operation == Operation.OUTPUT:
                result = self[self.pt + 1]
                try:
                    out_pos = self.get_output_pos(instruction.parameters[0], result)
                    out =  self[out_pos]
                except ValueError:
                    out = result

                if self.output is not None:
                    self.output.append(out)
                else:
                    self.pt += 2
                    return out

            elif instruction.operation in JUMP_OPS:
                check, pointer = self[self.pt + 1 : self.pt + 3]
                check_value = self.get_value(instruction.parameters[0], check)
                pointer_value = self.get_value(instruction.parameters[1], pointer)

                if (check_value and instruction.operation == Operation.JUMP_TRUE) or (
                    not check_value and instruction.operation == Operation.JUMP_FALSE
                ):
                    self.pt = pointer_value
                    pointer_modified = True
            elif instruction.operation == Operation.LESS_THAN:
                lh, rh, result = self[self.pt + 1 : self.pt + 4]
                lh_value = self.get_value(instruction.parameters[0], lh)
                rh_value = self.get_value(instruction.parameters[1], rh)
                result_pos = self.get_output_pos(instruction.parameters[2], result)
                self[result_pos] = int(lh_value < rh_value)
            elif instruction.operation == Operation.EQUALS:
                lh, rh, result = self[self.pt + 1 : self.pt + 4]
                lh_value = self.get_value(instruction.parameters[0], lh)
                rh_value = self.get_value(instruction.parameters[1], rh)
                result_pos = self.get_output_pos(instruction.parameters[2], result)
                self[result_pos] = int(lh_value == rh_value)
            elif instruction.operation == Operation.BASE:
                self.relative_base += self.get_value(
                    instruction.parameters[0], self[self.pt + 1]
                )

            if not pointer_modified:
                self.pt += len(instruction.parameters) + 1

            instruction = get_instruction(self[self.pt])

        self.state = State.HALTED
        raise IntcodeTerminated()

    def reset(self):
        self.code = copy(self.initial_code)

    def hash(self):
        return hash(tuple(self.code))
