from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Callable, Deque, List, Iterator, Set, Tuple, Optional

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


def search(start: Node, win_condition: Callable):
    q: Deque[Node] = Deque([start])
    visited: Set[Coordinate] = {start.location}
    while q:
        print(visited_nodes_map(visited))
        node = q.popleft()
        if win_condition(node):
            return node
        for child in node.get_children():
            if child.location not in visited:
                visited.add(child.location)
                q.append(child)
    return node

def visited_nodes_map(visited: Set[Coordinate]) -> str:
    min_x = -20
    max_x = 18
    min_y = -18
    max_y = 20
    OXYGEN_LOCATION = Coordinate(12, -12)

    pixels: List[str] = []
    for j in range(min_y, max_y + 1):
        for i in range(min_x, max_x + 1):
            if Coordinate(i, j) in visited:
                if Coordinate(i, j) == OXYGEN_LOCATION:
                    pixels.append('o')
                else:
                    pixels.append("*")
            else:
                pixels.append(".")
        pixels.append('\n')
    return ''.join(pixels)


if __name__ == "__main__":
    with open("input.txt") as f:
        for line in f:
            code = [int(i) for i in line.split(",")]

    goal = search(
        Node(computer=Computer(code), location=Coordinate(0, 0)),
        win_condition=lambda n: n.goal,
    )

    goal.parent = None
    new_goal = goal = search(goal, win_condition=lambda n: False)
    furthest_point = new_goal.location

    moves = 0
    while new_goal.parent:
        new_goal = new_goal.parent
        moves += 1
    print(moves)
