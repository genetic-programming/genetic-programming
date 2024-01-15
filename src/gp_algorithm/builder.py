from antlr4.tree.Tree import ErrorNodeImpl

from antlr.LanguageParser import LanguageParser
from antlr.LanguageVisitor import LanguageVisitor
from gp_algorithm.individual import Individual
from gp_algorithm.interpreter.exceptions import LanguageSyntaxError
from gp_algorithm.interpreter.parser import Parser
from gp_algorithm.node import LanguageNode
from gp_algorithm.tree_config import NodeType


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

        self._current_node.value = " ".join([f"{{{i}}}" for i in range(tree.getChildCount())])

        self.visit(tree)

        return self._individual

    # PRIMARY EXPRESSION
    def visitConditionalStatement(self, ctx: LanguageParser.ConditionalStatementContext) -> None:
        new_conditional_statement = LanguageNode(
            node_type=NodeType.STATEMENT,
            value="if {0} {{{1}}} else {{{2}}}",
        )
        new_conditional_statement.parent = self._current_node

        self._current_node = new_conditional_statement
        self.visitExpression(ctx.expression())
        self.visitCompoundStatement(ctx.compoundStatement(0))
        self.visitCompoundStatement(ctx.compoundStatement(1))
        self._current_node = self._current_node.parent

    def visitLoopStatement(self, ctx: LanguageParser.LoopStatementContext) -> None:
        new_loop_statement = LanguageNode(
            node_type=NodeType.STATEMENT,
            value="while {0} {{{1}}}",
        )
        new_loop_statement.parent = self._current_node

        self._current_node = new_loop_statement
        self.visitExpression(ctx.expression())
        self.visitCompoundStatement(ctx.compoundStatement())
        self._current_node = self._current_node.parent

    def visitCompoundStatement(self, ctx: LanguageParser.CompoundStatementContext) -> None:
        children_number = len(
            list(ctx.statements().getChildren(lambda child: isinstance(child, LanguageParser.StatementContext))),
        )
        new_compound_statement = LanguageNode(
            node_type=NodeType.STATEMENTS,
            value=" ".join([f"{{{i}}}" for i in range(children_number)]),
        )
        new_compound_statement.parent = self._current_node

        self._current_node = new_compound_statement
        self.visitStatements(ctx.statements())
        self._current_node = self._current_node.parent

    def visitAssignment(self, ctx: LanguageParser.AssignmentContext) -> None:
        new_assignment = LanguageNode(
            node_type=NodeType.STATEMENT,
            value="{0} = {1};",
        )
        new_assignment.parent = self._current_node

        self._current_node = new_assignment
        self.add_var_name(ctx.VARIABLE_NAME().getText())
        self.visitExpression(ctx.expression())
        self._current_node = self._current_node.parent

    def visitPrintStatement(self, ctx: LanguageParser.PrintStatementContext) -> None:
        new_print_statement = LanguageNode(
            node_type=NodeType.STATEMENT,
            value="print {0};",
        )
        new_print_statement.parent = self._current_node

        self._current_node = new_print_statement
        self.visitExpression(ctx.expression())
        self._current_node = self._current_node.parent

    def visitReadStatement(self, ctx: LanguageParser.ReadStatementContext) -> None:
        new_read_statement = LanguageNode(
            node_type=NodeType.STATEMENT,
            value="read {0} {1};",
        )
        new_read_statement.parent = self._current_node

        self._current_node = new_read_statement
        self.add_var_name(ctx.VARIABLE_NAME().getText())
        super().visitExpression(ctx.expression())
        self._current_node = self._current_node.parent

    # EXPRESSIONS
    def visitExpression(self, ctx: LanguageParser.ExpressionContext) -> None:
        if ctx.VARIABLE_NAME():
            self.add_var_name(ctx.VARIABLE_NAME().getText())
            return

        if not ctx.nestedExpression() and ctx.getChildCount() == 1:
            super().visitExpression(ctx)
            return

        new_expression = LanguageNode(node_type=NodeType.EXPRESSION)
        new_expression.parent = self._current_node

        self._current_node = new_expression
        super().visitExpression(ctx)
        self._current_node = self._current_node.parent

    def visitBooleanUnaryOperator(self, ctx: LanguageParser.BooleanUnaryOperatorContext) -> None:
        self._current_node.value = "{0} {1}"
        new = LanguageNode(node_type=NodeType.UNARY_OPERATOR, value=ctx.getText())
        new.parent = self._current_node

    def visitNumericUnaryOperator(self, ctx: LanguageParser.NumericUnaryOperatorContext) -> None:
        self._current_node.value = "{0}{1}"
        new = LanguageNode(node_type=NodeType.UNARY_OPERATOR, value=ctx.getText())
        new.parent = self._current_node

    def visitMultiplicationOperator(self, ctx: LanguageParser.MultiplicationOperatorContext) -> None:
        self._current_node.value = "{0} {1} {2}"
        new = LanguageNode(node_type=NodeType.BINARY_OPERATOR, value=ctx.getText())
        new.parent = self._current_node

    def visitAdditionOperator(self, ctx: LanguageParser.AdditionOperatorContext) -> None:
        self._current_node.value = "{0} {1} {2}"
        new = LanguageNode(node_type=NodeType.BINARY_OPERATOR, value=ctx.getText())
        new.parent = self._current_node

    def visitComparisonOperator(self, ctx: LanguageParser.ComparisonOperatorContext) -> None:
        self._current_node.value = "{0} {1} {2}"
        new = LanguageNode(node_type=NodeType.BINARY_OPERATOR, value=ctx.getText())
        new.parent = self._current_node

    def visitAndOperator(self, ctx: LanguageParser.AndOperatorContext) -> None:
        self._current_node.value = "{0} {1} {2}"
        new = LanguageNode(node_type=NodeType.BINARY_OPERATOR, value=ctx.getText())
        new.parent = self._current_node

    def visitOrOperator(self, ctx: LanguageParser.OrOperatorContext) -> None:
        self._current_node.value = "{0} {1} {2}"
        new = LanguageNode(node_type=NodeType.BINARY_OPERATOR, value=ctx.getText())
        new.parent = self._current_node

    def visitNestedExpression(self, ctx: LanguageParser.NestedExpressionContext) -> None:
        self._current_node.value = "({0})"
        self.visitExpression(ctx.expression())

    def visitLiteral(self, ctx: LanguageParser.LiteralContext) -> None:
        if ctx.BOOLEAN_VAL():
            new_literal = LanguageNode(node_type=NodeType.LITERAL_BOOL, value=ctx.BOOLEAN_VAL().getText())
            new_literal.parent = self._current_node
            return

        if ctx.INT_VAL():
            new_literal = LanguageNode(node_type=NodeType.LITERAL_INT, value=ctx.INT_VAL().getText())
            new_literal.parent = self._current_node
            return

        raise NotImplementedError("Unknown literal type")

    def visitErrorNode(self, error_node: ErrorNodeImpl) -> None:
        exc = LanguageSyntaxError(extra_info=str(error_node))
        exc.inject_context_to_exc(error_node.parentCtx)

    def add_var_name(self, var_name: str) -> None:
        new_var_name = LanguageNode(node_type=NodeType.VARIABLE_NAME, value=var_name)
        new_var_name.parent = self._current_node


individual_builder = IndividualBuilder()
