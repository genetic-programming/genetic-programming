from antlr4 import ParserRuleContext
from antlr4.tree.Tree import ErrorNodeImpl, TerminalNodeImpl

from antlr.LanguageParser import LanguageParser
from antlr.LanguageVisitor import LanguageVisitor
from gp_algorithm.interpreter.exceptions import (
    ConditionTypeError,
    LanguageSyntaxError,
    VariableAssignedTypeError,
    VariableUnassignedError,
    VariableValueUnassignableError,
)
from gp_algorithm.interpreter.language_types.base_type import LanguageType
from gp_algorithm.interpreter.language_types.boolean import BooleanType, CONST_TRUE
from gp_algorithm.interpreter.language_types.integer import IntegerType
from gp_algorithm.interpreter.program_io import ProgramInput, ProgramOutput
from gp_algorithm.interpreter.variable_stack import VariableStack


class ExpressionsVisitor(LanguageVisitor):
    def visitExpression(self, ctx: LanguageParser.ExpressionContext) -> LanguageType:
        children = filter(
            lambda node: not isinstance(node, TerminalNodeImpl),
            ctx.children,
        )
        match list(children):
            case [atom_ctx] if ctx.atom():
                return self.visitAtom(atom_ctx)

            case [expr]:
                return self.visitExpression(expr)

            case [operator, expr]:
                return self.handle_unary_operator(operator, expr)

            case [left, operator, right]:
                return self.handle_operator(left, operator, right)

        raise NotImplementedError(f"Unknown expression type. {ctx.getText()}")

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


class Visitor(ExpressionsVisitor):
    def __init__(
        self,
        variable_stack: VariableStack | None = None,
        program_input: ProgramInput | None = None,
        program_output: ProgramOutput | None = None,
    ) -> None:
        self._variable_stack: VariableStack = variable_stack or VariableStack()
        self._program_input: ProgramInput = program_input or ProgramInput()
        self._program_output: ProgramOutput = program_output or ProgramOutput()

    def visit_program(
        self,
        program_ctx: LanguageParser.ProgramContext,
        program_input: list[LanguageType],
    ) -> list[str]:
        self._program_input.set_inputs(program_input)
        self.visitProgram(program_ctx)
        return self._program_output.return_outputs()

    # PRIMARY EXPRESSION

    def visitProgram(self, ctx: LanguageParser.ProgramContext) -> None:
        self._variable_stack.add_frame()
        super().visitProgram(ctx)
        self._variable_stack.pop_frame()

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
            raise ConditionTypeError(type=condition_value.type_name)
        return condition_value == CONST_TRUE

    def visitCompoundStatement(self, ctx: LanguageParser.CompoundStatementContext) -> None:
        self._variable_stack.add_frame()
        super().visitCompoundStatement(ctx)
        self._variable_stack.pop_frame()

    # EXPRESSIONS

    def visitAtom(self, ctx: LanguageParser.AtomContext) -> LanguageType:
        if literal := ctx.literal():
            return self.visitLiteral(literal)
        if ctx.VARIABLE_NAME():
            name = ctx.VARIABLE_NAME().symbol.text
            var = self._variable_stack.get_var(name)
            if var.value is None:
                raise VariableUnassignedError(name=name)
            return var
        raise NotImplementedError("Unknown product.")

    # VARIABLES AND TYPES

    def visitDeclaration(self, ctx: LanguageParser.DeclarationContext) -> LanguageType:
        var_type = self.visitVarType(ctx.varType())
        name = ctx.VARIABLE_NAME().symbol.text
        var = self._variable_stack.declare_var(var_type, name)
        return var

    def visitVarType(self, ctx: LanguageParser.VarTypeContext) -> type[LanguageType]:
        if ctx.Int():
            return IntegerType
        if ctx.Bool():
            return BooleanType
        raise NotImplementedError("Unknown var type")

    def visitAssignment(self, ctx: LanguageParser.AssignmentContext) -> None:
        expr: LanguageType = self.visitExpression(ctx.expression())
        if expr is None:
            expr_str = ctx.expression().getText()
            raise VariableValueUnassignableError(expr=expr_str)

        if declaration_ctx := ctx.declaration():
            var_name = declaration_ctx.VARIABLE_NAME().symbol.text
            var = self.visitDeclaration(declaration_ctx)
        elif var_name_ctx := ctx.VARIABLE_NAME():
            var_name = var_name_ctx.symbol.text
            var = self._variable_stack.get_var(var_name)
        else:
            raise NotImplementedError("Unknown variable type")

        self.assign_expr_to_var(var=var, var_name=var_name, expr=expr)

    def visitLiteral(self, ctx: LanguageParser.LiteralContext) -> LanguageType:
        value = ctx.children[0].symbol.text
        if ctx.BOOLEAN_VAL():
            return BooleanType(value)
        if ctx.INT_VAL():
            return IntegerType(value)
        raise NotImplementedError("Unknown literal type")

    def visitErrorNode(self, error_node: ErrorNodeImpl) -> None:
        exc = LanguageSyntaxError(extra_info=str(error_node))
        exc.inject_context_to_exc(error_node.parentCtx)

    # IO

    def visitPrintStatement(self, ctx: LanguageParser.PrintStatementContext) -> None:
        language_type = self.visitExpression(ctx.expression())
        self._program_output.append(str(language_type.value))

    def visitReadStatement(self, ctx: LanguageParser.ReadStatementContext) -> None:
        var_name = ctx.VARIABLE_NAME().symbol.text
        var = self._variable_stack.get_var(var_name)
        expr = self._program_input.pop()
        self.assign_expr_to_var(var=var, var_name=var_name, expr=expr)

    @staticmethod
    def assign_expr_to_var(
        var: LanguageType,
        var_name: str,
        expr: LanguageType,
    ) -> None:
        if type(var) is not type(expr):
            raise VariableAssignedTypeError(
                val_type=expr.type_name,
                name=var_name,
                type=var.type_name,
            )
        var.value = expr.value
