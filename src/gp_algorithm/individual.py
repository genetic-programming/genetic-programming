import random
from typing import Any

from anytree import PreOrderIter

from gp_algorithm.node import LanguageNode
from gp_algorithm.tree_config import NodeType


class Individual(LanguageNode):
    def __init__(
        self,
        size: int = 0,
        parent: LanguageNode | None = None,
        children: list[LanguageNode] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            node_type=NodeType.STATEMENTS,
            parent=parent,
            children=children,
            variables_count=0,
            **kwargs,
        )
        for _ in range(size):
            self.grow()

    def __str__(self) -> str:
        return self.pretty_str()

    def mutate(self) -> None:
        mutate_candidates = list(PreOrderIter(self, filter_=lambda node: not node.node_data.successors))
        if not mutate_candidates:
            return
        node_to_mutate: LanguageNode = random.choice(mutate_candidates)
        node_to_mutate.set_random_value()
