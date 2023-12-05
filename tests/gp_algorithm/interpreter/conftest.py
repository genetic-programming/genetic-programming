from typing import Callable

import pytest

from antlr.LanguageParser import LanguageParser
from gp_algorithm.interpreter.parser import Parser
from gp_algorithm.interpreter.visitor import Visitor


@pytest.fixture()
def visitor() -> Visitor:
    visitor = Visitor()
    visitor._variable_stack.add_frame()
    return visitor


@pytest.fixture()
def get_parser_from_input() -> Callable[[str], LanguageParser]:
    def _(input_string: str) -> LanguageParser:
        parser = Parser()
        parser.set_token_stream(data=input_string)
        return parser

    return _
