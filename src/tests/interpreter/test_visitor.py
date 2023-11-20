from typing import Callable

import pytest
from pytest_mock import MockFixture

from antlr.LanguageParser import LanguageParser
from interpreter.exceptions import VariableAssignedTypeError
from interpreter.types.base_type import LanguageType
from interpreter.types.boolean import BooleanType, CONST_FALSE, CONST_TRUE
from interpreter.types.float import FloatType
from interpreter.types.integer import IntegerType
from interpreter.visitors.main import Visitor


@pytest.mark.parametrize(
    ("input_string", "expected"),
    [
        ("float", FloatType),
        ("int", IntegerType),
        ("bool", BooleanType),
    ],
)
def test_visit_var_type(
    input_string: str,
    expected: type[LanguageType],
    get_parser_from_input: Callable[[str], LanguageParser],
    visitor: Visitor,
) -> None:
    parser = get_parser_from_input(input_string)
    var_type_ctx = parser.varType()

    result = visitor.visit(var_type_ctx)
    assert result == expected


@pytest.mark.parametrize(
    "input_string",
    [
        "Float",
        "Int",
        "Bool",
        "incorrect",
    ],
)
def test_visit_var_type_incorrect(
    input_string: str,
    get_parser_from_input: Callable[[str], LanguageParser],
    visitor: Visitor,
) -> None:
    parser = get_parser_from_input(input_string)
    var_type_ctx = parser.varType()

    with pytest.raises(NotImplementedError):
        visitor.visit(var_type_ctx)


@pytest.mark.parametrize(
    ("input_string", "expected_var_type", "expected_name"),
    [
        ("float a", FloatType, "a"),
        ("int a", IntegerType, "a"),
        ("bool jpdrugigmd", BooleanType, "jpdrugigmd"),
    ],
)
def test_visit_declaration(
    input_string: str,
    expected_var_type: type[LanguageType],
    expected_name: str,
    get_parser_from_input: Callable[[str], LanguageParser],
    visitor: Visitor,
) -> None:
    parser = get_parser_from_input(input_string)
    declaration_ctx = parser.declaration()

    visitor.visit(declaration_ctx)
    visitor.variable_stack.declare_variable.assert_called_once_with(  # type: ignore[attr-defined]
        expected_var_type,
        expected_name,
    )


@pytest.mark.parametrize(
    ("input_string", "value_from_stack", "expected_value"),
    [
        ("a = 0.", FloatType(10.0), FloatType(0.0)),
        ("a = 0", IntegerType(8643), IntegerType(0)),
        ("chuj = true", BooleanType(False), CONST_TRUE),
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
    visitor.variable_stack.get_var.return_value = value_from_stack  # type: ignore[attr-defined]

    visitor.visit(assignment_ctx)
    visitor.variable_stack.get_var.assert_called_once()  # type: ignore[attr-defined]
    assert value_from_stack == expected_value


@pytest.mark.parametrize(
    ("input_string", "value_from_stack", "expected_value"),
    [
        ("float a = 0.", FloatType(None), FloatType(0.0)),
        ("int a = 0", IntegerType(None), IntegerType(0)),
        ("bool chuj = true", BooleanType(None), CONST_TRUE),
    ],
)
def test_visit_assignment_with_declaration(
    input_string: str,
    value_from_stack: LanguageType,
    expected_value: LanguageType,
    get_parser_from_input: Callable[[str], LanguageParser],
    visitor: Visitor,
) -> None:
    parser = get_parser_from_input(input_string)
    assignment_ctx = parser.assignment()
    visitor.variable_stack.declare_variable.return_value = value_from_stack  # type: ignore[attr-defined]

    visitor.visit(assignment_ctx)
    visitor.variable_stack.declare_variable.assert_called_once()  # type: ignore[attr-defined]
    assert value_from_stack == expected_value


@pytest.mark.parametrize(
    ("input_string", "value_from_stack"),
    [
        ("a = 0.", IntegerType(None)),
        ("int a = 0.", IntegerType(None)),
        ("bool chuj = 0", BooleanType(None)),
    ],
)
def test_visit_assignment_incorrect_types(
    input_string: str,
    value_from_stack: LanguageType,
    get_parser_from_input: Callable[[str], LanguageParser],
    visitor: Visitor,
) -> None:
    parser = get_parser_from_input(input_string)
    assignment_ctx = parser.assignment()
    visitor.variable_stack.get_var.return_value = value_from_stack  # type: ignore[attr-defined]
    visitor.variable_stack.declare_variable.return_value = value_from_stack  # type: ignore[attr-defined]

    with pytest.raises(VariableAssignedTypeError):
        visitor.visit(assignment_ctx)


@pytest.mark.parametrize(
    ("input_string", "dupa_value", "expected_body_number"),
    [
        pytest.param("if dupa {}", CONST_TRUE, 0, id="condition met"),
        pytest.param("if dupa {}", CONST_FALSE, None, id="condition not met"),
        pytest.param("if dupa {} else {}", CONST_TRUE, 0, id="condition met with else"),
        pytest.param("if dupa {} else {}", CONST_FALSE, 1, id="condition not met with else"),
    ],
)
def test_visit_conditional_instruction(
    input_string: str,
    dupa_value: LanguageType,
    expected_body_number: int | None,
    get_parser_from_input: Callable[[str], LanguageParser],
    visitor: Visitor,
    mocker: MockFixture,
) -> None:
    parser = get_parser_from_input(input_string)
    cond_instruction_ctx = parser.conditionalStatement()
    visitor.variable_stack.get_var.side_effect = [dupa_value]  # type: ignore[attr-defined]
    visit_body_mock = mocker.patch("interpreter.visitors.main.Visitor.visitCompoundStatement")

    visitor.visit(cond_instruction_ctx)
    if expected_body_number is None:
        visit_body_mock.assert_not_called()
    else:
        expected_call_arg = cond_instruction_ctx.compoundStatement(expected_body_number)
        visit_body_mock.assert_called_once_with(expected_call_arg)


@pytest.mark.parametrize(
    ("dupa_values", "expected_call_number"),
    [
        pytest.param(
            [CONST_FALSE],
            0,
            id="simple condition false",
        ),
        pytest.param(
            [CONST_TRUE, CONST_FALSE],
            1,
            id="dupa set to false after one repetition",
        ),
        pytest.param(
            [CONST_TRUE, CONST_TRUE, CONST_FALSE],
            2,
            id="dupa set to false after two repetitions",
        ),
        pytest.param(
            [CONST_TRUE, CONST_TRUE, CONST_TRUE, CONST_FALSE],
            3,
            id="dupa set to false after three repetitions",
        ),
    ],
)
def test_visit_loop_instruction(
    dupa_values: list[LanguageType],
    expected_call_number: int,
    get_parser_from_input: Callable[[str], LanguageParser],
    visitor: Visitor,
    mocker: MockFixture,
) -> None:
    parser = get_parser_from_input("while dupa {}")
    loop_instruction_ctx = parser.loopStatement()
    visitor.variable_stack.get_var.side_effect = dupa_values  # type: ignore[attr-defined]
    visit_body_mock = mocker.patch("interpreter.visitors.main.Visitor.visitCompoundStatement")

    visitor.visit(loop_instruction_ctx)
    assert visit_body_mock.call_count == expected_call_number
