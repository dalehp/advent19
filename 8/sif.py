from collections import defaultdict
from typing import Iterable, Sequence, Tuple

from more_itertools import sliced


BLACK = 0
WHITE = 1
TRANSPARENT = 2

class Layer:
    def __init__(self, width: int, height: int, pixels: Sequence[int]):
        self.width = width
        self.height = height

        if len(pixels) != width * height:
            raise ValueError

        self.map: List[List[int]] = []
        for i in range(height):
            self.map.append(pixels[i * width : i * width + width])

    def count(self, x: int) -> int:
        return sum(row.count(x) for row in self.map)


class Image:
    def __init__(self, width: int, height: int, layers: Sequence[Layer]):
        self.width = width
        self.height = height

        for layer in layers:
            if layer.width != self.width or layer.height != self.height:
                raise ValueError

        self.map: List[List[int]] = [[0 for _ in range(width)] for _ in range(height)]
        for i in range(height):
            for j in range(width):
                self.map[i][j] = self._resolve_pixel(layer.map[i][j] for layer in layers)

    def _resolve_pixel(self, pixels: Iterable[int]) -> int:
        for pixel in pixels:
            if pixel == TRANSPARENT:
                continue
            else:
                return pixel
        return TRANSPARENT

    def __str__(self):
        return '\n'.join(' '.join(str(pixel) for pixel in row) for row in self.map)



if __name__ == "__main__":
    with open("input.txt") as f:
        raw_pixels = [int(p) for p in f.readline().strip()]
    width = 25
    height = 6
    raw_layers = sliced(raw_pixels, width * height)
    layers = [Layer(width, height, layer) for layer in raw_layers]

    layer_fewest_0 = min(layers, key=lambda x: x.count(0))
    
    print(layer_fewest_0.count(1) * layer_fewest_0.count(2))

    image = Image(width, height, layers)
    print(str(image))
