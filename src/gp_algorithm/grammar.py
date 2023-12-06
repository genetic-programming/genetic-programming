from __future__ import annotations

from enum import auto, StrEnum

from pydantic import BaseModel


class NodeType(StrEnum):
    PROGRAM = auto()
    STATEMENT = auto()

    LINE = auto()
    CONDITIONAL_STATEMENT = auto()
    LOOP_STATEMENT = auto()
    COMPOUND_STATEMENT = auto()

    EXPRESSION = auto()
    DECLARATION = auto()
    ASSIGNMENT = auto()
    PRINT_STATEMENT = auto()
    READ_STATEMENT = auto()

    VAR_NAME = auto()
    LITERAL = auto()
    ATOM = auto()


class NodeData(BaseModel):
    growable: bool = False
    successors: list[list[NodeType]] = []
    possible_types: list[str] = []
    allowed_swaps: set[NodeType] = set()
    representation: str = "{0}"


GRAMMAR = {
    NodeType.PROGRAM: NodeData(
        growable=True,
        successors=[[NodeType.STATEMENT]],
    ),
    NodeType.STATEMENT: NodeData(
        successors=[
            [NodeType.LINE],
            [NodeType.CONDITIONAL_STATEMENT],
            [NodeType.LOOP_STATEMENT],
            # [NodeType.COMPOUND_STATEMENT],
        ],
    ),
    NodeType.LINE: NodeData(
        successors=[
            [NodeType.EXPRESSION],
            [NodeType.ASSIGNMENT],
            [NodeType.PRINT_STATEMENT],
            [NodeType.READ_STATEMENT],
        ],
        representation="{0};",
    ),
    NodeType.CONDITIONAL_STATEMENT: NodeData(
        successors=[
            [NodeType.EXPRESSION, NodeType.COMPOUND_STATEMENT],
            # [NodeType.EXPRESSION, NodeType.COMPOUND_STATEMENT, NodeType.COMPOUND_STATEMENT],
        ],
        representation="if {0} {1}",
        # representation="if {0} {1} else {2}",
    ),
    NodeType.LOOP_STATEMENT: NodeData(
        successors=[[NodeType.EXPRESSION, NodeType.COMPOUND_STATEMENT]],
        representation="while {0} {1}",
    ),
    NodeType.COMPOUND_STATEMENT: NodeData(
        growable=True,
        successors=[[NodeType.STATEMENT]],
        representation="{}",
    ),
    NodeType.EXPRESSION: NodeData(
        successors=[[NodeType.ATOM]],
    ),
    NodeType.PRINT_STATEMENT: NodeData(
        successors=[[NodeType.EXPRESSION]],
        representation="print {0}",
    ),
    NodeType.READ_STATEMENT: NodeData(
        successors=[[NodeType.DECLARATION]],
        representation="{0} = read",
    ),
    NodeType.ATOM: NodeData(
        successors=[
            [NodeType.VAR_NAME],
            [NodeType.LITERAL],
        ],
    ),
    NodeType.ASSIGNMENT: NodeData(
        successors=[
            [NodeType.DECLARATION, NodeType.VAR_NAME],
            [NodeType.DECLARATION, NodeType.EXPRESSION],
        ],
        representation="{0} = {1}",
    ),
    NodeType.DECLARATION: NodeData(possible_types=["variable declaration"]),
    NodeType.VAR_NAME: NodeData(possible_types=["variable name"]),
    NodeType.LITERAL: NodeData(possible_types=["boolean", "integer", "string"]),
}
