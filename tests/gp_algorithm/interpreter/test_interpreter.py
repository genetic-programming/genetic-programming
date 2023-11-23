from typing import Callable

import pytest

from gp_algorithm.interpreter.interpreter import Interpreter


@pytest.mark.parametrize(
    ("file_name", "inputs"),
    [
        ("test_1", []),
        ("test_2", ["1", "1"]),
    ],
)
def test_interpret_file(
    file_name: str,
    inputs: list[str],
    get_input_path: Callable[[str], str],
) -> None:
    interpreter = Interpreter(print_stacktraces=True)
    input_path = get_input_path(file_name)
    program_input = interpreter.interpret_input(input_strings=inputs)
    interpreter.interpret_file(file_path=input_path, program_input=program_input)
