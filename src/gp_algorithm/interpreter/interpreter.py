from antlr.LanguageParser import LanguageParser
from gp_algorithm.interpreter.expression import Expression
from gp_algorithm.interpreter.parser import Parser
from gp_algorithm.interpreter.visitor import Visitor


class Interpreter:
    def __init__(
        self,
        parser: Parser | None = None,
        visitor: Visitor | None = None,
    ) -> None:
        self._parser = parser or Parser()
        self._visitor = visitor or Visitor()

    def parse_str(self, data: str) -> Parser.StatementsContext:
        return self._parser.parse_str(data=data)

    def interpret_inputs(self, input_strings: list[list[str]]) -> list[list[Expression]]:
        return [self.interpret_input(input_string) for input_string in input_strings]

    def interpret_input(self, input_strings: list[str]) -> list[Expression]:
        expression_contexts = self._parser.parse_expressions(input_strings)
        return [self._visitor.visitExpression(expression_ctx) for expression_ctx in expression_contexts]

    def interpret_file(self, file_path: str, program_input: list[Expression]) -> list[str]:
        with open(file_path, "r") as file:
            data = file.read()

        return self.interpret_str(data=data, program_input=program_input)

    def interpret_str(self, data: str, program_input: list[Expression]) -> list[str]:
        tree = self._parser.parse_str(data=data)
        return self.interpret_tree(tree=tree, program_input=program_input)

    def interpret_tree(
        self,
        tree: LanguageParser.StatementsContext,
        program_input: list[Expression],
    ) -> list[str]:
        return self._visitor.visit_tree(tree=tree, program_input=program_input)
