from pathlib import Path
from typing import Callable
from unittest.mock import create_autospec

import pytest

from antlr.LanguageParser import LanguageParser
from gp_algorithm.interpreter.parser import Parser
from gp_algorithm.interpreter.variable_stack import VariableStack
from gp_algorithm.interpreter.visitor import Visitor


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
        parser = Parser()
        parser.set_token_stream(data=input_string)
        return parser

    return _
