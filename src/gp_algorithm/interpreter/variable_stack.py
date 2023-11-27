from gp_algorithm.interpreter.exceptions import LanguageFrameStackEmptyError, VariableUndeclaredError
from gp_algorithm.interpreter.expression import Expression


class VariableStack:
    def __init__(self) -> None:
        self.frames_stacks: list[dict[str, Expression]] = []

    @property
    def current_frame(self) -> dict[str, Expression]:
        return self.frames_stacks[-1]

    def add_frame(self) -> None:
        self.frames_stacks.append({})

    def pop_frame(self) -> None:
        if len(self.frames_stacks) == 0:
            raise LanguageFrameStackEmptyError(failed_event="pop subframe")
        self.frames_stacks.pop()

    def set_var(self, var_name: str, expr: Expression) -> None:
        if len(self.frames_stacks) == 0:
            raise LanguageFrameStackEmptyError(failed_event="declare variable")

        for frame in self.frames_stacks:
            var = frame.get(var_name)
            if var is not None:
                frame[var_name] = expr

        self.current_frame[var_name] = expr

    def get_var(self, var_name: str) -> Expression:
        if len(self.frames_stacks) == 0:
            raise LanguageFrameStackEmptyError(failed_event="get variable value")

        for frame in reversed(self.frames_stacks):
            var = frame.get(var_name)
            if var is not None:
                return var

        raise VariableUndeclaredError(name=var_name)
