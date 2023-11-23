from typing import Any

from antlr4 import CommonTokenStream, InputStream
from antlr4 import NoViableAltException as ANTLRNoViableAltException
from antlr4 import RecognitionException as ANTLRRecognitionException
from antlr4 import TokenStream
from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.Errors import FailedPredicateException as ANTLRFailedPredicateException
from antlr4.error.Errors import InputMismatchException as ANTLRInputMismatchException
from antlr4.Recognizer import Recognizer
from antlr4.Token import CommonToken

from antlr.LanguageLexer import LanguageLexer
from antlr.LanguageParser import LanguageParser
from gp_algorithm.interpreter.exceptions import (
    FailedPredicateException,
    InputMismatchException,
    LanguageException,
    LanguageSyntaxError,
    NoViableAltException,
)


class SyntaxErrorListener(ErrorListener):
    def __init__(self) -> None:
        self.errors: list[LanguageException] = []

    def syntaxError(
        self,
        recognizer: Recognizer,
        offending_symbol: CommonToken,
        line: int,
        column: int,
        msg: str,
        e: ANTLRRecognitionException,
    ) -> None:
        if e is None:  # for extraneous input error
            return
        exc: LanguageException
        if isinstance(e, ANTLRNoViableAltException):
            exc = NoViableAltException(offending_symbol=offending_symbol.text)
        elif isinstance(e, ANTLRInputMismatchException):
            exc = InputMismatchException(extra_info=msg)
        elif isinstance(e, ANTLRFailedPredicateException):
            exc = FailedPredicateException(extra_info=msg)
        else:
            exc = LanguageSyntaxError(extra_info=msg)
        exc.start_line = line
        exc.stop_line = line
        exc.start_column = column
        exc.stop_column = column
        self.errors.append(exc)


class RecognizerWithCustomListener(Recognizer):
    def __init__(self, *args: Any) -> None:
        super().__init__()
        self.removeErrorListeners()
        listener = SyntaxErrorListener()
        self.addErrorListener(listener)


class Lexer(LanguageLexer, RecognizerWithCustomListener):
    pass


class Parser(LanguageParser, RecognizerWithCustomListener):
    def __init__(self, lexer: Lexer | None = None) -> None:
        super().__init__(TokenStream())
        self._lexer = lexer or Lexer()

    def parse_literals(self, data: list[str]) -> list[LanguageParser.LiteralContext]:
        return [self.parse_literal(literal) for literal in data]

    def parse_literal(self, literal: str) -> LanguageParser.LiteralContext:
        self.set_token_stream(data=literal)
        return self.literal()

    def parse_program(self, data: str) -> LanguageParser.ProgramContext:
        self.set_token_stream(data=data)
        return self.program()

    def set_token_stream(self, data: str) -> None:
        self._lexer.inputStream = InputStream(data)
        token_stream = CommonTokenStream(self._lexer)
        self.setTokenStream(token_stream)

    def get_errors(self) -> list[LanguageException]:
        errors = []
        for listener in [
            *self._lexer.getErrorListenerDispatch().delegates,
            *self.getErrorListenerDispatch().delegates,
        ]:
            errors.extend(listener.errors)

        if self.getNumberOfSyntaxErrors() > 0:
            errors.append(LanguageException())

        return errors
