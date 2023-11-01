from __future__ import annotations
from typing import Any

from anytree import Node


class LanguageNode(Node):
    def __init__(
        self,
        parent: LanguageNode | None = None,
        children: list[LanguageNode] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            name=self.node_name,
            parent=parent,
            children=children,
            **kwargs,
        )
    
    @property
    def node_name(self) -> str:
        return self.__class__.__name__
    
    @property
    def growable(self) -> bool:
        return False
    
    def grow(self) -> None:
        raise NotImplementedError()


class Leaf(LanguageNode):
    def __init__(self, value: str, *args: Any, **kwargs: Any) -> None:
        self.value = value
        super().__init__(*args, **kwargs)
    
    @property
    def node_name(self) -> str:
        return self.value


def swap_parents(node_1: LanguageNode, node_2: LanguageNode) -> None:
    tmp = node_1.parent
    node_1.parent = node_2.parent
    node_2.parent = tmp
