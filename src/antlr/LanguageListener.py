# Generated from /Users/spoton/Studia/pg/genetic-programming/src/antlr/Language.g4 by ANTLR 4.13.1
from antlr4 import *

if "." in __name__:
    from .LanguageParser import LanguageParser
else:
    from LanguageParser import LanguageParser


# This class defines a complete listener for a parse tree produced by LanguageParser.
class LanguageListener(ParseTreeListener):
    # Enter a parse tree produced by LanguageParser#statements.
    def enterStatements(self, ctx: LanguageParser.StatementsContext):
        pass

    # Exit a parse tree produced by LanguageParser#statements.
    def exitStatements(self, ctx: LanguageParser.StatementsContext):
        pass

    # Enter a parse tree produced by LanguageParser#statement.
    def enterStatement(self, ctx: LanguageParser.StatementContext):
        pass

    # Exit a parse tree produced by LanguageParser#statement.
    def exitStatement(self, ctx: LanguageParser.StatementContext):
        pass

    # Enter a parse tree produced by LanguageParser#line.
    def enterLine(self, ctx: LanguageParser.LineContext):
        pass

    # Exit a parse tree produced by LanguageParser#line.
    def exitLine(self, ctx: LanguageParser.LineContext):
        pass

    # Enter a parse tree produced by LanguageParser#assignment.
    def enterAssignment(self, ctx: LanguageParser.AssignmentContext):
        pass

    # Exit a parse tree produced by LanguageParser#assignment.
    def exitAssignment(self, ctx: LanguageParser.AssignmentContext):
        pass

    # Enter a parse tree produced by LanguageParser#conditionalStatement.
    def enterConditionalStatement(self, ctx: LanguageParser.ConditionalStatementContext):
        pass

    # Exit a parse tree produced by LanguageParser#conditionalStatement.
    def exitConditionalStatement(self, ctx: LanguageParser.ConditionalStatementContext):
        pass

    # Enter a parse tree produced by LanguageParser#loopStatement.
    def enterLoopStatement(self, ctx: LanguageParser.LoopStatementContext):
        pass

    # Exit a parse tree produced by LanguageParser#loopStatement.
    def exitLoopStatement(self, ctx: LanguageParser.LoopStatementContext):
        pass

    # Enter a parse tree produced by LanguageParser#compoundStatement.
    def enterCompoundStatement(self, ctx: LanguageParser.CompoundStatementContext):
        pass

    # Exit a parse tree produced by LanguageParser#compoundStatement.
    def exitCompoundStatement(self, ctx: LanguageParser.CompoundStatementContext):
        pass

    # Enter a parse tree produced by LanguageParser#printStatement.
    def enterPrintStatement(self, ctx: LanguageParser.PrintStatementContext):
        pass

    # Exit a parse tree produced by LanguageParser#printStatement.
    def exitPrintStatement(self, ctx: LanguageParser.PrintStatementContext):
        pass

    # Enter a parse tree produced by LanguageParser#readStatement.
    def enterReadStatement(self, ctx: LanguageParser.ReadStatementContext):
        pass

    # Exit a parse tree produced by LanguageParser#readStatement.
    def exitReadStatement(self, ctx: LanguageParser.ReadStatementContext):
        pass

    # Enter a parse tree produced by LanguageParser#expression.
    def enterExpression(self, ctx: LanguageParser.ExpressionContext):
        pass

    # Exit a parse tree produced by LanguageParser#expression.
    def exitExpression(self, ctx: LanguageParser.ExpressionContext):
        pass

    # Enter a parse tree produced by LanguageParser#nestedExpression.
    def enterNestedExpression(self, ctx: LanguageParser.NestedExpressionContext):
        pass

    # Exit a parse tree produced by LanguageParser#nestedExpression.
    def exitNestedExpression(self, ctx: LanguageParser.NestedExpressionContext):
        pass

    # Enter a parse tree produced by LanguageParser#literal.
    def enterLiteral(self, ctx: LanguageParser.LiteralContext):
        pass

    # Exit a parse tree produced by LanguageParser#literal.
    def exitLiteral(self, ctx: LanguageParser.LiteralContext):
        pass

    # Enter a parse tree produced by LanguageParser#booleanUnaryOperator.
    def enterBooleanUnaryOperator(self, ctx: LanguageParser.BooleanUnaryOperatorContext):
        pass

    # Exit a parse tree produced by LanguageParser#booleanUnaryOperator.
    def exitBooleanUnaryOperator(self, ctx: LanguageParser.BooleanUnaryOperatorContext):
        pass

    # Enter a parse tree produced by LanguageParser#numericUnaryOperator.
    def enterNumericUnaryOperator(self, ctx: LanguageParser.NumericUnaryOperatorContext):
        pass

    # Exit a parse tree produced by LanguageParser#numericUnaryOperator.
    def exitNumericUnaryOperator(self, ctx: LanguageParser.NumericUnaryOperatorContext):
        pass

    # Enter a parse tree produced by LanguageParser#multiplicationOperator.
    def enterMultiplicationOperator(self, ctx: LanguageParser.MultiplicationOperatorContext):
        pass

    # Exit a parse tree produced by LanguageParser#multiplicationOperator.
    def exitMultiplicationOperator(self, ctx: LanguageParser.MultiplicationOperatorContext):
        pass

    # Enter a parse tree produced by LanguageParser#additionOperator.
    def enterAdditionOperator(self, ctx: LanguageParser.AdditionOperatorContext):
        pass

    # Exit a parse tree produced by LanguageParser#additionOperator.
    def exitAdditionOperator(self, ctx: LanguageParser.AdditionOperatorContext):
        pass

    # Enter a parse tree produced by LanguageParser#comparisonOperator.
    def enterComparisonOperator(self, ctx: LanguageParser.ComparisonOperatorContext):
        pass

    # Exit a parse tree produced by LanguageParser#comparisonOperator.
    def exitComparisonOperator(self, ctx: LanguageParser.ComparisonOperatorContext):
        pass

    # Enter a parse tree produced by LanguageParser#andOperator.
    def enterAndOperator(self, ctx: LanguageParser.AndOperatorContext):
        pass

    # Exit a parse tree produced by LanguageParser#andOperator.
    def exitAndOperator(self, ctx: LanguageParser.AndOperatorContext):
        pass

    # Enter a parse tree produced by LanguageParser#orOperator.
    def enterOrOperator(self, ctx: LanguageParser.OrOperatorContext):
        pass

    # Exit a parse tree produced by LanguageParser#orOperator.
    def exitOrOperator(self, ctx: LanguageParser.OrOperatorContext):
        pass


del LanguageParser
