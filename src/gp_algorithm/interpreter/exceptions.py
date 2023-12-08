from typing import Any

from antlr4 import ParserRuleContext


class LanguageException(Exception):
    message_schema: str = "Error occurred."
    attrs: dict[str, Any] = {}

    def __init__(self, **kwargs: Any) -> None:
        self.attrs.update(kwargs)
        self.start_line: int | None = None
        self.stop_line: int | None = None
        self.start_column: int | None = None
        self.stop_column: int | None = None

    @property
    def message(self) -> str:
        return self.message_schema.format(**self.attrs)

    def __str__(self) -> str:
        line_info = self.line_info()
        column_info = self.column_info()
        if not line_info:
            return f"\033[91mError!!!\n\t{self.message}\033[0m"
        elif not column_info:
            return f"\033[91mError {line_info}!!!\n\t{self.message}\033[0m"
        else:
            return f"\033[91mError {line_info}, {column_info}!!!\n\t{self.message}\033[0m"

    def line_info(self) -> str:
        if self.start_line is None or self.stop_line is None:
            return ""
        if self.start_line == self.stop_line:
            return f"line: {self.start_line}"
        return f"lines: {self.start_line}-{self.stop_line}"

    def column_info(self) -> str:
        if self.start_column is None or self.stop_column is None:
            return ""
        if self.start_column == self.stop_column:
            return f"column: {self.start_column}"
        return f"columns: {self.start_column}-{self.stop_column}"

    def inject_context_to_exc(self, ctx: "ParserRuleContext") -> None:
        if self.start_line is not None or self.stop_line is not None:
            return
        self.start_line = ctx.start.line
        self.stop_line = ctx.stop.line
        self.start_column = ctx.start.column
        self.stop_column = ctx.stop.column


# LEXER EXCEPTIONS
class RecognitionError(LanguageException):
    message_schema = "Recognition error. {extra_info}"
    attrs = {"extra_info": "not specified"}


class NoViableAltException(RecognitionError):
    message_schema = "No viable alternative at input '{offending_symbol}'."
    attrs = {"offending_symbol": "not specified"}


class InputMismatchException(RecognitionError):
    pass


class FailedPredicateException(RecognitionError):
    pass


# PARSER EXCEPTIONS
class LanguageSyntaxError(LanguageException):
    message_schema = "Syntax error. {extra_info}"
    attrs = {"extra_info": "not specified"}


# VISITOR EXCEPTIONS
class LanguageZeroDivisionError(LanguageException):
    message_schema = "Division by zero."
    attrs = {}


class TooManyStatements(LanguageException):
    message_schema = "Too many statements."
    attrs = {}
