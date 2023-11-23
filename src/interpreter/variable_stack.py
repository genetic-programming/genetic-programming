from interpreter.exceptions import LanguageFrameStackEmptyError, VariableRedeclarationError, VariableUndeclaredError
from interpreter.language_types.base_type import LanguageType


class VariableStack:
    def __init__(self) -> None:
        self.frames_stacks: list[dict[str, LanguageType]] = []

    @property
    def current_frame(self) -> dict[str, LanguageType]:
        return self.frames_stacks[-1]

    def add_frame(self) -> None:
        self.frames_stacks.append({})

    def pop_frame(self) -> None:
        if len(self.frames_stacks) == 0:
            raise LanguageFrameStackEmptyError(failed_event="pop subframe")
        self.frames_stacks.pop()

    def declare_var(self, var_type: type[LanguageType], var_name: str) -> LanguageType:
        if len(self.frames_stacks) == 0:
            raise LanguageFrameStackEmptyError(failed_event="declare variable")

        if self.current_frame.get(var_name) is not None:
            raise VariableRedeclarationError(var_name=var_name)

        var = var_type(None)
        self.current_frame[var_name] = var
        return var

    def get_var(self, var_name: str) -> LanguageType:
        if len(self.frames_stacks) == 0:
            raise LanguageFrameStackEmptyError(failed_event="get variable value")

        for frame in reversed(self.frames_stacks):
            var = frame.get(var_name)
            if var is not None:
                return var

        raise VariableUndeclaredError(name=var_name)
