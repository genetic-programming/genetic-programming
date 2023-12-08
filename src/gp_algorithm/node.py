from __future__ import annotations

import random
from string import ascii_letters
from typing import Any

from anytree import Node, PreOrderIter

from gp_algorithm.tree_config import NodeType, TREE_CONFIG


class LanguageNode(Node):
    def __init__(
        self,
        node_type: NodeType,
        value: str | None = None,
        variables_count: int = 0,
        parent: LanguageNode | None = None,
        children: list[LanguageNode] | None = None,
        **kwargs: Any,
    ) -> None:
        self.node_type = node_type
        self.node_data = TREE_CONFIG[node_type]
        self.value = value
        self.variables_count = variables_count
        super().__init__(
            name=self.get_name(),
            parent=parent,
            children=children,
            **kwargs,
        )

    def __repr__(self) -> str:
        return self.get_name()

    def get_name(self) -> str:
        return self.value if self.value is not None else self.node_type

    def grow(self) -> None:
        growable_descendants = PreOrderIter(self, filter_=lambda node: node.node_data.growable)
        chosen_growable_node: LanguageNode = random.choice(list(growable_descendants))
        chosen_growable_node.random_init()

    def random_init(self) -> None:
        successors = self.node_data.successors
        if not successors:
            self.set_random_value()
            return

        chosen_successor = random.choices(successors, weights=[s.weight for s in successors])[0]
        self.value = chosen_successor.template
        for child_type in chosen_successor.children:
            new_node = LanguageNode(
                node_type=child_type,
                variables=self.variables_count,
                parent=self,
            )
            new_node.parent = self
            if not new_node.node_data.growable:
                new_node.random_init()

    def set_random_value(self) -> None:
        match self.node_type:
            case NodeType.UNARY_OPERATOR:
                self.value = random.choice(["-", "not"])

            case NodeType.BINARY_OPERATOR:
                self.value = random.choice(["+", "-", "*", "/", "and", "or", "==", "!=", ">"])

            case NodeType.VARIABLE_NAME:
                var_number = random.randint(0, self.variables_count)
                self.value = f"v{var_number}"
                if var_number == self.variables_count:
                    statements = filter(
                        lambda node: node.node_type == NodeType.STATEMENTS,
                        self.ancestors,
                    )
                    current_statement = next(statements)
                    current_statement.variables_count += 1

            case NodeType.LITERAL_BOOL:
                self.value = random.choice(["true", "false"])

            case NodeType.LITERAL_INT:
                self.value = str(random.randint(-100, 100))

            case NodeType.LITERAL_STR:
                self.value = '"' + "".join([random.choice(ascii_letters) for _ in range(random.randint(0, 15))]) + '"'

            case _:
                raise ValueError(f"Cannot set random value to node of type: {self.node_type}")

    def build_str(self) -> str:
        if not self.value:
            return ""

        if not self.node_data.successors:
            return self.value

        if not self.node_data.growable:
            return self.value.format(*[child.build_str() for child in self.children])

        children_number = len(self.children)
        if children_number == 0:
            return ""

        result = " ".join(["{}" for _ in range(children_number)])
        return result.format(*[child.build_str() for child in self.children])

    def pretty_str(self, depth: int = 0) -> str:
        if not self.value:
            return ""

        if not self.node_data.successors:
            return self.value

        if not self.node_data.growable:
            return self.value.format(*[child.pretty_str(depth) for child in self.children])

        children_number = len(self.children)
        if children_number == 0:
            return ""

        indent = "  " * depth
        result = f"\n{indent}".join(["{}" for _ in range(children_number)])
        depth += 1
        result = result.format(*[child.pretty_str(depth) for child in self.children])
        if self.node_type == NodeType.STATEMENTS:
            result = "\n" + indent + result
            indent = "  " * (depth - 2)
            result = result + "\n" + indent
        return result
