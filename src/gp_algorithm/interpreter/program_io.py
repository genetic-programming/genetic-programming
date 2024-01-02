from gp_algorithm.interpreter.exceptions import EmptyInputException, OutputOverflow
from gp_algorithm.interpreter.expression import Expression


class ProgramInput:
    def __init__(self, *args: Expression) -> None:
        self._literals: list[Expression] = list(args)

    def set_inputs(self, inputs: list[Expression]) -> None:
        self._literals = inputs.copy()

    def pop(self) -> Expression:
        try:
            return self._literals.pop(0)
        except IndexError:
            raise EmptyInputException()


class ProgramOutput:
    def __init__(self, max_length: int = 100) -> None:
        self._data: list[str] = []
        self._max_length = max_length

    def append(self, output: str) -> None:
        if len(self._data) >= self._max_length:
            raise OutputOverflow()
        self._data.append(output)

    def return_outputs(self) -> list[str]:
        data = self._data
        self._data = []
        return data
