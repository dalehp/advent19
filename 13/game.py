from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from time import sleep
from typing import DefaultDict, List, Optional, Tuple

from intcode import Computer, IntcodeTerminated, InputRequested

Index = Tuple[int, int]

class Tile(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4

TILE_CHARACTERS = {
    Tile.EMPTY: ' ',
    Tile.WALL: '|',
    Tile.BLOCK: '#',
    Tile.PADDLE: '_',
    Tile.BALL: 'o',
}

@dataclass
class Pixel:
    pos: Index
    tile: Tile


class Game:
    def __init__(self, code: List[int]):
        self.grid: DefaultDict[Index, Tile] = defaultdict(lambda: Tile.EMPTY)
        self.computer = Computer(code=code)
        self.score = 0
        self.ball_pos = (0, 0)
        self.paddle_pos = (0, 0)

    def draw(self, move: int = 0) -> None:
        self.computer.inputs.append(move)
        try:
            while True:
                pixel = self.get_pixel(move)
                if pixel:
                    self.grid[pixel.pos] = pixel.tile
                    if pixel.tile == Tile.BALL:
                        self.ball_pos = pixel.pos
                    if pixel.tile == Tile.PADDLE:
                        self.paddle_pos = pixel.pos

        except (IntcodeTerminated, InputRequested):
            return

    def get_pixel(self) -> Optional[Pixel]:
        x = self.computer.run()
        y = self.computer.run()
        result = self.computer.run()
        if (x, y) == (-1, 0):
            self.score = result
            pixel = None
        else:
            pixel = Pixel((x, y), Tile(result))
        return pixel

    def min_x(self) -> int:
        return min(i_x for i_x, _ in self.grid.keys())

    def max_x(self) -> int:
        return max(i_x for i_x, _ in self.grid.keys())

    def min_y(self) -> int:
        return min(i_y for _, i_y in self.grid.keys())

    def max_y(self) -> int:
        return max(i_y for _, i_y in self.grid.keys())

    def __str__(self) -> str:
        pixels: List[str] = [f"Score = {self.score}\n"]
        for j in range(self.min_y(), self.max_y()):
            for i in range(self.min_x(), self.max_x() + 1):
                pixels.append(TILE_CHARACTERS[self.grid[(i, j)]])
            pixels.append('\n')
        return ''.join(pixels)


def get_paddle_input(ball_pos: Index, paddle_pos: Index) -> int:
    ball_x, _ = ball_pos
    paddle_x, _ = paddle_pos
    if ball_x > paddle_x:
        return 1
    elif ball_x < paddle_x:
        return -1
    else:
        return 0

if __name__ ==  "__main__":
    with open("input.txt") as f:
        for line in f:
            code = [int(i) for i in line.split(",")]
    g = Game(code=code)
    g.draw()
    num_blocks = sum(1 for tile in g.grid.values() if tile == Tile.BLOCK)
    print(num_blocks)

    code[0] = 2
    g2 = Game(code=code)
    g2.draw(0)
    print(g2)
    while True:
        #sleep(0.1)
        g2.draw(get_paddle_input(g2.ball_pos, g2.paddle_pos))
        print(g2)


