from collections import defaultdict
from intcode import Computer, IntcodeTerminated, State
from typing import DefaultDict, List, Set, Tuple

Index = Tuple[int, int]

MOVES = {

}

class Robot:
    def __init__(self, code: List[int]):
        self.grid: DefaultDict[Index, int] = defaultdict(int)
        self.computer = Computer(code=code)
        self.pos = (0, 0)
        self.dir = (0, 1)
        self.grid[(0, 0)] = 1

    def turn(self, turn_code: int) -> None:
        if turn_code == 0:
            self.dir = (- self.dir[1], self.dir[0])
        elif turn_code == 1:
            self.dir = (self.dir[1], - self.dir[0])

    def run(self) -> int:
        visited: Set[Index] = {self.pos}
        try:
            while True:
                paint_output = self.computer.run(self.grid[self.pos])
                self.grid[self.pos] = paint_output
                turn_output = self.computer.run(self.grid[self.pos])
                self.turn(turn_output)
                self.pos = (self.pos[0] + self.dir[0], self.pos[1] + self.dir[1])
                visited.add(self.pos)
        except IntcodeTerminated:
            return len(visited)

    def min_x(self) -> int:
        return min(i_x for i_x, _ in self.grid.keys())

    def max_x(self) -> int:
        return max(i_x for i_x, _ in self.grid.keys())

    def min_y(self) -> int:
        return min(i_y for _, i_y in self.grid.keys())

    def max_y(self) -> int:
        return max(i_y for _, i_y in self.grid.keys())

    def __str__(self) -> str:
        pixels = []
        for j in range(self.max_y(), self.min_y() - 1, -1):
            for i in range(self.min_x(), self.max_x() + 1):
                pixels.append('#' if self.grid[(i, j)] else '.')
            pixels.append('\n')
        return ''.join(pixels)


if __name__ ==  "__main__":
    with open("input.txt") as f:
        for line in f:
            code = [int(i) for i in line.split(",")]
    r = Robot(code=code)
    visited = r.run()
    print(visited)
    print(r)


