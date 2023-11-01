# Generated from /Users/spoton/Studia/pg/genetic-programming/src/antlr/Language.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .LanguageParser import LanguageParser
else:
    from LanguageParser import LanguageParser

# This class defines a complete generic visitor for a parse tree produced by LanguageParser.

class LanguageVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by LanguageParser#program.
    def visitProgram(self, ctx:LanguageParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#statements.
    def visitStatements(self, ctx:LanguageParser.StatementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#statement.
    def visitStatement(self, ctx:LanguageParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#line.
    def visitLine(self, ctx:LanguageParser.LineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#conditional_statement.
    def visitConditional_statement(self, ctx:LanguageParser.Conditional_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#loop_statement.
    def visitLoop_statement(self, ctx:LanguageParser.Loop_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#compound_statement.
    def visitCompound_statement(self, ctx:LanguageParser.Compound_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#expression.
    def visitExpression(self, ctx:LanguageParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#boolean_unary_operator.
    def visitBoolean_unary_operator(self, ctx:LanguageParser.Boolean_unary_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#numeric_unary_operator.
    def visitNumeric_unary_operator(self, ctx:LanguageParser.Numeric_unary_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#multiplication_operator.
    def visitMultiplication_operator(self, ctx:LanguageParser.Multiplication_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#addition_operator.
    def visitAddition_operator(self, ctx:LanguageParser.Addition_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#comparison_operator.
    def visitComparison_operator(self, ctx:LanguageParser.Comparison_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#and_operator.
    def visitAnd_operator(self, ctx:LanguageParser.And_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#or_operator.
    def visitOr_operator(self, ctx:LanguageParser.Or_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#atom.
    def visitAtom(self, ctx:LanguageParser.AtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#declaration.
    def visitDeclaration(self, ctx:LanguageParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#var_type.
    def visitVar_type(self, ctx:LanguageParser.Var_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#assignment.
    def visitAssignment(self, ctx:LanguageParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#literal.
    def visitLiteral(self, ctx:LanguageParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#printStatement.
    def visitPrintStatement(self, ctx:LanguageParser.PrintStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#readStatement.
    def visitReadStatement(self, ctx:LanguageParser.ReadStatementContext):
        return self.visitChildren(ctx)



del LanguageParser