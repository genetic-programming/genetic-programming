from antlr4 import ParserRuleContext
from antlr4.tree.Tree import ParseTree, TerminalNodeImpl

from antlr.LanguageParser import LanguageParser
from antlr.LanguageVisitor import LanguageVisitor
from interpreter.decorators import handle_exception
from interpreter.exceptions import NullValueUsageError
from interpreter.language_types.base_type import LanguageType


class ExpressionsVisitor(LanguageVisitor):
    @handle_exception
    def visitExpression(self, ctx: LanguageParser.ExpressionContext) -> LanguageType:
        children = list(filter(self.is_not_empty_terminal, ctx.children))
        match children:
            case [atom_ctx]:
                return self.visitAtom(atom_ctx)

            case [bool_unary, expr] if ctx.booleanUnaryOperator():
                return self.handle_boolean_unary_operator(bool_unary, expr)

            case [num_unary, expr] if ctx.numericUnaryOperator():
                return self.handle_numeric_unary_operator(num_unary, expr)

            case [left, mult_op, right] if ctx.multiplicationOperator():
                return self.handle_multiplication_operator(left, mult_op, right)

            case [left, add_op, right] if ctx.additionOperator():
                return self.handle_addition_operator(left, add_op, right)

            case [left, comp_op, right] if ctx.comparisonOperator():
                return self.handle_comparison_operator(left, comp_op, right)

            case [left, and_op, right] if ctx.andOperator():
                return self.handle_and_operator(left, and_op, right)

            case [left, or_op, right] if ctx.orOperator():
                return self.handle_or_operator(left, or_op, right)

            case [parentheses_start, expr, parentheses_end] if (
                parentheses_start.symbol.text == "(" and parentheses_end.symbol.text == ")"
            ):
                return self.visitExpression(expr)

        raise NotImplementedError(f"Unknown expression type. {ctx.getText()}")

    @staticmethod
    def is_not_empty_terminal(node: ParseTree) -> bool:
        if not isinstance(node, TerminalNodeImpl):
            return True
        return node.symbol.text != " "

    def handle_boolean_unary_operator(
        self,
        boolean_unary_op_ctx: LanguageParser.BooleanUnaryOperatorContext,
        expr_ctx: LanguageParser.ExpressionContext,
    ) -> LanguageType:
        expression = self.get_operand(expr_ctx, boolean_unary_op_ctx)
        match self.visitBooleanUnaryOperator(boolean_unary_op_ctx):
            case "not":
                return ~expression
        raise NotImplementedError(f"Unknown boolean unary operator: {boolean_unary_op_ctx.getText()}")

    def handle_numeric_unary_operator(
        self,
        numeric_unary_op_ctx: LanguageParser.NumericUnaryOperatorContext,
        expr_ctx: LanguageParser.ExpressionContext,
    ) -> LanguageType:
        expression = self.get_operand(expr_ctx, numeric_unary_op_ctx)
        match self.visitNumericUnaryOperator(numeric_unary_op_ctx):
            case "+":
                return +expression
            case "-":
                return -expression
        raise NotImplementedError(f"Unknown numeric unary operator: {numeric_unary_op_ctx.getText()}")

    def handle_multiplication_operator(
        self,
        left_expr_ctx: LanguageParser.ExpressionContext,
        mult_op_ctx: LanguageParser.MultiplicationOperatorContext,
        right_expr_ctx: LanguageParser.ExpressionContext,
    ) -> LanguageType:
        left = self.get_operand(left_expr_ctx, mult_op_ctx)
        right = self.get_operand(right_expr_ctx, mult_op_ctx)
        match self.visitMultiplicationOperator(mult_op_ctx):
            case "*":
                return left * right
            case "/":
                return left / right
        raise NotImplementedError(f"Unknown multiplication operator: {mult_op_ctx.getText()}")

    def handle_addition_operator(
        self,
        left_expr_ctx: LanguageParser.ExpressionContext,
        add_op_ctx: LanguageParser.AdditionOperatorContext,
        right_expr_ctx: LanguageParser.ExpressionContext,
    ) -> LanguageType:
        left = self.get_operand(left_expr_ctx, add_op_ctx)
        right = self.get_operand(right_expr_ctx, add_op_ctx)
        match self.visitAdditionOperator(add_op_ctx):
            case "+":
                return left + right
            case "-":
                return left - right
        raise NotImplementedError(f"Unknown addition operator: {add_op_ctx.getText()}")

    def handle_comparison_operator(
        self,
        left_expr_ctx: LanguageParser.ExpressionContext,
        comp_op_ctx: LanguageParser.ComparisonOperatorContext,
        right_expr_ctx: LanguageParser.ExpressionContext,
    ) -> LanguageType:
        left = self.get_operand(left_expr_ctx, comp_op_ctx)
        right = self.get_operand(right_expr_ctx, comp_op_ctx)
        match self.visitComparisonOperator(comp_op_ctx):
            case "<":
                return left < right
            case ">":
                return left > right
            case "==":
                return left.is_equal(right)
            case "!=":
                return left.is_not_equal(right)
        raise NotImplementedError(f"Unknown comparison operator: {comp_op_ctx.getText()}")

    def handle_and_operator(
        self,
        left_expr_ctx: LanguageParser.ExpressionContext,
        and_op_ctx: LanguageParser.AndOperatorContext,
        right_expr_ctx: LanguageParser.ExpressionContext,
    ) -> LanguageType:
        left = self.get_operand(left_expr_ctx, and_op_ctx)
        right = self.get_operand(right_expr_ctx, and_op_ctx)
        return left and right

    def handle_or_operator(
        self,
        left_expr_ctx: LanguageParser.ExpressionContext,
        or_op_ctx: LanguageParser.OrOperatorContext,
        right_expr_ctx: LanguageParser.ExpressionContext,
    ) -> LanguageType:
        left = self.get_operand(left_expr_ctx, or_op_ctx)
        right = self.get_operand(right_expr_ctx, or_op_ctx)
        return left or right

    def get_operand(
        self,
        operand_ctx: LanguageParser.ExpressionContext,
        operator_ctx: ParserRuleContext,
    ) -> LanguageType:
        expression = self.visitExpression(operand_ctx)
        if expression is None:
            raise NullValueUsageError(
                operand=operand_ctx.getText(),
                operation=operator_ctx.getText(),
            )
        return expression

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
