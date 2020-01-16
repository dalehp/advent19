from typing import Optional

from intcode import Computer, IntcodeTerminated

class BeamSearcher():
    def __init__(self, c: Computer, x: int, y: int):
        self.c = c
        self.x = x
        self.y = y

    def big_enough(self) -> bool:
        self.find_bottom()
        top_right_x = self.x + 99
        top_right_y = self.y - 99
        if top_right_y < 0:
            return False

        return self.in_beam(top_right_x, top_right_y)

    def in_beam(self, x: Optional[int] = None, y: Optional[int] = None) -> bool:
        c.reset()
        if not x:
            x = self.x
        if not y:
            y = self.y

        c.inputs = [x, y]
        print(x, y)
        return bool(c.run())

    def find_bottom(self):
        y_in_beam = False

        # Go to top of the beam
        while not y_in_beam:
            self.y += 1
            y_in_beam = self.in_beam()

        # Go to bottom of beam
        while y_in_beam:
            self.y += 1
            y_in_beam = self.in_beam()
        self.y -= 1
    

if __name__ == "__main__":
    with open("input.txt") as f:
        for line in f:
            code = [int(i) for i in line.split(",")]

    c = Computer(code=code)

    beam_affected = 0

    # for i in range(50):
    #     for j in range(50):
    #         beam_affected += 1 if in_beam(c, i, j) else 0
    # print(beam_affected)

    x = 100
    y = 100
    bs = BeamSearcher(c, x, y)

    while not bs.big_enough():
        print(bs.x, bs.y)
        bs.x += 1

    print(bs.x)

    print(bs.x * 10000 + bs.y - 99)


            