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


class TileType(Enum):
    OPEN = auto()
    WALL = auto()
    KEY = auto()
    DOOR = auto()
    START = auto()


class Tile:
    def __init__(self, char: str):
        self.char = char
        if char == "#":
            self.type = TileType.WALL
            self.name = ""
        elif char == ".":
            self.type = TileType.OPEN
            self.name = ""
        elif char == "@":
            self.type = TileType.START
        elif char.islower():
            self.type = TileType.KEY
            self.name = char
        elif char.isupper():
            self.type = TileType.DOOR
            self.name = char.lower()
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


@dataclass
class DNode:
    positions: Tuple[str, ...]
    keys: int = 0
    dist: int = float("inf")

    def __lt__(self, o: DNode):
        return self.dist < o.dist

    def __ge__(self, o: DNode):
        return self.dist >= o.dist


class Maze:
    def __init__(self, maze: Dict[Coordinate, Tile]):
        self.maze = maze
        self.keys: Dict[str, Coordinate] = {}
        self.starts: Dict[str, Coordinate] = {}
        for c, t in maze.items():
            if t.type == TileType.START:
                self.starts[f"START_{len(self.starts)}"] = c
            elif t.type == TileType.KEY:
                self.keys[t.name] = c
        self.adj_matrix = self._build_adjacencies()

    def shortest_path(self):
        start = DNode(
            positions=tuple(self.starts.keys()),
            dist=0,
        )
        visited: Dict[Tuple[Tuple[str, ...], FrozenSet[str]], DNode] = {
            (start.positions, start.keys): start
        }
        q = [start]

        while q:
            node = heappop(q)
            if node.keys == 2 ** len(self.keys) - 1:
                return node
            for child, child_keys, dist in self._neighbour_keys(node.positions, node.keys):
                alt = dist + node.dist
                child_node = visited.get((child, child_keys))
                if not child_node:
                    child_node = DNode(positions=child, keys=child_keys)
                    visited[(child, child_keys)] = child_node
                if alt < child_node.dist:
                    child_node.dist = alt
                    child_node.pre = node
                    heappush(q, child_node)

        return visited

    def _neighbour_keys(
        self, key_names: Sequence[str], keys: int
    ) -> Iterator[Tuple[Tuple[str, ...], int, int]]:
        for i, key_name in enumerate(key_names):
            for neighbour_name, (dist, doors) in self.adj_matrix[key_name].items():
                if doors_unlocked(keys, doors):
                    new_key_names = (
                        *key_names[:i],
                        neighbour_name,
                        *key_names[i + 1 :],
                    )
                    child_keys = keys | key_int(neighbour_name)
                    yield (new_key_names, child_keys, dist)

    def _build_adjacencies(self) -> Dict[str, Dict[str, Tuple[int, int]]]:
        adj_map: Dict[str, Dict[str, Tuple[int, int]]] = {}
        for start_name, start in self.starts.items():
            adj_map[start_name] = self._adjacency_bfs(start)
        for key_name, key_location in self.keys.items():
            adj_map[key_name] = self._adjacency_bfs(key_location)
        return adj_map

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
            if tile.type == TileType.DOOR:
                child.doors |= key_int(tile.name)

            yield child

    def _adjacency_bfs(
        self, start_location: Coordinate
    ) -> Dict[str, Tuple[int, int]]:
        start = BFSNode(
            location=start_location,
            tile=self.maze[start_location],
        )
        q: Deque[BFSNode] = deque([start])
        adjancancies: Dict[str, Tuple[int, int]] = {}
        visited: Set[Coordinate] = {start.location}
        while q:
            node = q.popleft()
            if node.tile.type == TileType.KEY and node != start:
                adjancancies[node.tile.name] = (node.depth, node.doors)
            for move in self._next_moves(node):
                if move.location not in visited:
                    visited.add(move.location)
                    q.append(move)
        return adjancancies


def key_int(key: str) -> int:
    key = key.lower()
    offset = ord(key) - ord("a")
    return 2 ** offset

def doors_unlocked(keys: int, doors: int) -> bool:
    return not bool(~keys & doors)


if __name__ == "__main__":
    maze: Dict[Coordinate, Tile] = {}
    with open("input_2.txt") as f:
        for j, line in enumerate(f):
            for i, char in enumerate(line.strip()):
                maze[Coordinate(i, j)] = Tile(char)
    m = Maze(maze=maze)
    now = datetime.now()
    ans = m.shortest_path()
    print(f"Time taken: {datetime.now() - now}")
    print(ans.dist)
