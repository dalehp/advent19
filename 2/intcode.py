from typing import List
from enum import Enum


class Operation(Enum):
    ADD = 1
    MULTIPLY = 2
    END = 99


def intcode(code: List[int]) -> None:
    i = 0
    operation = Operation(code[i])

    while operation != Operation.END:
        lh_pos, rh_pos, result_pos = code[i + 1 : i + 4]
        if operation == Operation.ADD:
            code[result_pos] = code[lh_pos] + code[rh_pos]
        if operation == Operation.MULTIPLY:
            code[result_pos] = code[lh_pos] * code[rh_pos]
        i += 4
        operation = Operation(code[i])
        

if __name__ == "__main__":
    with open("input.txt") as f:
        for line in f:
            code = [int(i) for i in line.split(",")]
            code[1] = 12
            code[2] = 2
            intcode(code)
            print(f"Output intcode: {code}")
