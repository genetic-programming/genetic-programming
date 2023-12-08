import pytest

from gp_algorithm.grammar import NodeType
from gp_algorithm.node import LanguageNode


@pytest.mark.parametrize(
    ("node", "expected"),
    [
        pytest.param(
            LanguageNode(
                node_type=NodeType.LITERAL_INT,
                value="1",
            ),
            "1",
            id="literal 1",
        ),
        pytest.param(
            LanguageNode(
                value="{0}",
                node_type=NodeType.EXPRESSION,
                children=[
                    LanguageNode(
                        node_type=NodeType.LITERAL_INT,
                        value="1",
                    ),
                ],
            ),
            "1",
            id="simple expression 1",
        ),
        pytest.param(
            LanguageNode(
                value="while {0} {{{1}}}",
                node_type=NodeType.STATEMENT,
                children=[
                    LanguageNode(
                        value="{0}",
                        node_type=NodeType.EXPRESSION,
                        children=[
                            LanguageNode(
                                node_type=NodeType.LITERAL_INT,
                                value="1",
                            ),
                        ],
                    ),
                    LanguageNode(node_type=NodeType.STATEMENTS),
                ],
            ),
            "while 1 {}",
            id="while 1 {}",
        ),
    ],
)
def test_cast_to_str(node: LanguageNode, expected: str) -> None:
    assert node.build_str() == expected
