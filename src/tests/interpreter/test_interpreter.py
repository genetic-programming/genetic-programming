from typing import Callable

import pytest
from antlr4 import ParseTreeWalker, TokenStream

from interpreter.interpreter import Interpreter
from interpreter.listener import Listener
from interpreter.recognizers import CustomLexer, CustomParser
from interpreter.variable_stack import VariableStack
from interpreter.visitors.main import Visitor


@pytest.mark.parametrize(
    "file_name",
    [
        "test",
    ],
)
def test_interpret_file(
    file_name: str,
    get_input_path: Callable[[str], str],
) -> None:
    variable_stack = VariableStack()
    interpreter = Interpreter(
        CustomLexer(),
        CustomParser(input=TokenStream()),
        Listener(variable_stack=variable_stack),
        ParseTreeWalker(),
        Visitor(variable_stack=variable_stack, allow_prints=True),
        print_stacktraces=True,
    )
    input_path = get_input_path(file_name)
    interpreter.interpret_file(input_path)
