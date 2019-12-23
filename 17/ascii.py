from collections import defaultdict
from dataclasses import dataclass, field
from typing import DefaultDict, List, Tuple

from intcode import Computer, IntcodeTerminated


Index = Tuple[int, int]


@dataclass
class Vacuum:
    computer: Computer
    grid: List[List[str]] = field(init=False)

    def __post_init__(self):
        self.grid = []

    def draw(self) -> str:
        output: List[int] = []
        self.computer.output = output
        try:
            self.computer.run()
        except IntcodeTerminated:
            pass

        squares: List[str] = []
        for o in output:
            squares.append(chr(o))

        text = "".join(squares)
        self.grid = [list(line) for line in text.split("\n")][:-2]

        return "".join(squares)

    def grid_size(self) -> Index:
        return len(self.grid[0]) - 1, len(self.grid) - 1

    def find_intersections(self) -> List[Index]:
        inters = []
        for j, row in enumerate(self.grid):
            for i, char in enumerate(row):
                if self._is_intersection(i, j):
                    inters.append((i, j))
        return inters

    def _is_intersection(self, x: int, y: int) -> bool:
        if self.grid[y][x] != "#":
            return False
        neighbours = self._get_neighbors(x, y)
        if len(neighbours) != 4:
            return False
        for neighbour in neighbours:
            if neighbour != "#":
                return False
        return True

    def _get_neighbors(self, x: int, y: int) -> List[str]:
        if x == 0 or y == 0:
            return []
        max_x, max_y = self.grid_size()
        if x == max_x or y == max_y:
            return []
        return [
            self.grid[y][x + 1],
            self.grid[y][x - 1],
            self.grid[y - 1][x],
            self.grid[y + 1][x],
        ]


def inputs_to_ascii(inps: List[str]) -> List[int]:
    inp_string = ",".join(inps)
    return [ord(inp) for inp in inp_string] + [ord("\n")]


if __name__ == "__main__":
    with open("input.txt") as f:
        for line in f:
            code = [int(i) for i in line.split(",")]

    v = Vacuum(Computer(code))
    print(v.draw())
    print(f"intersections: {len(v.find_intersections())}")
    print(f"Total alignment: {sum(x * y for x, y in v.find_intersections())}")

    main_routine = ["A", "B", "A", "C", "B", "A", "C", "A", "C", "B"]
    sub_a = ["L", "12", "L", "8", "L", "8"]
    sub_b = ["L", "12", "R", "4", "L", "12", "R", "6"]
    sub_c = ["R", "4", "L", "12", "L", "12", "R", "6"]
    video = ["n"]

    code[0] = 2
    inputs = [
        *inputs_to_ascii(main_routine),
        *inputs_to_ascii(sub_a),
        *inputs_to_ascii(sub_b),
        *inputs_to_ascii(sub_c),
        *inputs_to_ascii(video),
    ]
    print(inputs)

    output: List[int] = []
    v2 = Vacuum(Computer(code, inputs=inputs, output=output))
    try:
        v2.computer.run()
    except IntcodeTerminated:
        pass
    print(output)
