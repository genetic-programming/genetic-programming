from __future__ import annotations

import random
from enum import StrEnum, auto
from typing import Any

from anytree import Node, PreOrderIter
from pydantic import BaseModel


class NodeType(StrEnum):
    PROGRAM = auto()
    STATEMENT = auto()
    DECLARATION = auto()
    VAR_TYPE = auto()
    VAR_NAME = auto()


class NodeData(BaseModel):
    mutations_allowed: bool = True
    growable: bool = False
    grammar_successors: list[list[NodeType]] = []
    possible_values: list[str] = []
    

GRAMMAR = {
    NodeType.PROGRAM: NodeData(growable=True, grammar_successors=[[NodeType.STATEMENT]]),
    NodeType.STATEMENT: NodeData(grammar_successors=[[NodeType.DECLARATION]]),
    NodeType.DECLARATION: NodeData(grammar_successors=[[NodeType.VAR_TYPE, NodeType.VAR_NAME]]),
    NodeType.VAR_TYPE: NodeData(possible_values=["int", "bool", "float"]),
    NodeType.VAR_NAME: NodeData(possible_values=["a", "b", "c"]),
}


class LanguageNode(Node):
    def __init__(
        self,
        node_type: NodeType,
        value: str | None = None,
        parent: LanguageNode | None = None,
        children: list[LanguageNode] | None = None,
        **kwargs: Any,
    ) -> None:
        self.node_type = node_type
        self.value = value
        super().__init__(
            name=self.node_title,
            parent=parent,
            children=children,
            **kwargs,
        )
    
    @property
    def node_title(self) -> str:
        if self.value:
            return f"{self.node_type}: {self.value}"
        return self.node_type
    
    def grow(self) -> None:
        growable_descendants = PreOrderIter(self, filter_=lambda node: GRAMMAR[node.node_type].growable)
        parent_node: LanguageNode = random.choice(list(growable_descendants))
        parent_node.random_init()
        
    def random_init(self) -> None:
        successors = GRAMMAR[self.node_type].grammar_successors
        if not successors:
            return
        
        new_nodes_types = random.choice(successors)
        for new_node_type in new_nodes_types:
            possible_values = GRAMMAR[new_node_type].possible_values
            value = random.choice(possible_values) if possible_values else None
            new_node = LanguageNode(
                node_type=new_node_type,
                value=value,
                parent=self,
            )
            new_node.random_init()
            

class Individual(LanguageNode):
    def __init__(self) -> None:
        super().__init__(
            node_type=NodeType.PROGRAM,
            name=self.node_title,
        )


def swap_parents(node_1: LanguageNode, node_2: LanguageNode) -> None:
    tmp = node_1.parent
    node_1.parent = node_2.parent
    node_2.parent = tmp
