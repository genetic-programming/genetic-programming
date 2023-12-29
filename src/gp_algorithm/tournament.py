import random
from typing import Generator

from gp_algorithm.individual import IndividualWithFitness


class Tournament:
    def __init__(
        self,
        population: list[IndividualWithFitness],
        size: int,
    ) -> None:
        self.population = population
        self.shuffle_population()
        if size < 2:
            raise ValueError("Tournament size must be at least 2")
        self.size = size

    def shuffle_population(self) -> None:
        random.shuffle(self.population)

    def select(self) -> list[IndividualWithFitness]:
        winners = []
        for chunk in self.chunks():
            winner = self.select_from_chunk(chunk=chunk)
            winners.append(winner)

        return winners

    def chunks(self) -> Generator[list[IndividualWithFitness], None, None]:
        for i in range(0, len(self.population), self.size):
            yield self.population[i : i + self.size]

    @staticmethod
    def select_from_chunk(chunk: list[IndividualWithFitness]) -> IndividualWithFitness:
        winner = chunk[0]

        for individual in chunk[1:]:
            if individual.fitness > winner.fitness:
                continue
            winner = individual

        return winner


class NegativeTournament(Tournament):
    @staticmethod
    def select_from_chunk(chunk: list[IndividualWithFitness]) -> IndividualWithFitness:
        winner = chunk[0]

        for individual in chunk[1:]:
            if individual.fitness < winner.fitness:
                continue
            winner = individual

        return winner
