from intcode import Computer

def test_write_code():
    c = Computer([1, 2, 3])
    c[5] = 10
    assert c.code == [1, 2, 3, 0, 0, 10]