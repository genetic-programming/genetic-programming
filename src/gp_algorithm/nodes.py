from __future__ import annotations

import random
from typing import Any

from anytree import Node, PreOrderIter

from gp_algorithm.grammar import GRAMMAR, NodeType

from string import ascii_letters


def random_value(node_type: NodeType) -> str | None:
    possible_types = GRAMMAR[node_type].possible_types
    if possible_types:
        match random.choice(possible_types):
            case "variable name":
                return random.choice([f"v{i}" for i in range(100)])
            case "integer":
                return str(random.randint(-1000, 1000))
            case "boolean":
                return random.choice(["true", "false"])
            case "string":
                return "\"" + "".join([random.choice(ascii_letters) for _ in range(15)]) + "\""
    else:
        return None


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
        self.node_data = GRAMMAR[node_type]
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
        growable_descendants = PreOrderIter(self, filter_=lambda node: node.node_data.growable)
        parent_node: LanguageNode = random.choice(list(growable_descendants))  # noqa: S311
        parent_node.random_init()

    def random_init(self) -> None:
        successors = self.node_data.successors
        if not successors:
            return

        new_nodes_types = random.choice(successors)  # noqa: S311
        for new_node_type in new_nodes_types:
            new_node = create_node_random(node_type=new_node_type)
            new_node.parent = self
            if not new_node.node_data.growable:
                new_node.random_init()

    def cast_to_str(self, depth: int = 0) -> str:
        if self.value:
            return self.value

        if self.node_data.growable:
            indent = "  " * depth
            result = f"\n{indent}".join(["{}" for _ in range(len(self.children))])
            depth += 1
            result = result.format(*[child.cast_to_str(depth) for child in self.children])
            if self.node_type == NodeType.COMPOUND_STATEMENT:
                result = "{\n" + indent + result
                indent = "  " * (depth - 2)
                result = result + "\n" + indent + "}"
        else:
            result = self.node_data.representation
            result = result.format(*[child.cast_to_str(depth) for child in self.children])
        return result
