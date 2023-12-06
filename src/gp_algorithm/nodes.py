from __future__ import annotations

import random
from string import ascii_letters
from typing import Any

from anytree import Node, PreOrderIter

from gp_algorithm.grammar import GRAMMAR, NodeType


def random_value(node_type: NodeType, free_variables: list[str], declared_variables: list[str]) -> str | None:
    possible_types = GRAMMAR[node_type].possible_types
    if not possible_types:
        return None

    match random.choice(possible_types):
        case "variable declaration":
            new_variable = free_variables.pop(0)
            declared_variables.append(new_variable)
            return new_variable
        case "variable name":
            return random.choice(declared_variables)
        case "integer":
            return str(random.randint(-1000, 1000))
        case "boolean":
            return random.choice(["true", "false"])
        case "string":
            return '"' + "".join([random.choice(ascii_letters) for _ in range(random.randint(0, 15))]) + '"'
        case _:
            return None


def create_node_random(node_type: NodeType, parent: LanguageNode) -> LanguageNode:
    return LanguageNode(
        node_type=node_type,
        value=random_value(node_type, parent.free_variables, parent.declared_variables),
        free_variables=parent.free_variables,
        declared_variables=parent.declared_variables,
        parent=parent,
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
        free_variables: list[str] | None = None,
        declared_variables: list[str] | None = None,
        value: str | None = None,
        parent: LanguageNode | None = None,
        children: list[LanguageNode] | None = None,
        **kwargs: Any,
    ) -> None:
        self.node_type = node_type
        self.node_data = GRAMMAR[node_type]
        self.value = value
        self.free_variables = free_variables
        self.declared_variables = declared_variables
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
        parent_node: LanguageNode = random.choice(list(growable_descendants))
        parent_node.random_init()

    def random_init(self) -> None:
        successors = self.node_data.successors
        if not successors:
            return

        new_nodes_types = self.draw_new_nodes_types(successors)

        for new_node_type in new_nodes_types:
            new_node = create_node_random(node_type=new_node_type, parent=self)
            if new_node.node_type == NodeType.ASSIGNMENT:
                new_node.make_assignment()
            elif not new_node.node_data.growable:
                new_node.random_init()

    def cast_to_str(self, depth: int = 0) -> str:
        if self.value:
            return self.value

        if not self.node_data.growable:
            result = self.node_data.representation
            return result.format(*[child.cast_to_str(depth) for child in self.children])

        indent = "  " * depth
        result = f"\n{indent}".join(["{}" for _ in range(len(self.children))])
        depth += 1
        result = result.format(*[child.cast_to_str(depth) for child in self.children])
        if self.node_type == NodeType.COMPOUND_STATEMENT:
            result = "{\n" + indent + result
            indent = "  " * (depth - 2)
            result = result + "\n" + indent + "}"
        return result

    def make_assignment(self) -> None:
        successors = self.node_data.successors
        value_type = self.draw_new_nodes_types(successors)[1]
        new_variable_name = self.free_variables.pop(0)
        LanguageNode(
            node_type=NodeType.DECLARATION,
            value=new_variable_name,
            parent=self,
        )
        value_node = create_node_random(node_type=value_type, parent=self)
        value_node.random_init()
        self.declared_variables.append(new_variable_name)

    def draw_new_nodes_types(self, successors: list[list[NodeType]]) -> list[NodeType]:
        new_nodes_types = random.choice(successors)
        while (NodeType.VAR_NAME in new_nodes_types and not self.declared_variables) or (
            NodeType.ASSIGNMENT in new_nodes_types and not self.free_variables
        ):
            new_nodes_types = random.choice(successors)
        return new_nodes_types
