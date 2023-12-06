from antlr4.tree.Tree import ErrorNodeImpl

from antlr.LanguageParser import LanguageParser
from antlr.LanguageVisitor import LanguageVisitor
from gp_algorithm.grammar import NodeType
from gp_algorithm.individual import Individual
from gp_algorithm.interpreter.exceptions import LanguageSyntaxError
from gp_algorithm.interpreter.parser import Parser
from gp_algorithm.nodes import LanguageNode


class IndividualBuilder(LanguageVisitor):
    def __init__(
        self,
        parser: Parser | None = None,
        individual: Individual | None = None,
    ) -> None:
        self._parser = parser or Parser()
        self._individual: Individual = individual or Individual()
        self._current_node: LanguageNode = self._individual

    def build_from_parser_str(self, data: str) -> Individual:
        self._individual = Individual()
        self._current_node = self._individual
        tree = self._parser.parse_str(data=data)
        self.visit(tree)
        return self._individual

    # PRIMARY EXPRESSION
    def visitStatement(self, ctx: LanguageParser.StatementContext) -> None:
        new_statement = LanguageNode(node_type=NodeType.STATEMENT)
        new_statement.parent = self._current_node
        self._current_node = new_statement
        super().visitStatement(ctx)
        self._current_node = self._current_node.parent

    def visitLine(self, ctx: LanguageParser.LineContext) -> None:
        new_line = LanguageNode(node_type=NodeType.LINE)
        new_line.parent = self._current_node
        self._current_node = new_line
        super().visitLine(ctx)
        self._current_node = self._current_node.parent

    def visitAssignment(self, ctx: LanguageParser.AssignmentContext) -> None:
        new_assignment = LanguageNode(node_type=NodeType.ASSIGNMENT)
        new_assignment.parent = self._current_node
        self._current_node = new_assignment
        self.add_var_name(ctx.VARIABLE_NAME().getText())
        super().visitAssignment(ctx)
        self._current_node = self._current_node.parent

    # STATEMENTS
    def visitConditionalStatement(self, ctx: LanguageParser.ConditionalStatementContext) -> None:
        new_conditional_statement = LanguageNode(node_type=NodeType.CONDITIONAL_STATEMENT)
        new_conditional_statement.parent = self._current_node
        self._current_node = new_conditional_statement
        super().visitConditionalStatement(ctx)
        self._current_node = self._current_node.parent

    def visitLoopStatement(self, ctx: LanguageParser.LoopStatementContext) -> None:
        new_loop_statement = LanguageNode(node_type=NodeType.LOOP_STATEMENT)
        new_loop_statement.parent = self._current_node
        self._current_node = new_loop_statement
        super().visitLoopStatement(ctx)
        self._current_node = self._current_node.parent

    def visitCompoundStatement(self, ctx: LanguageParser.CompoundStatementContext) -> None:
        new_compound_statement = LanguageNode(node_type=NodeType.COMPOUND_STATEMENT)
        new_compound_statement.parent = self._current_node
        self._current_node = new_compound_statement
        super().visitCompoundStatement(ctx)
        self._current_node = self._current_node.parent

    def visitPrintStatement(self, ctx: LanguageParser.PrintStatementContext) -> None:
        new_print_statement = LanguageNode(node_type=NodeType.PRINT_STATEMENT)
        new_print_statement.parent = self._current_node
        self._current_node = new_print_statement
        super().visitPrintStatement(ctx)
        self._current_node = self._current_node.parent

    # EXPRESSIONS
    def visitExpression(self, ctx: LanguageParser.ExpressionContext) -> None:
        new_expression = LanguageNode(node_type=NodeType.EXPRESSION)
        new_expression.parent = self._current_node
        self._current_node = new_expression
        if ctx.VARIABLE_NAME():
            self.add_var_name(ctx.VARIABLE_NAME().getText())
        if ctx.Read():
            self.add_read()
        super().visitExpression(ctx)
        self._current_node = self._current_node.parent

    def visitLiteral(self, ctx: LanguageParser.LiteralContext) -> None:
        if ctx.BOOLEAN_VAL():
            new_literal = LanguageNode(node_type=NodeType.LITERAL, value=ctx.BOOLEAN_VAL().getText())
            new_literal.parent = self._current_node
            return

        if ctx.INT_VAL():
            new_literal = LanguageNode(node_type=NodeType.LITERAL, value=ctx.INT_VAL().getText())
            new_literal.parent = self._current_node
            return

        if ctx.STRING_VAL():
            new_literal = LanguageNode(node_type=NodeType.LITERAL, value=ctx.STRING_VAL().getText())
            new_literal.parent = self._current_node
            return

        raise NotImplementedError("Unknown literal type")

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

    def add_var_name(self, var_name: str) -> None:
        new_var_name = LanguageNode(node_type=NodeType.VAR_NAME, value=var_name)
        new_var_name.parent = self._current_node

    def add_read(self) -> None:
        new_var_name = LanguageNode(node_type=NodeType.READ)
        new_var_name.parent = self._current_node


individual_builder = IndividualBuilder()
