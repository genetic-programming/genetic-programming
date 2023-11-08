from anytree import RenderTree
from anytree.exporter import UniqueDotExporter

from nodes import Individual


def create_individual(size: int) -> Individual:
    individual = Individual()
    
    for _ in range(size):
        individual.grow()
    
    return individual


def crossover(
    individual_1: Individual,
    individual_2: Individual,
) -> Individual:
    pass


indiv_1 = create_individual(size=5)
print(RenderTree(indiv_1))
UniqueDotExporter(indiv_1).to_picture("individual_1.png")

indiv_2 = create_individual(size=1)
UniqueDotExporter(indiv_2).to_picture("individual_2.png")
