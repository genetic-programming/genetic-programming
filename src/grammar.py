from __future__ import annotations

from enum import StrEnum, auto
from string import ascii_lowercase

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
    
    VAR_TYPE = auto()
    VAR_NAME = auto()
    LITERAL = auto()
    ATOM = auto()


class NodeData(BaseModel):
    growable: bool = False
    successors: list[list[NodeType]] = []
    possible_values: list[str] = []
    allowed_swaps: set[NodeType] = set()


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
            [NodeType.COMPOUND_STATEMENT],
        ],
    ),
    NodeType.LINE: NodeData(
        successors=[
            [NodeType.EXPRESSION],
            [NodeType.DECLARATION],
            [NodeType.ASSIGNMENT],
            [NodeType.PRINT_STATEMENT],
            [NodeType.READ_STATEMENT],
        ],
    ),
    NodeType.CONDITIONAL_STATEMENT: NodeData(
        successors=[
            [NodeType.EXPRESSION, NodeType.COMPOUND_STATEMENT],
            [NodeType.EXPRESSION, NodeType.COMPOUND_STATEMENT, NodeType.COMPOUND_STATEMENT],
        ],
    ),
    NodeType.LOOP_STATEMENT: NodeData(
        successors=[[NodeType.EXPRESSION, NodeType.COMPOUND_STATEMENT]],
    ),
    NodeType.COMPOUND_STATEMENT: NodeData(
        growable=True,
        successors=[[NodeType.STATEMENT]],
    ),
    NodeType.EXPRESSION: NodeData(
        successors=[[NodeType.ATOM]],
    ),
    NodeType.PRINT_STATEMENT: NodeData(successors=[[NodeType.EXPRESSION]]),
    NodeType.READ_STATEMENT: NodeData(successors=[[NodeType.VAR_NAME]]),
    NodeType.ATOM: NodeData(
        successors=[
            [NodeType.VAR_NAME],
            [NodeType.LITERAL],
        ],
    ),
    NodeType.DECLARATION: NodeData(successors=[[NodeType.VAR_TYPE, NodeType.VAR_NAME]]),
    NodeType.VAR_TYPE: NodeData(possible_values=["int", "bool", "float"]),
    NodeType.ASSIGNMENT: NodeData(
        successors=[
            [NodeType.DECLARATION, NodeType.VAR_NAME],
            [NodeType.DECLARATION, NodeType.EXPRESSION]
        ],
    ),
    NodeType.VAR_NAME: NodeData(possible_values=list(ascii_lowercase)),
    NodeType.LITERAL: NodeData(possible_values=["true", "false", "1", "2", "3", ".5", ".1", "1.5"]),
}
