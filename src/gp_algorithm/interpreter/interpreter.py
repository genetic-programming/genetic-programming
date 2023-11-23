from antlr.LanguageParser import LanguageParser
from gp_algorithm.interpreter.exceptions import LanguageException
from gp_algorithm.interpreter.language_types.base_type import LanguageType
from gp_algorithm.interpreter.parser import Parser
from gp_algorithm.interpreter.visitor import Visitor


class Interpreter:
    def __init__(
        self,
        parser: Parser | None = None,
        visitor: Visitor | None = None,
        print_stacktraces: bool = False,
    ) -> None:
        self._parser = parser or Parser()
        self._visitor = visitor or Visitor()
        self._print_stacktraces = print_stacktraces

    def interpret_inputs(self, input_strings: list[list[str]]) -> list[list[LanguageType]]:
        return [self.interpret_input(input_string) for input_string in input_strings]

    def interpret_input(self, input_strings: list[str]) -> list[LanguageType]:
        literal_contexts = self._parser.parse_literals(input_strings)
        return [self._visitor.visitLiteral(literal_ctx) for literal_ctx in literal_contexts]

    def interpret_file(self, file_path: str, program_input: list[LanguageType]) -> list[str]:
        with open(file_path, "r") as file:
            data = file.read()

        return self.interpret_str(data=data, program_input=program_input)

    def interpret_str(self, data: str, program_input: list[LanguageType]) -> list[str]:
        tree = self.parse_str(data=data)
        return self.interpret_tree(tree=tree, program_input=program_input)

    def parse_str(self, data: str) -> Parser.StatementsContext:
        tree = self._parser.parse_program(data=data)
        errors = self._parser.get_errors()
        for error in errors:
            self._handle_exception(error)
        return tree

    def _handle_exception(self, exc: LanguageException) -> None:
        if self._print_stacktraces:
            raise exc
        print(exc)  # noqa: T201

    def interpret_tree(
        self,
        tree: LanguageParser.StatementsContext,
        program_input: list[LanguageType],
    ) -> list[str]:
        return self._visitor.visit_tree(tree=tree, program_input=program_input)
