from intcode import get_instruction, Instruction, Mode, Operation

def test_get_instruction():
    code = 1002
    expected = Instruction(operation=Operation.MULTIPLY, parameters=[Mode.POSITION, Mode.IMMEDIATE, Mode.POSITION])
    assert expected == get_instruction(code)
