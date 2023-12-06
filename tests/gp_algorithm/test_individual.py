from typing import Callable

import pytest

from gp_algorithm.grammar import NodeType
from gp_algorithm.individual import Individual
from gp_algorithm.nodes import LanguageNode
from gp_algorithm.utils import build_individual_from_file


@pytest.mark.parametrize(
    ("file_name", "expected_individual"),
    [
        pytest.param(
            "test_1",
            Individual(
                children=[
                    LanguageNode(
                        node_type=NodeType.STATEMENT,
                        children=[
                            LanguageNode(
                                node_type=NodeType.LINE,
                                children=[
                                    LanguageNode(
                                        node_type=NodeType.ASSIGNMENT,
                                        children=[
                                            LanguageNode(
                                                node_type=NodeType.VAR_NAME,
                                                value="v1",
                                            ),
                                            LanguageNode(
                                                node_type=NodeType.LITERAL,
                                                value="10",
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    LanguageNode(
                        node_type=NodeType.STATEMENT,
                        children=[
                            LanguageNode(
                                node_type=NodeType.LINE,
                                children=[
                                    LanguageNode(
                                        node_type=NodeType.ASSIGNMENT,
                                        children=[
                                            LanguageNode(
                                                node_type=NodeType.VAR_NAME,
                                                value="v0",
                                            ),
                                            LanguageNode(
                                                node_type=NodeType.LITERAL,
                                                value="true",
                                            ),
                                        ],
                                    ),
                                ],
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
                children=[
                    LanguageNode(
                        node_type=NodeType.STATEMENT,
                        children=[
                            LanguageNode(
                                node_type=NodeType.LOOP_STATEMENT,
                                children=[
                                    LanguageNode(
                                        node_type=NodeType.EXPRESSION,
                                        children=[
                                            LanguageNode(
                                                node_type=NodeType.LITERAL,
                                                value="true",
                                            ),
                                        ],
                                    ),
                                    LanguageNode(node_type=NodeType.COMPOUND_STATEMENT),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            id="while true {}",
        ),
        pytest.param(
            "test_3",
            Individual(
                children=[
                    LanguageNode(
                        node_type=NodeType.STATEMENT,
                        children=[
                            LanguageNode(
                                node_type=NodeType.CONDITIONAL_STATEMENT,
                                children=[
                                    LanguageNode(
                                        node_type=NodeType.EXPRESSION,
                                        children=[
                                            LanguageNode(
                                                node_type=NodeType.LITERAL,
                                                value="true",
                                            ),
                                        ],
                                    ),
                                    LanguageNode(node_type=NodeType.COMPOUND_STATEMENT),
                                    LanguageNode(node_type=NodeType.COMPOUND_STATEMENT),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            id="if true {} else {}",
        ),
        pytest.param(
            "test_4",
            Individual(
                children=[
                    LanguageNode(
                        node_type=NodeType.STATEMENT,
                        children=[
                            LanguageNode(
                                node_type=NodeType.LINE,
                                children=[
                                    LanguageNode(
                                        node_type=NodeType.PRINT_STATEMENT,
                                        children=[
                                            LanguageNode(
                                                node_type=NodeType.EXPRESSION,
                                                children=[
                                                    LanguageNode(
                                                        node_type=NodeType.VAR_NAME,
                                                        value="v0",
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            id="print v0;",
        ),
        pytest.param(
            "test_5",
            Individual(
                children=[
                    LanguageNode(
                        node_type=NodeType.STATEMENT,
                        children=[
                            LanguageNode(
                                node_type=NodeType.LINE,
                                children=[
                                    LanguageNode(node_type=NodeType.READ_STATEMENT),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            id="read;",
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
    expected_str = expected_individual.cast_to_str()
    actual_str = individual.cast_to_str()
    assert actual_str == expected_str, actual_str
