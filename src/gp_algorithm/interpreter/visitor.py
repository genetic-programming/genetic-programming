from antlr4 import ParserRuleContext
from antlr4.tree.Tree import ErrorNodeImpl

from antlr.LanguageParser import LanguageParser
from antlr.LanguageVisitor import LanguageVisitor
from gp_algorithm.interpreter.exceptions import (
    ConditionTypeError,
    LanguageSyntaxError,
    TooManyStatements,
    VariableValueUnassignableError,
)
from gp_algorithm.interpreter.language_types.base_type import LanguageType
from gp_algorithm.interpreter.language_types.boolean import BooleanType, CONST_TRUE
from gp_algorithm.interpreter.language_types.integer import IntegerType
from gp_algorithm.interpreter.program_io import ProgramInput, ProgramOutput
from gp_algorithm.interpreter.variable_stack import VariableStack


class Visitor(LanguageVisitor):
    def __init__(
        self,
        variable_stack: VariableStack | None = None,
        program_input: ProgramInput | None = None,
        program_output: ProgramOutput | None = None,
    ) -> None:
        self._variable_stack: VariableStack = variable_stack or VariableStack()
        self._program_input: ProgramInput = program_input or ProgramInput()
        self._program_output: ProgramOutput = program_output or ProgramOutput()
        self._statement_left: int = 100

    def visit_tree(
        self,
        tree: LanguageParser.StatementsContext,
        program_input: list[LanguageType],
        statements_left: int = 100,
    ) -> list[str]:
        self._statement_left = statements_left
        self._program_input.set_inputs(program_input)
        self.visitStatements(tree)
        return self._program_output.return_outputs()

    # PRIMARY EXPRESSION
    def visitStatements(self, ctx: LanguageParser.StatementsContext) -> None:
        self._variable_stack.add_frame()
        super().visitStatements(ctx)
        self._variable_stack.pop_frame()

    def visitStatement(self, ctx: LanguageParser.StatementContext) -> None:
        self._statement_left -= 1
        if self._statement_left < 0:
            exc = TooManyStatements()
            exc.inject_context_to_exc(ctx)
            raise exc
        return super().visitStatement(ctx)

    def visitAssignment(self, ctx: LanguageParser.AssignmentContext) -> None:
        expr: LanguageType = self.visitExpression(ctx.expression())
        if expr is None:
            exc = VariableValueUnassignableError(expr=ctx.expression().getText())
            exc.inject_context_to_exc(ctx)
            raise exc

        var_name = ctx.VARIABLE_NAME().symbol.text
        self._variable_stack.set_var(var_name=var_name, expr=expr)

    # STATEMENTS
    def visitConditionalStatement(
        self,
        ctx: LanguageParser.ConditionalStatementContext,
    ) -> None:
        expression_ctx = ctx.expression()
        if self.check_condition(expression_ctx):
            self.visitCompoundStatement(ctx.compoundStatement(0))
        elif ctx.Else():
            self.visitCompoundStatement(ctx.compoundStatement(1))

    def visitLoopStatement(self, ctx: LanguageParser.LoopStatementContext) -> None:
        expression_ctx = ctx.expression()
        body_ctx = ctx.compoundStatement()
        while self.check_condition(expression_ctx):
            self.visitCompoundStatement(body_ctx)

    def check_condition(self, condition_ctx: LanguageParser.ExpressionContext) -> bool:
        condition_value: LanguageType = self.visitExpression(condition_ctx)
        if not isinstance(condition_value, BooleanType):
            exc = ConditionTypeError(type=condition_value.type_name)
            exc.inject_context_to_exc(condition_ctx)
            raise exc
        return condition_value == CONST_TRUE

    def visitCompoundStatement(self, ctx: LanguageParser.CompoundStatementContext) -> None:
        self._variable_stack.add_frame()
        super().visitCompoundStatement(ctx)
        self._variable_stack.pop_frame()

    def visitPrintStatement(self, ctx: LanguageParser.PrintStatementContext) -> None:
        language_type = self.visitExpression(ctx.expression())
        self._program_output.append(str(language_type.value))

    # EXPRESSIONS
    def visitExpression(self, ctx: LanguageParser.ExpressionContext) -> LanguageType:
        match ctx.children:
            case [_] if var_terminal := ctx.VARIABLE_NAME():
                name = var_terminal.symbol.text
                return self._variable_stack.get_var(name)

            case [_] if ctx.Read():
                return self._program_input.pop()

            case [node]:
                return self.visit(node)

            case [operator, expr]:
                return self.handle_unary_operator(operator, expr)

            case [left, operator, right]:
                return self.handle_operator(left, operator, right)

        raise NotImplementedError(f"Unknown expression type. {ctx.getText()}")

    def visitNestedExpression(self, ctx: LanguageParser.NestedExpressionContext) -> LanguageType:
        return self.visitExpression(ctx.expression())

    def visitLiteral(self, ctx: LanguageParser.LiteralContext) -> LanguageType:
        value = ctx.children[0].symbol.text
        if ctx.BOOLEAN_VAL():
            return BooleanType(value)
        if ctx.INT_VAL():
            return IntegerType(value)
        raise NotImplementedError("Unknown literal type")

    def handle_unary_operator(
        self,
        operator_ctx: LanguageParser.BooleanUnaryOperatorContext,
        expr_ctx: LanguageParser.ExpressionContext,
    ) -> LanguageType:
        expression = self.visitExpression(expr_ctx)
        operator = self.visit(operator_ctx)
        match operator:
            case "not":
                return ~expression
            case "+":
                return +expression
            case "-":
                return -expression
        raise NotImplementedError(f"Unknown unary operator: {operator}")

    def handle_operator(
        self,
        left_ctx: LanguageParser.ExpressionContext,
        operator_ctx: ParserRuleContext,
        right_ctx: LanguageParser.ExpressionContext,
    ) -> LanguageType:
        left = self.visitExpression(left_ctx)
        right = self.visitExpression(right_ctx)
        operator = self.visit(operator_ctx)
        match operator:
            case "*":
                return left * right
            case "/":
                return left / right
            case "+":
                return left + right
            case "-":
                return left - right
            case ">":
                return left.is_greater_than(right)
            case "==":
                return left.is_equal(right)
            case "!=":
                return ~left.is_equal(right)
            case "and":
                return left and right
            case "or":
                return left or right
        raise NotImplementedError(f"Unknown operator: {operator}")

    def visitBooleanUnaryOperator(self, ctx: LanguageParser.BooleanUnaryOperatorContext) -> str:
        return ctx.children[0].symbol.text

    def visitNumericUnaryOperator(self, ctx: LanguageParser.NumericUnaryOperatorContext) -> str:
        return ctx.children[0].symbol.text

    def visitMultiplicationOperator(self, ctx: LanguageParser.MultiplicationOperatorContext) -> str:
        return ctx.children[0].symbol.text

    def visitAdditionOperator(self, ctx: LanguageParser.AdditionOperatorContext) -> str:
        return ctx.children[0].symbol.text

    def visitComparisonOperator(self, ctx: LanguageParser.ComparisonOperatorContext) -> str:
        return ctx.children[0].symbol.text

    def visitAndOperator(self, ctx: LanguageParser.AndOperatorContext) -> str:
        return ctx.children[0].symbol.text

    def visitOrOperator(self, ctx: LanguageParser.OrOperatorContext) -> str:
        return ctx.children[0].symbol.text

    def visitErrorNode(self, error_node: ErrorNodeImpl) -> None:
        exc = LanguageSyntaxError(extra_info=str(error_node))
        exc.inject_context_to_exc(error_node.parentCtx)
