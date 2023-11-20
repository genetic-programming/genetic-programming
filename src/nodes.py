from __future__ import annotations

import random
from typing import Any

from anytree import Node, PreOrderIter

from grammar import GRAMMAR, NodeType


def random_value(node_type: NodeType) -> str:
    possible_values = GRAMMAR[node_type].possible_values
    return random.choice(possible_values) if possible_values else None  # noqa: S311


def create_node_random(node_type: NodeType) -> LanguageNode:
    return LanguageNode(
        node_type=node_type,
        value=random_value(node_type),
    )


def swap_parents(node_1: LanguageNode, node_2: LanguageNode) -> None:
    parent_1 = node_1.parent
    parent_2 = node_2.parent
    children_1 = parent_1.children
    children_2 = parent_2.children

    children_1 = list(children_1)
    index_1 = children_1.index(node_1)
    children_1[index_1] = node_2
    children_1 = tuple(children_1)

    children_2 = list(children_2)
    index_2 = children_2.index(node_2)
    children_2[index_2] = node_1
    children_2 = tuple(children_2)

    parent_1.children = children_1
    parent_2.children = children_2


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
        parent_node: LanguageNode = random.choice(list(growable_descendants))  # noqa: S311
        parent_node.random_init()

    def random_init(self) -> None:
        successors = GRAMMAR[self.node_type].successors
        if not successors:
            return

        new_nodes_types = random.choice(successors)  # noqa: S311
        for new_node_type in new_nodes_types:
            new_node = create_node_random(node_type=new_node_type)
            if not GRAMMAR[new_node.node_type].growable:
                new_node.random_init()
            new_node.parent = self
