from antlr4.tree.Tree import ErrorNodeImpl

from antlr.LanguageParser import LanguageParser
from interpreter.decorators import handle_exception
from interpreter.exceptions import (
    ConditionTypeError,
    LanguageSyntaxError,
    VariableAssignedTypeError,
    VariableUnassignedError,
    VariableValueUnassignableError,
)
from interpreter.types.base_type import LanguageType
from interpreter.types.boolean import BooleanType, CONST_TRUE
from interpreter.types.float import FloatType
from interpreter.types.integer import IntegerType
from interpreter.variable_stack import VariableStack
from interpreter.visitors.expressions import ExpressionsVisitor


class Visitor(ExpressionsVisitor):
    def __init__(
        self,
        variable_stack: VariableStack,
        allow_prints: bool = False,
    ) -> None:
        self.variable_stack = variable_stack
        self._allow_prints = allow_prints

    # PRIMARY EXPRESSION
    @handle_exception
    def visitProgram(self, ctx: LanguageParser.ProgramContext) -> None:
        self.variable_stack.append_frame("main")
        self.variable_stack.append_subframe()
        super().visitProgram(ctx)
        self.variable_stack.pop_frame()

    # STATEMENTS
    @handle_exception
    def visitConditionalStatement(
        self,
        ctx: LanguageParser.ConditionalStatementContext,
    ) -> None:
        expression_ctx = ctx.expression()
        if self.check_condition(expression_ctx):
            self.visitCompoundStatement(ctx.compoundStatement(0))
        elif ctx.Else():
            self.visitCompoundStatement(ctx.compoundStatement(1))

    @handle_exception
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

    @handle_exception
    def visitCompoundStatement(self, ctx: LanguageParser.CompoundStatementContext) -> None:
        self.variable_stack.append_subframe()
        super().visitCompoundStatement(ctx)
        self.variable_stack.pop_subframe()

    # EXPRESSIONS
    @handle_exception
    def visitAtom(self, ctx: LanguageParser.AtomContext) -> LanguageType:
        if literal := ctx.literal():
            return self.visitLiteral(literal)
        if ctx.VARIABLE_NAME():
            name = ctx.VARIABLE_NAME().symbol.text
            var = self.variable_stack.get_var(name)
            if var.value is None:
                raise VariableUnassignedError(name=name)
            return var
        raise NotImplementedError("Unknown product.")

    # VARIABLES AND TYPES
    @handle_exception
    def visitDeclaration(self, ctx: LanguageParser.DeclarationContext) -> LanguageType:
        var_type = self.visitVarType(ctx.varType())
        name = ctx.VARIABLE_NAME().symbol.text
        var = self.variable_stack.declare_variable(var_type, name)
        return var

    def visitVarType(self, ctx: LanguageParser.VarTypeContext) -> type[LanguageType]:
        if ctx.Float():
            return FloatType
        if ctx.Int():
            return IntegerType
        if ctx.Bool():
            return BooleanType
        raise NotImplementedError("Unknown var type")

    @handle_exception
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
            var = self.variable_stack.get_var(var_name)
        else:
            raise NotImplementedError("Unknown variable type")

        if type(var) is not type(expr):
            raise VariableAssignedTypeError(
                val_type=expr.type_name,
                name=var_name,
                type=var.type_name,
            )
        var.value = expr.value

    @handle_exception
    def visitLiteral(self, ctx: LanguageParser.LiteralContext) -> LanguageType:
        value = ctx.children[0].symbol.text
        if ctx.BOOLEAN_VAL():
            return BooleanType(value)
        if ctx.FLOAT_VAL():
            return FloatType(value)
        if ctx.INT_VAL():
            return IntegerType(value)
        raise NotImplementedError("Unknown literal type")

    def visitErrorNode(self, error_node: ErrorNodeImpl) -> None:
        exc = LanguageSyntaxError(extra_info=str(error_node))
        exc.inject_context_to_exc(error_node.parentCtx)
