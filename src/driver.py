from anytree import RenderTree
from anytree.exporter import UniqueDotExporter

from individual import create_individual, random_crossover
from tournament import Tournament

# Tworzenie osobników
indiv_1 = create_individual(size=2)
print(RenderTree(indiv_1))
UniqueDotExporter(indiv_1).to_picture("images/individual_1.png")
indiv_2 = create_individual(size=2)
UniqueDotExporter(indiv_2).to_picture("images/individual_2.png")

# Operacja krzyżowania
random_crossover(indiv_1, indiv_2)
UniqueDotExporter(indiv_1).to_picture("images/swapped_1.png")
UniqueDotExporter(indiv_2).to_picture("images/swapped_2.png")

# Operacja mutacje
indiv_1.mutate()
UniqueDotExporter(indiv_1).to_picture("images/mutated.png")

# Selekcja turniejowa
tournament = Tournament(
    fitness_function=lambda _: 1.0,
    population=[create_individual(size=5) for _ in range(20)],
    size=7,
)
best_individuals = tournament.select()
UniqueDotExporter(best_individuals[0]).to_picture("images/best.png")
