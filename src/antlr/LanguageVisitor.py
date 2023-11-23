# Generated from /Users/spoton/Studia/pg/genetic-programming/src/antlr/Language.g4 by ANTLR 4.13.1
from antlr4 import *

if "." in __name__:
    from .LanguageParser import LanguageParser
else:
    from LanguageParser import LanguageParser

# This class defines a complete generic visitor for a parse tree produced by LanguageParser.


class LanguageVisitor(ParseTreeVisitor):
    # Visit a parse tree produced by LanguageParser#statements.
    def visitStatements(self, ctx: LanguageParser.StatementsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#statement.
    def visitStatement(self, ctx: LanguageParser.StatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#line.
    def visitLine(self, ctx: LanguageParser.LineContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#assignment.
    def visitAssignment(self, ctx: LanguageParser.AssignmentContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#conditionalStatement.
    def visitConditionalStatement(self, ctx: LanguageParser.ConditionalStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#loopStatement.
    def visitLoopStatement(self, ctx: LanguageParser.LoopStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#compoundStatement.
    def visitCompoundStatement(self, ctx: LanguageParser.CompoundStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#printStatement.
    def visitPrintStatement(self, ctx: LanguageParser.PrintStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#expression.
    def visitExpression(self, ctx: LanguageParser.ExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#nestedExpression.
    def visitNestedExpression(self, ctx: LanguageParser.NestedExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#literal.
    def visitLiteral(self, ctx: LanguageParser.LiteralContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#booleanUnaryOperator.
    def visitBooleanUnaryOperator(self, ctx: LanguageParser.BooleanUnaryOperatorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#numericUnaryOperator.
    def visitNumericUnaryOperator(self, ctx: LanguageParser.NumericUnaryOperatorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#multiplicationOperator.
    def visitMultiplicationOperator(self, ctx: LanguageParser.MultiplicationOperatorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#additionOperator.
    def visitAdditionOperator(self, ctx: LanguageParser.AdditionOperatorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#comparisonOperator.
    def visitComparisonOperator(self, ctx: LanguageParser.ComparisonOperatorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#andOperator.
    def visitAndOperator(self, ctx: LanguageParser.AndOperatorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#orOperator.
    def visitOrOperator(self, ctx: LanguageParser.OrOperatorContext):
        return self.visitChildren(ctx)


del LanguageParser
