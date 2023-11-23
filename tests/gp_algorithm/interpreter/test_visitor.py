from typing import Callable
from unittest.mock import Mock

import pytest

from antlr.LanguageParser import LanguageParser
from gp_algorithm.interpreter.language_types.base_type import LanguageType
from gp_algorithm.interpreter.language_types.boolean import BooleanType, CONST_FALSE, CONST_TRUE
from gp_algorithm.interpreter.language_types.integer import IntegerType
from gp_algorithm.interpreter.visitor import Visitor


@pytest.mark.parametrize(
    ("input_string", "value_from_stack", "expected_value"),
    [
        ("v420 = 0", IntegerType(8643), IntegerType(0)),
        ("v420 = true", BooleanType(False), CONST_TRUE),
    ],
)
def test_visit_assignment(
    input_string: str,
    value_from_stack: LanguageType,
    expected_value: LanguageType,
    get_parser_from_input: Callable[[str], LanguageParser],
    visitor: Visitor,
) -> None:
    parser = get_parser_from_input(input_string)
    assignment_ctx = parser.assignment()

    visitor._variable_stack.set_var("v420", value_from_stack)
    visitor.visit(assignment_ctx)
    assert visitor._variable_stack.get_var("v420") == expected_value


@pytest.mark.parametrize(
    ("input_string", "v2137_value", "expected_body_number"),
    [
        pytest.param("if v2137 {}", CONST_TRUE, 0, id="condition met"),
        pytest.param("if v2137 {}", CONST_FALSE, None, id="condition not met"),
        pytest.param("if v2137 {} else {}", CONST_TRUE, 0, id="condition met with else"),
        pytest.param("if v2137 {} else {}", CONST_FALSE, 1, id="condition not met with else"),
    ],
)
def test_visit_conditional_instruction(
    input_string: str,
    v2137_value: LanguageType,
    expected_body_number: int | None,
    get_parser_from_input: Callable[[str], LanguageParser],
    visitor: Visitor,
) -> None:
    parser = get_parser_from_input(input_string)
    cond_instruction_ctx = parser.conditionalStatement()

    visitor._variable_stack.set_var("v2137", v2137_value)
    visitor.visit(cond_instruction_ctx)
    if expected_body_number is None:
        pass
    else:
        expected_call_arg = cond_instruction_ctx.compoundStatement(expected_body_number)
        assert expected_call_arg


@pytest.mark.parametrize(
    ("v2137_values", "expected_call_number"),
    [
        pytest.param(
            [CONST_FALSE],
            0,
            id="simple condition false",
        ),
        pytest.param(
            [CONST_TRUE, CONST_FALSE],
            1,
            id="v2137 set to false after one repetition",
        ),
        pytest.param(
            [CONST_TRUE, CONST_TRUE, CONST_FALSE],
            2,
            id="v2137 set to false after two repetitions",
        ),
        pytest.param(
            [CONST_TRUE, CONST_TRUE, CONST_TRUE, CONST_FALSE],
            3,
            id="v2137 set to false after three repetitions",
        ),
    ],
)
def test_visit_loop_instruction(
    v2137_values: list[LanguageType],
    expected_call_number: int,
    get_parser_from_input: Callable[[str], LanguageParser],
    visitor: Visitor,
) -> None:
    parser = get_parser_from_input("while v2137 {}")
    loop_instruction_ctx = parser.loopStatement()

    visitor._variable_stack.get_var = Mock(side_effect=v2137_values)
    visitor.visit(loop_instruction_ctx)
