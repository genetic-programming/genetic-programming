import random
from typing import Generator

from gp_algorithm.individual import IndividualWithFitness


class Tournament:
    def __init__(
        self,
        population: dict[int, IndividualWithFitness],
        size: int,
    ) -> None:
        self.population = list(population.items())
        self.shuffle_population()
        if size < 2:
            raise ValueError("Tournament size must be at least 2")
        self.size = size

    def shuffle_population(self) -> None:
        random.shuffle(self.population)

    def select(self) -> list[tuple[int, IndividualWithFitness]]:
        winners = []
        for chunk in self.chunks():
            winner = self.select_from_chunk(chunk=chunk)
            winners.append(winner)

        return winners

    def chunks(self) -> Generator[list[tuple[int, IndividualWithFitness]], None, None]:
        for i in range(0, len(self.population), self.size):
            yield self.population[i : i + self.size]

    @staticmethod
    def select_from_chunk(chunk: list[tuple[int, IndividualWithFitness]]) -> tuple[int, IndividualWithFitness]:
        winner_id, winner = chunk[0]

        for individual_id, individual in chunk[1:]:
            if individual.fitness > winner.fitness:
                continue
            winner = individual
            winner_id = individual_id

        return winner_id, winner


class NegativeTournament(Tournament):
    @staticmethod
    def select_from_chunk(chunk: list[tuple[int, IndividualWithFitness]]) -> tuple[int, IndividualWithFitness]:
        winner = chunk[0]

        for individual in chunk[1:]:
            if individual[1].fitness < winner[1].fitness:
                continue
            winner = individual

        return winner
