from typing import Any

from antlr4 import NoViableAltException as ANTLRNoViableAltException
from antlr4 import RecognitionException as ANTLRRecognitionException
from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.Errors import FailedPredicateException as ANTLRFailedPredicateException
from antlr4.error.Errors import InputMismatchException as ANTLRInputMismatchException
from antlr4.Recognizer import Recognizer
from antlr4.Token import CommonToken

from antlr.LanguageLexer import LanguageLexer
from antlr.LanguageParser import LanguageParser
from interpreter.exceptions import (
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
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__()
        self.removeErrorListeners()
        listener = SyntaxErrorListener()
        self.addErrorListener(listener)


class CustomLexer(LanguageLexer, RecognizerWithCustomListener):
    pass


class CustomParser(LanguageParser, RecognizerWithCustomListener):
    pass
