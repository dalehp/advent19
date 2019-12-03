from wires import indices_at_distance, parse_wire, Direction, WireGrid, WireSegment


def test_parse():
    input = "U7,R6,D4,L4"
    expected = [
        WireSegment(Direction.U, 7),
        WireSegment(Direction.R, 6),
        WireSegment(Direction.D, 4),
        WireSegment(Direction.L, 4),
    ]
    assert list(parse_wire(input)) == expected


def test_add_wire():
    input = [WireSegment(Direction.U, 3), WireSegment(Direction.R, 2)]
    grid = WireGrid()
    grid.add_wire(input, 0)
    expected_indices = {(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3)}
    assert set(grid.grid.keys()) == expected_indices


def test_indices():
    expected = {(1, 0), (-1, 0), (0, 1), (0, -1)}
    assert expected == indices_at_distance(1)
