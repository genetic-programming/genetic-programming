import random
from gp_algorithm.genetic_algorithm import GeneticAlgorithm, GeneticAlgorithmStep


# Given 3 integer inputs: start, end, and step, print the integers in the sequence
#  n0 = start
# ni = ni-1 + step
#
# for each ni < end, each on their own line.


def generate_inputs(number: int) -> list[list[str]]:
    inputs_list = []
    for _ in range(number):
        inputs_list.append([str(random.randint(0, 100)) for _ in range(3)])
    return inputs_list


inputs = [["5", "20", "3"], ["2", "50", "7"], ["12", "28", "4"], ["4", "12", "3"], ["1", "8", "2"]]


# inputs = generate_inputs(100)

expected_outputs = []

for input_ in inputs:
    start = int(input_[0])
    end = int(input_[1])
    step = int(input_[2])
    output = []
    n = 0
    for i in range(start, end, step):
        n += i
        output.append(str(n))
    expected_outputs.append(output)


def fitness(outputs: list[list[str]]) -> float:
    total_error = 0
    for program_output, expected_output in zip(outputs, expected_outputs):
        len_diff = abs(len(program_output) - len(expected_output))
        if len_diff > 0:
            total_error += len_diff * 1000
        for program_value, expected_value in zip(program_output, expected_output):
            try:
                value = int(program_value)
            except ValueError:
                return float("inf")
            total_error += abs(int(value) - int(expected_value))

    return total_error


gp = GeneticAlgorithm(
    initial_individual_size=10,
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
            file_name="results/for_loop_index",
        ),
    ],
).run()
