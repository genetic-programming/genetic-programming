import pytest

from gp_algorithm.grammar import NodeType
from gp_algorithm.nodes import LanguageNode


@pytest.mark.parametrize(
    ("node", "expected"),
    [
        pytest.param(
            LanguageNode(
                node_type=NodeType.LITERAL,
                value="1",
            ),
            "1",
            id="literal 1",
        ),
        pytest.param(
            LanguageNode(
                node_type=NodeType.EXPRESSION,
                children=[
                    LanguageNode(
                        node_type=NodeType.ATOM,
                        children=[
                            LanguageNode(
                                node_type=NodeType.LITERAL,
                                value="1",
                            ),
                        ],
                    ),
                ],
            ),
            "1",
            id="simple expression 1",
        ),
        pytest.param(
            LanguageNode(
                node_type=NodeType.LOOP_STATEMENT,
                children=[
                    LanguageNode(
                        node_type=NodeType.EXPRESSION,
                        children=[
                            LanguageNode(
                                node_type=NodeType.ATOM,
                                children=[
                                    LanguageNode(
                                        node_type=NodeType.LITERAL,
                                        value="1",
                                    ),
                                ],
                            ),
                        ],
                    ),
                    LanguageNode(node_type=NodeType.COMPOUND_STATEMENT),
                ],
            ),
            "while 1 {\n\n}",
            id="while 1 {}",
        ),
    ],
)
def test_cast_to_str(node: LanguageNode, expected: str) -> None:
    assert node.cast_to_str() == expected
