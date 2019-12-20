from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Deque, List, Iterator, Set, Tuple, Optional

from intcode import Computer, InputRequested

MOVE_COMMANDS = (1, 2, 3, 4)

@dataclass(eq=True, frozen=True)
class Coordinate:
    x: int
    y: int

    def difference(self, other) -> Coordinate:
        return Coordinate(other.x - self.x, other.y - self.y)

    def __add__(self, o: Coordinate) -> Coordinate:
        return Coordinate(self.x + o.x, self.y + o.y)

    def __repr__(self):
        return f"Coordinate(x={self.x}, y={self.y})"


MOVE_VECTORS = {
    1: Coordinate(0, 1),
    2: Coordinate(0, -1),
    3: Coordinate(-1, 0),
    4: Coordinate(1, 0),
}


@dataclass
class Node:
    computer: Computer
    location: Coordinate
    parent: Optional[Node] = None
    goal: bool = False

    def get_children(self) -> Iterator[Node]:
        for command in MOVE_COMMANDS:
            output: List[int] = []
            child_computer = Computer(code=self.computer.code, output=output)
            child_computer.inputs.append(command)
            try:
                child_computer.run()
            except InputRequested:
                pass
            if output[-1] == 2:
                yield Node(
                    computer=child_computer,
                    location=self.location + MOVE_VECTORS[command],
                    parent=self,
                    goal=True,
                )
            elif output[-1] == 1:
                yield Node(
                    computer=child_computer,
                    location=self.location + MOVE_VECTORS[command],
                    parent=self,
                    goal=False,
                )
                


def search(start: Node):
    q: Deque[Node] = Deque([start])
    visited: Set[Coordinate] = {start.location}
    count = 0
    while visited:
        node = q.popleft()
        if node.goal:
            return node
        for child in node.get_children():
            if child.location not in visited:
                visited.add(child.location)
                q.append(child)
        count += 1


if __name__ == "__main__":
    with open("input.txt") as f:
        for line in f:
            code = [int(i) for i in line.split(",")]

    goal = search(Node(computer=Computer(code), location=Coordinate(0, 0)))
    goal_location = goal.location
    
    moves = 0
    while goal.parent:
        goal = goal.parent
        moves += 1

    print(moves)
    print(goal_location)

