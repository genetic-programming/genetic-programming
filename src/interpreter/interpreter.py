from antlr4 import CommonTokenStream, InputStream, TokenStream
from antlr4.tree.Tree import ParseTreeWalker

from antlr.LanguageLexer import LanguageLexer
from antlr.LanguageListener import LanguageListener
from antlr.LanguageParser import LanguageParser
from interpreter.exceptions import LanguageException
from interpreter.language_types.base_type import LanguageType
from interpreter.listener import Listener
from interpreter.recognizers import CustomLexer, CustomParser
from interpreter.variable_stack import VariableStack
from interpreter.visitor import Visitor


class Interpreter:
    def __init__(
        self,
        lexer: LanguageLexer,
        parser: LanguageParser,
        listener: LanguageListener,
        walker: ParseTreeWalker,
        visitor: Visitor,
        print_stacktraces: bool = False,
    ) -> None:
        self.lexer = lexer
        self.parser = parser
        self.listener = listener
        self.walker = walker
        self.visitor = visitor
        self._print_stacktraces = print_stacktraces

    def interpret_file(self, file_path: str, inputs: list[LanguageType]) -> list[str]:
        with open(file_path, "r") as file:
            data = file.read()
        return self.interpret_str(data=data, inputs=inputs)

    def interpret_str(self, data: str, inputs: list[LanguageType]) -> list[str]:
        return self.interpret_stream(
            input_stream=InputStream(data),
            inputs=inputs,
        )

    def interpret_stream(self, input_stream: InputStream, inputs: list[LanguageType]) -> list[str]:
        self._set_input(input_stream=input_stream, program_inputs=inputs)
        program_ctx = self.get_primary_expression_ctx()
        if program_ctx is None or self.parser.getNumberOfSyntaxErrors() > 0:
            raise RuntimeError("Syntax error.")
        return self.walk_and_visit_tree(ctx=program_ctx)

    def _set_input(
        self,
        input_stream: InputStream,
        program_inputs: list[LanguageType],
    ) -> None:
        self.lexer.inputStream = input_stream
        token_stream = CommonTokenStream(self.lexer)
        self.parser.setTokenStream(token_stream)
        self.visitor.program_input = program_inputs

    def get_primary_expression_ctx(self) -> LanguageParser.ProgramContext | None:
        primary_context = self.parser.program()
        is_any_error = self.is_any_lexer_or_parser_error()
        if is_any_error:
            return None
        return primary_context

    def is_any_lexer_or_parser_error(self) -> bool:
        error_listeners = [
            *self.lexer.getErrorListenerDispatch().delegates,
            *self.parser.getErrorListenerDispatch().delegates,
        ]
        errors = []
        for listener in error_listeners:
            errors.extend(listener.errors)
        if not errors:
            return False
        for error in errors:
            self._handle_exception(error)
        return True

    def walk_and_visit_tree(self, ctx: LanguageParser.ProgramContext) -> list[str]:
        self.walker.walk(listener=self.listener, t=ctx)
        self.visitor.visitProgram(ctx=ctx)
        return self.visitor.program_output

    def _handle_exception(self, exc: LanguageException) -> None:
        if self._print_stacktraces:
            raise exc
        print(exc)  # noqa: T201


def create_interpreter(print_stacktraces: bool) -> Interpreter:
    variable_stack = VariableStack()
    return Interpreter(
        CustomLexer(),
        CustomParser(input=TokenStream()),
        Listener(variable_stack=variable_stack),
        ParseTreeWalker(),
        Visitor(variable_stack=variable_stack),
        print_stacktraces=print_stacktraces,
    )
