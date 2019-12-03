from fuel_calc import fuel_required

def test_simple_fuel():
    assert fuel_required(12) == 2

def test_rounded_fuel():
    assert fuel_required(14) == 2

def test_big_fuel():
    assert fuel_required(1969) == 966

def test_bigger_fuel():
    assert fuel_required(100756) == 50345
