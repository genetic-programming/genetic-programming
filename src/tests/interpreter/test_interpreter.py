from typing import Callable

import pytest

from interpreter.interpreter import create_interpreter
from interpreter.language_types.base_type import LanguageType
from interpreter.language_types.integer import IntegerType


@pytest.mark.parametrize(
    ("file_name", "inputs"),
    [
        ("test_1", []),
        ("test_2", [IntegerType(1), IntegerType(1)]),
    ],
)
def test_interpret_file(
    file_name: str,
    inputs: list[LanguageType],
    get_input_path: Callable[[str], str],
) -> None:
    interpreter = create_interpreter(print_stacktraces=True)
    input_path = get_input_path(file_name)
    interpreter.interpret_file(file_path=input_path, inputs=inputs)
