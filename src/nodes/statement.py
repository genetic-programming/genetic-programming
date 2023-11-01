import random
import string

from nodes.base import LanguageNode, Leaf


class Statement(LanguageNode):
    def grow(self) -> None:
        declaration = Declaration(parent=self)
        declaration.grow()


class Declaration(LanguageNode):
    def grow(self) -> None:
        Leaf(
            value=random.choice(["int", "float", "bool"]),
            parent=self,
        )
        letters = string.ascii_lowercase
        Leaf(
            value=random.choice(letters),
            parent=self,
        )
        