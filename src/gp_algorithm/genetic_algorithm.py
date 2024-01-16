import random
from copy import deepcopy

from gp_algorithm.individual import Individual, IndividualWithFitness
from gp_algorithm.interpreter.expression import Expression
from gp_algorithm.interpreter.interpreter import Interpreter
from gp_algorithm.interpreter.visitor import Visitor
from gp_algorithm.tournament import NegativeTournament, Tournament
from gp_algorithm.utils import calculate_fitness, FitnessFunction, random_crossover


class GeneticAlgorithmStep:
    def __init__(
        self,
        fitness_function: FitnessFunction,
        error_threshold: float,
        max_generations: int = 100,
        mutation_rate: float = 0.2,
        crossover_rate: float = 0.5,
        population: dict[int, IndividualWithFitness] | None = None,
        program_inputs: list[list[Expression]] | None = None,
        inputs: list[list[str]] | None = None,
        file_name: str | None = None,
    ) -> None:
        self.fitness_function = fitness_function
        self.error_threshold = error_threshold
        self.max_generations = max_generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.population = population or {}
        self.program_inputs = program_inputs or []
        self.inputs = inputs
        self.file_name = file_name


class GeneticAlgorithm:
    def __init__(
        self,
        steps: list[GeneticAlgorithmStep],
        population_size: int = 1000,
        initial_individual_size: int = 1,
        int_max_value: int = 100,
        interpreter: Interpreter | None = None,
        verbose: bool = False,
    ) -> None:
        self.steps = steps
        self.current_step = steps[0]
        self.population_size = population_size
        self.initial_individual_size = initial_individual_size
        self.interpreter = interpreter or Interpreter(visitor=Visitor(verbose=verbose))
        self.int_max_value = int_max_value
        self.population: dict[int, IndividualWithFitness] = {}
        self.program_inputs: list[list[Expression]] = []
        self.verbose = verbose

    def run(self) -> IndividualWithFitness:
        population = self.generate_population()
        best_individual = IndividualWithFitness(
            individual=population[0],
            fitness=float("inf"),
        )
        success = False

        for i, step in enumerate(self.steps):
            print(f"\nRunning step: {i} - {step.fitness_function.__name__}")
            print("=" * 25)
            self.current_step = step
            self.set_input()
            self.calculate_fitness_for_population(population)
            success, best_individual = self.run_step()
            if not success:
                break

        if success:
            print("\nPROBLEM SOLVED")
        else:
            print("\nPROBLEM NOT SOLVED")

        if self.current_step.file_name:
            self.save_results(
                best_individual=best_individual,
                generation=self.current_step.max_generations,
                file_name=self.current_step.file_name,
            )

        self.print_results(best_individual=best_individual)
        return best_individual

    def generate_population(self) -> dict[int, Individual]:
        population = {}
        for i in range(self.population_size):
            population[i] = Individual(
                size=self.initial_individual_size,
                int_max_value=self.int_max_value,
            )
        return population

    def set_input(self) -> None:
        if self.current_step.inputs:
            program_inputs = self.interpreter.interpret_inputs(input_strings=self.current_step.inputs)
        else:
            program_inputs = []

        self.program_inputs = program_inputs

    def calculate_fitness_for_population(self, population: dict[int, Individual]) -> None:
        for i in range(len(population)):
            individual = population[i]
            fitness = self.calculate_fitness(individual)
            self.population[i] = IndividualWithFitness(
                individual=individual,
                fitness=fitness,
            )

    def run_step(self) -> tuple[bool, IndividualWithFitness]:
        best_individual = self.population[0]

        for generation_number in range(self.current_step.max_generations):
            best_individual, average_fitness = self.get_best_and_avg_fitness()
            print(
                f"Generation: {generation_number}, "
                f"best fitness: {best_individual.fitness}, "
                f"avg fitness: {average_fitness}",
            )
            if self.verbose:
                print("=" * 25)
                print(f"Best individual: {best_individual.individual.build_str()}")

            if best_individual.fitness <= self.current_step.error_threshold:
                return True, best_individual

            self.evolve()

        return False, best_individual

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

            if random.random() < self.current_step.crossover_rate:
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
        mutant_count = int(self.population_size * self.current_step.mutation_rate)
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
            fitness_function=self.current_step.fitness_function,
            program_inputs=self.program_inputs,
        )

    @staticmethod
    def print_results(best_individual: IndividualWithFitness) -> None:
        print(f"Best fitness: {best_individual.fitness}")
        print(f"Best individual:\n{best_individual.individual}")

    @staticmethod
    def save_results(best_individual: IndividualWithFitness, generation: int, file_name: str) -> None:
        with open(file_name, "w") as f:
            f.write(f"Generation: {generation}\n")
            f.write(f"Best fitness: {best_individual.fitness}\n")
            f.write(f"Best individual:\n{best_individual.individual}")
