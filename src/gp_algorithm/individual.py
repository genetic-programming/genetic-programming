import random
from dataclasses import dataclass
from typing import Any

from gp_algorithm.node import LanguageNode
from gp_algorithm.tree_config import NodeType


class Individual(LanguageNode):
    def __init__(
        self,
        size: int = 0,
        parent: LanguageNode | None = None,
        children: list[LanguageNode] | None = None,
        int_max_value: int = 100,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            node_type=NodeType.STATEMENTS,
            parent=parent,
            children=children,
            variables_count=0,
            int_max_value=int_max_value,
            **kwargs,
        )
        for _ in range(size):
            self.grow()

    def __str__(self) -> str:
        return self.pretty_str()

    def mutate(self) -> None:
        mutate_candidates = list(self.descendants)
        if not mutate_candidates:
            return
        node_to_mutate: LanguageNode = random.choice(mutate_candidates)
        node_to_mutate.children = []
        node_to_mutate.random_init()


@dataclass()
class IndividualWithFitness:
    individual: Individual
    fitness: float
