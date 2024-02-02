import random
from gp_algorithm.genetic_algorithm import GeneticAlgorithm, GeneticAlgorithmStep


# Given integer n, return the sum of squaring each integer in the range [1, n].


def generate_inputs(number: int) -> list[list[str]]:
    inputs_list = []
    for _ in range(number):
        inputs_list.append([str(random.randint(0, 30))])
    return inputs_list


inputs = generate_inputs(100)
# inputs = [["5"], ["2"], ["12"], ["4"], ["1"]]


expected_outputs = []
for program_input in inputs:
    value = 0
    for i in range(int(program_input[0])):
        value += i**2
    expected_outputs.append([value])


def fitness(outputs: list[list[str]]) -> float:
    total_error = 0
    for program_output, expected_output in zip(outputs, expected_outputs):
        if len(program_output) != 1:
            return float("inf")
        try:
            value = int(program_output[0])
        except ValueError:
            return float("inf")

        total_error += abs(int(value) - int(expected_output[0]))

    return total_error


gp = GeneticAlgorithm(
    initial_individual_size=2,
    population_size=1000,
    int_max_value=100,
    verbose=True,
    steps=[
        GeneticAlgorithmStep(
            fitness_function=fitness,
            error_threshold=0.1,
            max_generations=150,
            mutation_rate=0.2,
            crossover_rate=0.5,
            inputs=inputs,
            file_name="results/sum_of_squares",
        ),
    ],
).run()
