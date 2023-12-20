from typing import Callable, Generator

from gp_algorithm.individual import Individual
from gp_algorithm.interpreter.interpreter import Interpreter
from gp_algorithm.utils import calculate_fitness


class Tournament:
    def __init__(
        self,
        fitness_function: Callable[[list[list[str]]], float],
        population: list[Individual],
        size: int,
        interpreter: Interpreter | None = None,
    ) -> None:
        self.interpreter = interpreter or Interpreter()
        self.fitness_function = fitness_function
        self.population = population
        self.size = size

    def select(self, inputs: list[list[str]] | None = None) -> list[tuple[Individual, float]]:
        winners = []
        for chunk in self.chunks():
            winner = self.select_from_chunk(chunk=chunk, inputs=inputs)
            winners.append(winner)

        return winners

    def chunks(self) -> Generator[list[Individual], None, None]:
        for i in range(0, len(self.population), self.size):
            yield self.population[i : i + self.size]

    def select_from_chunk(
        self,
        chunk: list[Individual],
        inputs: list[list[str]] | None = None,
    ) -> tuple[Individual, float]:
        min_value: float = float("inf")
        winner = None

        for individual in chunk:
            value = calculate_fitness(
                interpreter=self.interpreter,
                individual=individual,
                fitness_function=self.fitness_function,
                input_strings=inputs or [],
            )
            if value > min_value:
                continue
            min_value = value
            winner = individual

        return winner, min_value
