from typing import Callable
from unittest.mock import Mock

import pytest

from antlr.LanguageParser import LanguageParser
from gp_algorithm.interpreter.exceptions import LanguageZeroDivisionError
from gp_algorithm.interpreter.expression import CONST_FALSE, CONST_TRUE, Expression
from gp_algorithm.interpreter.visitor import Visitor


@pytest.mark.parametrize(
    ("input_string", "value_from_stack", "expected_value"),
    [
        ("v420 = 0", Expression(int_value=8643), Expression(int_value=0)),
        ("v420 = true", Expression(bool_value=False), CONST_TRUE),
    ],
)
def test_visit_assignment(
    input_string: str,
    value_from_stack: Expression,
    expected_value: Expression,
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
    v2137_value: Expression,
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
    v2137_values: list[Expression],
    expected_call_number: int,
    get_parser_from_input: Callable[[str], LanguageParser],
    visitor: Visitor,
) -> None:
    parser = get_parser_from_input("while v2137 {}")
    loop_instruction_ctx = parser.loopStatement()

    visitor._variable_stack.get_var = Mock(side_effect=v2137_values)
    visitor.visit(loop_instruction_ctx)


@pytest.mark.parametrize(
    ("input_string", "expected_result"),
    [
        ("2", Expression(int_value=2)),
        ("2 + 5 * 7", Expression(int_value=37)),
        ("2 * 5 - 7", Expression(int_value=3)),
        ("0 * 190", Expression(int_value=0)),
        ("100 / 30", Expression(int_value=3)),
        ("100 > 10 and true", CONST_TRUE),
        ("1 > 2", CONST_FALSE),
        ("2 > 2", CONST_FALSE),
        ("2 > 1.", CONST_TRUE),
        ("2 == 2", CONST_TRUE),
        ("2 == 1", CONST_FALSE),
        ("2 != 2", CONST_FALSE),
        ("true == true", CONST_TRUE),
        ("true == false", CONST_FALSE),
        ("false == true", CONST_FALSE),
        ("false == false", CONST_TRUE),
        ("true != true", CONST_FALSE),
        ("true != false", CONST_TRUE),
        ("false != true", CONST_TRUE),
        ("false != false", CONST_FALSE),
        ("false > false", CONST_FALSE),
        ("false > true", CONST_FALSE),
        ("true > false", CONST_TRUE),
        ("true > true", CONST_FALSE),
        ("false - false", Expression(int_value=0)),
        ("false - true", Expression(int_value=-1)),
        ("true - false", Expression(int_value=1)),
        ("true - true", Expression(int_value=0)),
        ("false + false", Expression(int_value=0)),
        ("false + true", Expression(int_value=1)),
        ("true + false", Expression(int_value=1)),
        ("true + true", Expression(int_value=2)),
        ("false * false", Expression(int_value=0)),
        ("false * true", Expression(int_value=0)),
        ("true * false", Expression(int_value=0)),
        ("true * true", Expression(int_value=1)),
        ("false / true", Expression(int_value=0)),
        ("1 and 0", CONST_FALSE),
        ("(1 and 1)", CONST_TRUE),
        ("0 and 1", CONST_FALSE),
        ("0 and 0", CONST_FALSE),
        ("1 or 0", CONST_TRUE),
        ("1 or 1", CONST_TRUE),
        ("0 or 1", CONST_TRUE),
        ("0 or 0", CONST_FALSE),
        ("1 and 0 or 1", CONST_TRUE),
        ("-1 and 1", CONST_FALSE),
        ("true", CONST_TRUE),
        ("false", CONST_FALSE),
        ("true and false or true", CONST_TRUE),
        ("true or false and false", CONST_TRUE),
        ("(true or false) and true", CONST_TRUE),
    ],
)
def test_visit_expression(
    input_string: str,
    expected_result: Expression,
    get_parser_from_input: Callable[[str], LanguageParser],
    visitor: Visitor,
) -> None:
    parser = get_parser_from_input(input_string)
    expression_ctx = parser.expression()

    result = visitor.visit(expression_ctx)
    assert result == expected_result


@pytest.mark.parametrize(
    "input_string",
    [
        "1 / 0",
        "1/0",
        "4 / 0",
    ],
)
def test_visit_expression_divide_by_zero(
    input_string: str,
    get_parser_from_input: Callable[[str], LanguageParser],
    visitor: Visitor,
) -> None:
    parser = get_parser_from_input(input_string)
    expression_ctx = parser.expression()

    with pytest.raises(LanguageZeroDivisionError):
        visitor.visit(expression_ctx)
