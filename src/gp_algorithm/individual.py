import random

from anytree import PreOrderIter

from gp_algorithm.grammar import NodeType
from gp_algorithm.nodes import LanguageNode, random_value


class Individual(LanguageNode):
    def __init__(
            self,
            size: int = 0,
            parent: LanguageNode | None = None,
            children: list[LanguageNode] | None = None,
    ) -> None:
        super().__init__(
            node_type=NodeType.PROGRAM,
            parent=parent,
            children=children,
            free_variables=[f"v{i}" for i in range(100)],
            declared_variables=[]
        )
        for _ in range(size):
            self.grow()

    def mutate(self) -> None:
        mutate_candidates = PreOrderIter(self, filter_=lambda node: node.value is not None)
        node_to_mutate: LanguageNode = random.choice(list(mutate_candidates))
        node_to_mutate.value = random_value(node_to_mutate.node_type, self.free_variables, self.declared_variables)
