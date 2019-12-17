from moons import Coordinate, Moon, apply_gravity, _parse_moon

def test_gravity():
    a = Moon(Coordinate(1, 2, 3))
    b = Moon(Coordinate(3, 2, 1))
    expected_va = Coordinate(1, 0, -1)
    expected_vb = Coordinate(-1, 0, 1)
    apply_gravity(a, b)
    assert a.v == expected_va
    assert b.v == expected_vb

def test_parse_moon():
    moon_str = "<x=19, y=-10, z=7>"
    expected = Moon(Coordinate(19, -10, 7))
    assert _parse_moon(moon_str) == expected
    