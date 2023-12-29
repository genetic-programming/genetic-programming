import random
from typing import Callable

from gp_algorithm.individual import Individual, IndividualWithFitness
from gp_algorithm.interpreter.expression import Expression
from gp_algorithm.interpreter.interpreter import Interpreter
from gp_algorithm.tournament import NegativeTournament, Tournament
from gp_algorithm.utils import calculate_fitness, random_crossover


class GeneticAlgorithm:
    def __init__(
        self,
        fitness_function: Callable[[list[list[str]]], float],
        error_threshold: float,
        population_size: int = 1000,
        max_generations: int = 100,
        initial_individual_size: int = 1,
        interpreter: Interpreter | None = None,
    ) -> None:
        self.fitness_function = fitness_function
        self.error_threshold = error_threshold
        self.population_size = population_size
        self.max_generations = max_generations
        self.initial_individual_size = initial_individual_size
        self.interpreter = interpreter or Interpreter()
        self.population: list[IndividualWithFitness] = []

    def run(self, inputs: list[list[str]] | None = None) -> IndividualWithFitness:
        if inputs:
            program_inputs = self.interpreter.interpret_inputs(input_strings=inputs)
        else:
            program_inputs = []

        self.generate_population(program_inputs=program_inputs)
        best_individual = self.population[0]

        for generation_number in range(self.max_generations):
            best_individual = self.find_best_individual()
            print(f"Generation: {generation_number}, best fitness: {best_individual.fitness}")
            print(f"Best individual: {best_individual.individual.build_str()}\n")

            if best_individual.fitness < self.error_threshold:
                print("PROBLEM SOLVED")
                self.print_results(best_individual)
                return best_individual

            self.evolve(program_inputs=program_inputs)

        print("PROBLEM NOT SOLVED")
        self.print_results(best_individual)
        return best_individual

    def generate_population(
        self,
        program_inputs: list[list[Expression]],
    ) -> None:
        population = []
        for _ in range(self.population_size):
            individual = Individual(
                size=self.initial_individual_size,
            )
            fitness = self.calculate_fitness(
                individual=individual,
                program_inputs=program_inputs,
            )
            population.append(
                IndividualWithFitness(
                    individual=individual,
                    fitness=fitness,
                ),
            )
        self.population = population

    def find_best_individual(self) -> IndividualWithFitness:
        best_individual = self.population[0]
        for individual in self.population[1:]:
            if individual.fitness < best_individual.fitness:
                best_individual = individual
        return best_individual

    def evolve(self, program_inputs: list[list[Expression]]) -> None:
        best_individuals = Tournament(
            population=self.population,
            size=20,
        ).select()

        worst_individuals = NegativeTournament(
            population=self.population,
            size=5,
        ).select()

        for worst_individual_1, worst_individual_2 in zip(worst_individuals[::2], worst_individuals[1::2]):
            worst_1_index = self.population.index(worst_individual_1)
            worst_2_index = self.population.index(worst_individual_2)
            parents: list[IndividualWithFitness] = random.sample(best_individuals, 2)
            child_1, child_2 = random_crossover(
                parents[0].individual,
                parents[1].individual,
            )
            for child, index in [(child_1, worst_1_index), (child_2, worst_2_index)]:
                child.grow()
                child.mutate()
                child_fitness = self.calculate_fitness(
                    individual=child,
                    program_inputs=program_inputs,
                )
                self.population[index] = IndividualWithFitness(
                    individual=child,
                    fitness=child_fitness,
                )

    def calculate_fitness(
        self,
        individual: Individual,
        program_inputs: list[list[Expression]],
    ) -> float:
        return calculate_fitness(
            interpreter=self.interpreter,
            individual=individual,
            fitness_function=self.fitness_function,
            program_inputs=program_inputs,
        )

    @staticmethod
    def print_results(best_individual: IndividualWithFitness) -> None:
        print("=" * 25)
        print(f"Best fitness: {best_individual.fitness}")
        print(f"Best individual:\n{best_individual.individual}")
