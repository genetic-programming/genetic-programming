from interpreter.language_types.base_type import LanguageType


class ProgramInput:
    def __init__(self, *args: LanguageType) -> None:
        self._literals: list[LanguageType] = list(args)

    def set_inputs(self, inputs: list[LanguageType]) -> None:
        self._literals = inputs

    def pop(self) -> LanguageType:
        try:
            return self._literals.pop()
        except IndexError:
            raise RuntimeError("Program input is empty.")


class ProgramOutput:
    def __init__(self, max_length: int = 100) -> None:
        self._data: list[str] = []
        self._max_length = max_length

    def append(self, output: str) -> None:
        if len(self._data) >= self._max_length:
            raise RuntimeError("Program output is too long.")
        self._data.append(output)

    def return_outputs(self) -> list[str]:
        return self._data
