import random
from copy import deepcopy
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
        int_max_value: int = 100,
        mutation_rate: float = 0.2,
        crossover_rate: float = 0.5,
        interpreter: Interpreter | None = None,
    ) -> None:
        self.fitness_function = fitness_function
        self.error_threshold = error_threshold
        self.population_size = population_size
        self.max_generations = max_generations
        self.initial_individual_size = initial_individual_size
        self.interpreter = interpreter or Interpreter()
        self.int_max_value = int_max_value
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.population: dict[int, IndividualWithFitness] = {}
        self.program_inputs: list[list[Expression]] = []

    def run(
        self,
        inputs: list[list[str]] | None = None,
        verbose: bool = False,
        file_name: str = None,
    ) -> IndividualWithFitness:
        if inputs:
            program_inputs = self.interpreter.interpret_inputs(input_strings=inputs)
        else:
            program_inputs = []

        self.program_inputs = program_inputs
        self.generate_population()
        best_individual = self.population[0]

        for generation_number in range(self.max_generations):
            best_individual, average_fitness = self.get_best_and_avg_fitness()
            print(
                f"Generation: {generation_number}, "
                f"best fitness: {best_individual.fitness}, "
                f"avg fitness: {average_fitness}",
            )
            if verbose:
                print("=" * 25)
                print(f"Best individual: {best_individual.individual.build_str()}\n")
                print("=" * 25)

            if best_individual.fitness <= self.error_threshold:
                print("PROBLEM SOLVED")
                self.print_results(best_individual)
                self.save_results(best_individual, generation_number, file_name)
                return best_individual

            self.evolve()

        print("PROBLEM NOT SOLVED")
        self.print_results(best_individual)
        self.save_results(best_individual, self.max_generations, file_name)
        return best_individual

    def generate_population(self) -> None:
        population = {}
        for i in range(self.population_size):
            individual = Individual(
                size=self.initial_individual_size,
                int_max_value=self.int_max_value,
            )
            fitness = self.calculate_fitness(individual)
            population[i] = IndividualWithFitness(
                individual=individual,
                fitness=fitness,
            )
        self.population = population

    def get_best_and_avg_fitness(self) -> tuple[IndividualWithFitness, float]:
        best_individual = self.population[0]
        fitness_sum = 0
        for _, individual in self.population.items():
            fitness_sum += individual.fitness
            if individual.fitness < best_individual.fitness:
                best_individual = individual
        average_fitness = fitness_sum / self.population_size
        return best_individual, average_fitness

    def evolve(self) -> None:
        best_individuals = Tournament(
            population=self.population,
            size=20,
        ).select()

        worst_individuals = NegativeTournament(
            population=self.population,
            size=5,
        ).select()

        for worst_individual_1, worst_individual_2 in zip(worst_individuals[::2], worst_individuals[1::2]):
            worst_1_index, worst_individual_1 = worst_individual_1
            worst_2_index, worst_individual_2 = worst_individual_2
            parents: list[tuple[int, IndividualWithFitness]] = random.sample(best_individuals, 2)
            parent_1_index, parent_1 = parents[0]
            parent_2_index, parent_2 = parents[1]

            if random.random() < self.crossover_rate:
                child_1 = deepcopy(parent_1.individual)
                child_2 = deepcopy(parent_2.individual)
                for child, index in [(child_1, worst_1_index), (child_2, worst_2_index)]:
                    self.replace_individual(
                        new_individual=child,
                        id_to_replace=index,
                    )
                continue

            child_1, child_2 = random_crossover(
                parent_1.individual,
                parent_2.individual,
            )
            for child, index in [(child_1, worst_1_index), (child_2, worst_2_index)]:
                self.replace_individual(
                    new_individual=child,
                    id_to_replace=index,
                )

        self.mutate(best_ids=[index for index, _ in best_individuals])

    def mutate(self, best_ids: list[int]) -> None:
        mutant_count = int(self.population_size * self.mutation_rate)
        potential_mutant_ids = set(self.population.keys()) - set(best_ids)
        mutant_ids = random.choices(list(potential_mutant_ids), k=mutant_count)
        for mutant_id in mutant_ids:
            mutant = self.population[mutant_id]
            mutant.individual.mutate()
            self.replace_individual(
                new_individual=mutant.individual,
                id_to_replace=mutant_id,
            )

    def replace_individual(
        self,
        new_individual: Individual,
        id_to_replace: int,
    ) -> None:
        individual_fitness = self.calculate_fitness(new_individual)
        self.population[id_to_replace] = IndividualWithFitness(
            individual=new_individual,
            fitness=individual_fitness,
        )

    def calculate_fitness(self, individual: Individual) -> float:
        return calculate_fitness(
            interpreter=self.interpreter,
            individual=individual,
            fitness_function=self.fitness_function,
            program_inputs=self.program_inputs,
        )

    @staticmethod
    def print_results(best_individual: IndividualWithFitness) -> None:
        print("=" * 25)
        print(f"Best fitness: {best_individual.fitness}")
        print(f"Best individual:\n{best_individual.individual}")

    @staticmethod
    def save_results(best_individual: IndividualWithFitness, generation: int, file_name: str = None) -> None:
        if file_name:
            with open(file_name, "w") as f:
                f.write(f"Generation: {generation}\n")
                f.write(f"Best fitness: {best_individual.fitness}\n")
                f.write(f"Best individual:\n{best_individual.individual}")
