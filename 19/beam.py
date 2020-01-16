from intcode import Computer, IntcodeTerminated


def in_beam(c: Computer, x: int, y: int) -> bool:
    c.reset()
    c.inputs = [x, y]
    return bool(c.run())

def find_bottom(c, x, y) -> int:
    y_in_beam = False

    # Go to top of the beam
    while not y_in_beam:
        y += 1
        y_in_beam = in_beam(c, x, y)

    # Go to bottom of beam
    while y_in_beam:
        y += 1
        y_in_beam = in_beam(c, x, y)
    y -= 1
    return y

def big_enough(c, x, y) -> bool:
    y = find_bottom(c, x, y)
    top_right_x = x + 99
    top_right_y = y - 99
    if top_right_y < 0:
        return False

    return in_beam(c, top_right_x, top_right_y)

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

    x = 618
    y = 618

    while not big_enough(c, x, y):
        print(x, y)
        x += 1

    print(x)
    y = find_bottom(c, x, y)

    print(x * 10000 + y - 99)


            