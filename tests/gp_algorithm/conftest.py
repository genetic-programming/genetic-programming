from pathlib import Path
from typing import Callable

import pytest


@pytest.fixture()
def get_input_path() -> Callable[[str], str]:
    def _(source_file_name: str = "test") -> str:
        return str(Path(__file__).parent.parent / "inputs" / source_file_name)

    return _
