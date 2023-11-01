import random

from anytree import PreOrderIter, RenderTree
from anytree.exporter import UniqueDotExporter

from src.nodes.base import LanguageNode
from src.nodes.statement import Statement


class Individual(LanguageNode):
    def __init__(
        self,
        size: int,
    ) -> None:
        super().__init__()
        self.program_size: int = 0
        for _ in range(size):
            self.grow()
            
    @property
    def growable(self) -> bool:
        return True
            
    def grow(self) -> None:
        random_node = self.get_random_growable_node()
        new_statement = Statement(parent=random_node)
        new_statement.grow()
        self.program_size += 1
    
    def get_random_growable_node(self) -> LanguageNode:
        growable_nodes = list(PreOrderIter(self, filter_=lambda node: node.growable))
        return random.choice(growable_nodes)


program = Individual(size=8)
print(RenderTree(program))
UniqueDotExporter(program).to_picture("program.png")
