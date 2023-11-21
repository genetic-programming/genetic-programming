from interpreter.exceptions import (
    LanguageFrameStackEmptyError,
    LanguageSubFrameStackEmptyError,
    VariableRedeclarationError,
    VariableUndeclaredError,
)
from interpreter.language_types.base_type import LanguageType


class Frame:
    """
    Used as frame for function.
    """

    def __init__(self, f_name: str) -> None:
        self.function_name: str = f_name
        self.subframes: list[SubFrame] = []


class SubFrame:
    """
    Used as frame for body.
    """

    def __init__(self) -> None:
        self.variables: dict[str, LanguageType] = {}


class VariableStack:
    def __init__(self) -> None:
        self.frames: list[Frame] = []

    def append_frame(self, func_name: str) -> None:
        func_frame = Frame(func_name)
        self.frames.append(func_frame)

    def pop_frame(self) -> None:
        if len(self.frames) == 0:
            raise LanguageFrameStackEmptyError(failed_event="pop frame")
        self.frames.pop()

    def append_subframe(self) -> None:
        if len(self.frames) == 0:
            raise LanguageFrameStackEmptyError(failed_event="append subframe")
        curr_frame = self.frames[-1]
        subframe = SubFrame()
        curr_frame.subframes.append(subframe)

    def pop_subframe(self) -> None:
        if len(self.frames) == 0:
            raise LanguageFrameStackEmptyError(failed_event="pop subframe")
        curr_frame = self.frames[-1]
        if len(curr_frame.subframes) == 0:
            raise LanguageSubFrameStackEmptyError(failed_event="pop subframe")
        curr_frame.subframes.pop()

    def declare_variable(self, var_type: type[LanguageType], var_name: str) -> LanguageType:
        if len(self.frames) == 0:
            raise LanguageFrameStackEmptyError(failed_event="declare variable")
        curr_frame = self.frames[-1]
        if len(curr_frame.subframes) == 0:
            raise LanguageSubFrameStackEmptyError(failed_event="declare variable")
        curr_subframe = curr_frame.subframes[-1]

        if curr_subframe.variables.get(var_name) is not None:
            raise VariableRedeclarationError(var_name=var_name)

        var = var_type(None)
        curr_subframe.variables.update({var_name: var})

        return var

    def get_curr_function_name(self) -> str:
        if len(self.frames) == 0:
            raise LanguageFrameStackEmptyError(failed_event="get current function name")
        return self.frames[-1].function_name

    def get_var(self, var_name: str) -> LanguageType:
        if len(self.frames) == 0:
            raise LanguageFrameStackEmptyError(failed_event="get variable value")
        curr_frame = self.frames[-1]
        if len(curr_frame.subframes) == 0:
            raise LanguageSubFrameStackEmptyError(failed_event="get variable value")

        for frame in reversed(curr_frame.subframes):
            var = frame.variables.get(var_name)
            if var is not None:
                return var
        raise VariableUndeclaredError(name=var_name)
