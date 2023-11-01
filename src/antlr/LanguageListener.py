# Generated from /Users/spoton/Studia/pg/genetic-programming/src/antlr/Language.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .LanguageParser import LanguageParser
else:
    from LanguageParser import LanguageParser

# This class defines a complete listener for a parse tree produced by LanguageParser.
class LanguageListener(ParseTreeListener):

    # Enter a parse tree produced by LanguageParser#program.
    def enterProgram(self, ctx:LanguageParser.ProgramContext):
        pass

    # Exit a parse tree produced by LanguageParser#program.
    def exitProgram(self, ctx:LanguageParser.ProgramContext):
        pass


    # Enter a parse tree produced by LanguageParser#statements.
    def enterStatements(self, ctx:LanguageParser.StatementsContext):
        pass

    # Exit a parse tree produced by LanguageParser#statements.
    def exitStatements(self, ctx:LanguageParser.StatementsContext):
        pass


    # Enter a parse tree produced by LanguageParser#statement.
    def enterStatement(self, ctx:LanguageParser.StatementContext):
        pass

    # Exit a parse tree produced by LanguageParser#statement.
    def exitStatement(self, ctx:LanguageParser.StatementContext):
        pass


    # Enter a parse tree produced by LanguageParser#line.
    def enterLine(self, ctx:LanguageParser.LineContext):
        pass

    # Exit a parse tree produced by LanguageParser#line.
    def exitLine(self, ctx:LanguageParser.LineContext):
        pass


    # Enter a parse tree produced by LanguageParser#conditional_statement.
    def enterConditional_statement(self, ctx:LanguageParser.Conditional_statementContext):
        pass

    # Exit a parse tree produced by LanguageParser#conditional_statement.
    def exitConditional_statement(self, ctx:LanguageParser.Conditional_statementContext):
        pass


    # Enter a parse tree produced by LanguageParser#loop_statement.
    def enterLoop_statement(self, ctx:LanguageParser.Loop_statementContext):
        pass

    # Exit a parse tree produced by LanguageParser#loop_statement.
    def exitLoop_statement(self, ctx:LanguageParser.Loop_statementContext):
        pass


    # Enter a parse tree produced by LanguageParser#compound_statement.
    def enterCompound_statement(self, ctx:LanguageParser.Compound_statementContext):
        pass

    # Exit a parse tree produced by LanguageParser#compound_statement.
    def exitCompound_statement(self, ctx:LanguageParser.Compound_statementContext):
        pass


    # Enter a parse tree produced by LanguageParser#expression.
    def enterExpression(self, ctx:LanguageParser.ExpressionContext):
        pass

    # Exit a parse tree produced by LanguageParser#expression.
    def exitExpression(self, ctx:LanguageParser.ExpressionContext):
        pass


    # Enter a parse tree produced by LanguageParser#boolean_unary_operator.
    def enterBoolean_unary_operator(self, ctx:LanguageParser.Boolean_unary_operatorContext):
        pass

    # Exit a parse tree produced by LanguageParser#boolean_unary_operator.
    def exitBoolean_unary_operator(self, ctx:LanguageParser.Boolean_unary_operatorContext):
        pass


    # Enter a parse tree produced by LanguageParser#numeric_unary_operator.
    def enterNumeric_unary_operator(self, ctx:LanguageParser.Numeric_unary_operatorContext):
        pass

    # Exit a parse tree produced by LanguageParser#numeric_unary_operator.
    def exitNumeric_unary_operator(self, ctx:LanguageParser.Numeric_unary_operatorContext):
        pass


    # Enter a parse tree produced by LanguageParser#multiplication_operator.
    def enterMultiplication_operator(self, ctx:LanguageParser.Multiplication_operatorContext):
        pass

    # Exit a parse tree produced by LanguageParser#multiplication_operator.
    def exitMultiplication_operator(self, ctx:LanguageParser.Multiplication_operatorContext):
        pass


    # Enter a parse tree produced by LanguageParser#addition_operator.
    def enterAddition_operator(self, ctx:LanguageParser.Addition_operatorContext):
        pass

    # Exit a parse tree produced by LanguageParser#addition_operator.
    def exitAddition_operator(self, ctx:LanguageParser.Addition_operatorContext):
        pass


    # Enter a parse tree produced by LanguageParser#comparison_operator.
    def enterComparison_operator(self, ctx:LanguageParser.Comparison_operatorContext):
        pass

    # Exit a parse tree produced by LanguageParser#comparison_operator.
    def exitComparison_operator(self, ctx:LanguageParser.Comparison_operatorContext):
        pass


    # Enter a parse tree produced by LanguageParser#and_operator.
    def enterAnd_operator(self, ctx:LanguageParser.And_operatorContext):
        pass

    # Exit a parse tree produced by LanguageParser#and_operator.
    def exitAnd_operator(self, ctx:LanguageParser.And_operatorContext):
        pass


    # Enter a parse tree produced by LanguageParser#or_operator.
    def enterOr_operator(self, ctx:LanguageParser.Or_operatorContext):
        pass

    # Exit a parse tree produced by LanguageParser#or_operator.
    def exitOr_operator(self, ctx:LanguageParser.Or_operatorContext):
        pass


    # Enter a parse tree produced by LanguageParser#atom.
    def enterAtom(self, ctx:LanguageParser.AtomContext):
        pass

    # Exit a parse tree produced by LanguageParser#atom.
    def exitAtom(self, ctx:LanguageParser.AtomContext):
        pass


    # Enter a parse tree produced by LanguageParser#declaration.
    def enterDeclaration(self, ctx:LanguageParser.DeclarationContext):
        pass

    # Exit a parse tree produced by LanguageParser#declaration.
    def exitDeclaration(self, ctx:LanguageParser.DeclarationContext):
        pass


    # Enter a parse tree produced by LanguageParser#var_type.
    def enterVar_type(self, ctx:LanguageParser.Var_typeContext):
        pass

    # Exit a parse tree produced by LanguageParser#var_type.
    def exitVar_type(self, ctx:LanguageParser.Var_typeContext):
        pass


    # Enter a parse tree produced by LanguageParser#assignment.
    def enterAssignment(self, ctx:LanguageParser.AssignmentContext):
        pass

    # Exit a parse tree produced by LanguageParser#assignment.
    def exitAssignment(self, ctx:LanguageParser.AssignmentContext):
        pass


    # Enter a parse tree produced by LanguageParser#literal.
    def enterLiteral(self, ctx:LanguageParser.LiteralContext):
        pass

    # Exit a parse tree produced by LanguageParser#literal.
    def exitLiteral(self, ctx:LanguageParser.LiteralContext):
        pass


    # Enter a parse tree produced by LanguageParser#printStatement.
    def enterPrintStatement(self, ctx:LanguageParser.PrintStatementContext):
        pass

    # Exit a parse tree produced by LanguageParser#printStatement.
    def exitPrintStatement(self, ctx:LanguageParser.PrintStatementContext):
        pass


    # Enter a parse tree produced by LanguageParser#readStatement.
    def enterReadStatement(self, ctx:LanguageParser.ReadStatementContext):
        pass

    # Exit a parse tree produced by LanguageParser#readStatement.
    def exitReadStatement(self, ctx:LanguageParser.ReadStatementContext):
        pass



del LanguageParser