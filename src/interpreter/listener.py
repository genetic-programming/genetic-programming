from antlr.LanguageListener import LanguageListener
from antlr.LanguageParser import LanguageParser
from interpreter.decorators import handle_exception
from interpreter.types.base_type import LanguageType
from interpreter.types.boolean import BooleanType
from interpreter.types.float import FloatType
from interpreter.types.integer import IntegerType
from interpreter.variable_stack import VariableStack


class Listener(LanguageListener):
    def __init__(self, variable_stack: VariableStack) -> None:
        self.variable_stack = variable_stack

    @handle_exception
    def enterCompoundStatement(self, ctx: LanguageParser.CompoundStatementContext) -> None:
        self.variable_stack.append_subframe()

    @handle_exception
    def exitCompoundStatement(self, ctx: LanguageParser.CompoundStatementContext) -> None:
        self.variable_stack.pop_subframe()

    @handle_exception
    def enterDeclaration(self, ctx: LanguageParser.DeclarationContext) -> None:
        var_type_ctx: LanguageParser.VarTypeContext = ctx.varType()
        var_type: type[LanguageType]

        if var_type_ctx.Float():
            var_type = FloatType
        elif var_type_ctx.Int():
            var_type = IntegerType
        elif var_type_ctx.Bool():
            var_type = BooleanType
        else:
            raise NotImplementedError("Unknown var type")

        var_name = ctx.VARIABLE_NAME().symbol.text
        self.variable_stack.declare_variable(var_type, var_name)
