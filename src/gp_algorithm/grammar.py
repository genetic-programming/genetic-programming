from __future__ import annotations

from enum import auto, StrEnum

from pydantic import BaseModel


class NodeType(StrEnum):
    STATEMENTS = auto()
    STATEMENT = auto()
    EXPRESSION = auto()
    UNARY_OPERATOR = auto()
    BINARY_OPERATOR = auto()
    VARIABLE_NAME = auto()
    LITERAL_BOOL = auto()
    LITERAL_INT = auto()
    LITERAL_STR = auto()


class NodeSuccessor(BaseModel):
    weight: int = 1
    template: str = "{0}"
    children: list[NodeType]


class NodeData(BaseModel):
    growable: bool = False
    allowed_swaps: set[NodeType] = set()
    successors: list[NodeSuccessor] = []


GRAMMAR = {
    NodeType.STATEMENTS: NodeData(
        growable=True,
        successors=[
            NodeSuccessor(children=[NodeType.STATEMENT]),
        ],
    ),
    NodeType.STATEMENT: NodeData(
        allowed_swaps={NodeType.STATEMENT},
        successors=[
            NodeSuccessor(
                weight=2,
                template="{0} = {1};",
                children=[NodeType.VARIABLE_NAME, NodeType.EXPRESSION],
            ),
            NodeSuccessor(
                weight=2,
                template="print {0};",
                children=[NodeType.EXPRESSION],
            ),
            NodeSuccessor(
                weight=2,
                template="if {0} {{{1}}} else {{{2}}}",
                children=[NodeType.EXPRESSION, NodeType.STATEMENTS, NodeType.STATEMENTS],
            ),
            NodeSuccessor(
                weight=2,
                template="while {0} {{{1}}}",
                children=[NodeType.EXPRESSION, NodeType.STATEMENTS],
            ),
            NodeSuccessor(
                weight=0,
                template="{{{0}}}",
                children=[NodeType.STATEMENTS],
            ),
        ],
    ),
    NodeType.EXPRESSION: NodeData(
        allowed_swaps={
            NodeType.EXPRESSION,
            NodeType.LITERAL_BOOL,
            NodeType.LITERAL_INT,
            NodeType.LITERAL_STR,
        },
        successors=[
            NodeSuccessor(
                weight=1,
                template="{0} {1}",
                children=[NodeType.UNARY_OPERATOR, NodeType.EXPRESSION],
            ),
            NodeSuccessor(
                weight=2,
                template="{0} {1} {2}",
                children=[NodeType.EXPRESSION, NodeType.BINARY_OPERATOR, NodeType.EXPRESSION],
            ),
            NodeSuccessor(
                weight=2,
                template="({0})",
                children=[NodeType.EXPRESSION],
            ),
            NodeSuccessor(
                weight=4,
                children=[NodeType.VARIABLE_NAME],
            ),
            NodeSuccessor(
                weight=2,
                children=[NodeType.LITERAL_BOOL],
            ),
            NodeSuccessor(
                weight=2,
                children=[NodeType.LITERAL_INT],
            ),
            NodeSuccessor(
                weight=0,
                children=[NodeType.LITERAL_STR],
            ),
        ],
    ),
    NodeType.UNARY_OPERATOR: NodeData(
        allowed_swaps={NodeType.UNARY_OPERATOR},
    ),
    NodeType.BINARY_OPERATOR: NodeData(
        allowed_swaps={NodeType.BINARY_OPERATOR},
    ),
    NodeType.VARIABLE_NAME: NodeData(
        allowed_swaps={NodeType.VARIABLE_NAME},
    ),
    NodeType.LITERAL_BOOL: NodeData(
        allowed_swaps={
            NodeType.LITERAL_INT,
            NodeType.LITERAL_BOOL,
            NodeType.LITERAL_STR,
        },
    ),
    NodeType.LITERAL_INT: NodeData(
        allowed_swaps={
            NodeType.LITERAL_INT,
            NodeType.LITERAL_BOOL,
            NodeType.LITERAL_STR,
        },
    ),
    NodeType.LITERAL_STR: NodeData(
        allowed_swaps={
            NodeType.LITERAL_INT,
            NodeType.LITERAL_BOOL,
            NodeType.LITERAL_STR,
        },
    ),
}
