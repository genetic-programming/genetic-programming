from pathlib import Path
from typing import Callable
from unittest.mock import create_autospec

import pytest
from antlr4 import CommonTokenStream, InputStream

from antlr.LanguageParser import LanguageParser
from interpreter.recognizers import CustomLexer, CustomParser
from interpreter.variable_stack import VariableStack
from interpreter.visitors.main import Visitor


@pytest.fixture()
def visitor() -> Visitor:
    variable_stack = create_autospec(VariableStack)
    visitor = Visitor(variable_stack=variable_stack)
    return visitor


@pytest.fixture()
def get_input_path() -> Callable[[str], str]:
    def _(source_file_name: str = "test") -> str:
        return str(Path(__file__).parent / "inputs" / source_file_name)

    return _


@pytest.fixture()
def get_parser_from_input() -> Callable[[str], LanguageParser]:
    def _(input_string: str) -> LanguageParser:
        input_stream = InputStream(input_string)
        lexer = CustomLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        return CustomParser(token_stream)

    return _
