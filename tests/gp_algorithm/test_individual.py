from typing import Callable

import pytest

from gp_algorithm.individual import Individual
from gp_algorithm.node import LanguageNode
from gp_algorithm.tree_config import NodeType
from gp_algorithm.utils import build_individual_from_file


@pytest.mark.parametrize(
    ("file_name", "expected_individual"),
    [
        pytest.param(
            "test_1",
            Individual(
                value="{0} {1}",
                children=[
                    LanguageNode(
                        value="{0} = {1};",
                        node_type=NodeType.STATEMENT,
                        children=[
                            LanguageNode(
                                value="v1",
                                node_type=NodeType.VARIABLE_NAME,
                            ),
                            LanguageNode(
                                value="10",
                                node_type=NodeType.LITERAL_INT,
                            ),
                        ],
                    ),
                    LanguageNode(
                        value="{0} = {1};",
                        node_type=NodeType.STATEMENT,
                        children=[
                            LanguageNode(
                                value="v0",
                                node_type=NodeType.VARIABLE_NAME,
                            ),
                            LanguageNode(
                                value="true",
                                node_type=NodeType.LITERAL_BOOL,
                            ),
                        ],
                    ),
                ],
            ),
            id="v1 = 10; v0 = true;",
        ),
        pytest.param(
            "test_2",
            Individual(
                value="{0}",
                children=[
                    LanguageNode(
                        value="while {0} {{{1}}}",
                        node_type=NodeType.STATEMENT,
                        children=[
                            LanguageNode(
                                value="true",
                                node_type=NodeType.LITERAL_BOOL,
                            ),
                            LanguageNode(node_type=NodeType.STATEMENTS),
                        ],
                    ),
                ],
            ),
            id="while true {}",
        ),
        pytest.param(
            "test_3",
            Individual(
                value="{0}",
                children=[
                    LanguageNode(
                        value="if {0} {{{1}}} else {{{2}}}",
                        node_type=NodeType.STATEMENT,
                        children=[
                            LanguageNode(
                                value="true",
                                node_type=NodeType.LITERAL_BOOL,
                            ),
                            LanguageNode(node_type=NodeType.STATEMENTS),
                            LanguageNode(node_type=NodeType.STATEMENTS),
                        ],
                    ),
                ],
            ),
            id="if true {} else {}",
        ),
        pytest.param(
            "test_4",
            Individual(
                value="{0}",
                children=[
                    LanguageNode(
                        value="print {0};",
                        node_type=NodeType.STATEMENT,
                        children=[
                            LanguageNode(
                                value="v0",
                                node_type=NodeType.VARIABLE_NAME,
                            ),
                        ],
                    ),
                ],
            ),
            id="print v0;",
        ),
    ],
)
def test_build_individual_from_file(
    file_name: str,
    expected_individual: Individual,
    get_input_path: Callable[[str], str],
) -> None:
    input_path = get_input_path(file_name)
    individual = build_individual_from_file(input_path)
    expected_str = expected_individual.build_str()
    actual_str = individual.build_str()
    assert actual_str == expected_str, actual_str
