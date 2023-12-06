from typing import Callable, Generator

from gp_algorithm.individual import Individual
from gp_algorithm.interpreter.interpreter import Interpreter
from gp_algorithm.utils import calculate_fitness


class Tournament:
    def __init__(
        self,
        fitness_function: Callable[[Individual], float],
        population: list[Individual],
        size: int,
    ) -> None:
        self.fitness_function = fitness_function
        self.population = population
        self.size = size

    def select(self) -> list[Individual]:
        best_individuals = []
        for chunk in self.chunks():
            best_individuals.append(self.select_from_chunk(chunk))

        return best_individuals

    def chunks(self) -> Generator[list[Individual], None, None]:
        for i in range(0, len(self.population), self.size):
            yield self.population[i : i + self.size]

    def select_from_chunk(self, chunk: list[Individual]) -> Individual:
        max_value: float = 0
        best_individual = None

        for individual in chunk:
            try:
                value = calculate_fitness(interpreter=Interpreter(),individual=individual,fitness_function=self.fitness_function, input_strings=["1"]*100)
            except Exception:
                continue
            if value <= max_value:
                continue
            max_value = value
            best_individual = individual

        return best_individual
