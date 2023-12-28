import math
from typing import Callable

from gp_algorithm.interpreter.interpreter import Interpreter
from gp_algorithm.tournament import Tournament
from gp_algorithm.utils import calculate_fitness
from gp_algorithm.individual import Individual
from gp_algorithm.utils import random_crossover
import random


class GeneticAlgorithm:
    def __init__(
            self,
            fitness_function: Callable[[list[list[str]]], float],
            error_threshold: float,
            population_size: int,
            max_generations: int,
            crossover_probability: float = 0.8,
            individual_size: int = 10,
    ) -> None:
        self.population_size = population_size
        self.error_threshold = error_threshold
        self.max_generations = max_generations
        self.interpreter = Interpreter()
        self.fitness_function = fitness_function
        self.crossover_probability = crossover_probability
        self.individual_size = individual_size

    def run(self, inputs: list[list[str]]) -> Individual:
        population = self.generate_population(self.individual_size)
        best_fitness = float("inf")
        best_individual = None
        tournament = Tournament(
            fitness_function=self.fitness_function,
            population=population,
            size=int(self.population_size / 2),
            interpreter=self.interpreter,
        )

        for generation in range(self.max_generations):
            best_fitness, best_individual = self.calculate_best_fitness(
                population=population,
                inputs=inputs,
            )

            print(f"Generation: {generation}, best fitness: {best_fitness}")

            if best_fitness < self.error_threshold:
                print("PROBLEM SOLVED")
                self.print_results(best_fitness, best_individual)
                return best_individual

            # for i in range(self.population_size):
            for i in range(10):
                print(f"{i}/10")
                best_individuals = tournament.select(inputs=inputs)
                if random.random() < self.crossover_probability:
                    parent1, _ = best_individuals[0]
                    parent2, _ = best_individuals[1]
                    random_crossover(parent1, parent2)
                else:
                    parent, _ = best_individuals[0]
                    parent.mutate()

        print("PROBLEM NOT SOLVED")
        self.print_results(best_fitness, best_individual)
        return best_individual

    def generate_population(self, individual_size: int) -> list[Individual]:
        return [Individual(individual_size) for _ in range(self.population_size)]

    def calculate_best_fitness(self, population: list[Individual], inputs: list[list[str]]) -> (float, Individual):
        best_fitness = float("inf")
        best_individual = None
        for individual in population:
            fitness = calculate_fitness(
                interpreter=self.interpreter,
                individual=individual,
                fitness_function=self.fitness_function,
                input_strings=inputs,
            )
            if fitness < best_fitness:
                best_fitness = fitness
                best_individual = individual
        return best_fitness, best_individual

    @staticmethod
    def print_results(best_fitness: float, best_individual: Individual) -> None:
        print("=========================")
        print(f"Best fitness: {best_fitness}")
        print(f"Best individual:\n{best_individual}")
