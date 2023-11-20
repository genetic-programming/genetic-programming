from antlr4 import CommonTokenStream, InputStream
from antlr4.tree.Tree import ParseTreeWalker

from antlr.LanguageLexer import LanguageLexer
from antlr.LanguageListener import LanguageListener
from antlr.LanguageParser import LanguageParser
from antlr.LanguageVisitor import LanguageVisitor
from interpreter.exceptions import LanguageException


class Interpreter:
    def __init__(
        self,
        lexer: LanguageLexer,
        parser: LanguageParser,
        listener: LanguageListener,
        walker: ParseTreeWalker,
        visitor: LanguageVisitor,
        print_stacktraces: bool = False,
    ) -> None:
        self.lexer = lexer
        self.parser = parser
        self.listener = listener
        self.walker = walker
        self.visitor = visitor
        self._print_stacktraces = print_stacktraces

    def interpret_file(self, file_path: str) -> None:
        with open(file_path, "r") as file:
            data = file.read()
        input_stream = InputStream(data)
        self.interpret_stream(input_stream)

    def interpret_stream(self, input_stream: InputStream) -> None:
        self.set_input(input_stream)
        pe_ctx = self.get_primary_expression_ctx()
        if pe_ctx is None or self.parser.getNumberOfSyntaxErrors() > 0:
            return
        self.walk_and_visit_tree(pe_ctx)

    def set_input(self, input_stream: InputStream) -> None:
        self.lexer.inputStream = input_stream
        token_stream = CommonTokenStream(self.lexer)
        self.parser.setTokenStream(token_stream)

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

    def walk_and_visit_tree(self, ctx: LanguageParser.ProgramContext) -> None:
        try:
            self.walker.walk(self.listener, ctx)
            self.visitor.visitProgram(ctx)
        except LanguageException as exc:
            self._handle_exception(exc)

    def _handle_exception(self, exc: LanguageException) -> None:
        if self._print_stacktraces:
            raise exc
        print(exc)
