from __future__ import annotations

from collections import deque
from copy import copy
from dataclasses import dataclass, field
from enum import Enum, auto
from heapq import heappop, heappush
from datetime import datetime
from typing import (
    Deque,
    Dict,
    FrozenSet,
    Iterator,
    List,
    Optional,
    Set,
    Sequence,
    Tuple,
)


@dataclass(frozen=True, eq=True)
class Coordinate:
    x: int
    y: int

    def neighbours(self) -> Iterator[Coordinate]:
        yield Coordinate(self.x, self.y + 1)
        yield Coordinate(self.x, self.y - 1)
        yield Coordinate(self.x + 1, self.y)
        yield Coordinate(self.x - 1, self.y)

    def __add__(self, o: Coordinate) -> Coordinate:
        return Coordinate(self.x + o.x, self.y + o.y) 

    def __sub__(self, o: Coordinate) -> Coordinate:
        return Coordinate(self.x - o.x, self.y - o.y)


class TileType(Enum):
    OPEN = auto()
    WALL = auto()
    PORTAL = auto()
    START = auto()
    END = auto()


class Tile:
    def __init__(self, char: str):
        self.char = char
        if char == "#":
            self.type = TileType.WALL
            self.name = ""
        elif char == ".":
            self.type = TileType.OPEN
            self.name = ""
        elif char.isupper():
            self.type = TileType.PORTAL
            self.name = char
        else:
            raise ValueError(f"Unknown tile received: {char}")

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Tile):
            raise TypeError()
        return self.type == o.type and self.name == o.name

    def __hash__(self) -> int:
        return hash(repr(self))

    def __repr__(self) -> str:
        return f"Tile(char='{self.char}')"


@dataclass
class BFSNode:
    location: Coordinate
    tile: Tile
    doors: int = 0
    depth: int = 0
    parent: Optional[BFSNode] = None

    def __post_init__(self):
        self.keys = []


class Maze:
    def __init__(self, maze: Dict[Coordinate, Tile]):
        self.maze = maze
        self.start = self._find_start()
        self.end = self._find_end()

    def _find_start(self) -> Coordinate:
        for co, tile in self.maze.items():
            if tile.name == 'A':
                for ne in co.neighbours():
                    if self.maze.get(ne) and self.maze[ne].name == 'A':
                        direction = co - ne
                        if self.maze.get(co + direction):
                            start_co = co + direction
                        elif self.maze.get(ne - direction):
                            start_co = ne - direction
                        else:
                            raise ValueError
                        self.maze[start_co].type = TileType.START
                        return start_co
        raise ValueError

    def _find_end(self) -> Coordinate:
        for co, tile in self.maze.items():
            if tile.name == 'Z':
                for ne in co.neighbours():
                    if self.maze.get(ne) and self.maze[ne].name == 'Z':
                        direction = co - ne
                        if self.maze.get(co + direction):
                            end_co = co + direction
                        elif self.maze.get(ne - direction):
                            end_co = ne - direction
                        else:
                            raise ValueError
                        self.maze[end_co].type = TileType.END
                        return end_co
        raise ValueError

    def _next_moves(self, n: BFSNode) -> Iterator[BFSNode]:
        for location in n.location.neighbours():
            tile = self.maze[location]
            if tile.type == TileType.WALL:
                continue

            child = BFSNode(
                location=location,
                tile=tile,
                depth=n.depth + 1,
                doors=copy(n.doors),
                parent=n,
            )

            yield child

    def _adjacency_bfs(
        self, start_location: Coordinate
    ) -> Optional[BFSNode]:
        start = BFSNode(
            location=start_location,
            tile=self.maze[start_location],
        )
        q: Deque[BFSNode] = deque([start])
        adjancancies: Dict[str, Tuple[int, int]] = {}
        visited: Set[Coordinate] = {start.location}
        while q:
            node = q.popleft()
            if node.tile.type == TileType.END:
                return node
            for move in self._next_moves(node):
                if move.location not in visited:
                    visited.add(move.location)
                    q.append(move)
        return None

if __name__ == "__main__":
    maze: Dict[Coordinate, Tile] = {}
    with open("input.txt") as f:
        for j, line in enumerate(f):
            for i, char in enumerate(line.rstrip()):
                if char == ' ':
                    continue
                maze[Coordinate(i, j)] = Tile(char)
    m = Maze(maze=maze)
    print(m.maze)
    print(m.start)
    print(m.end)

