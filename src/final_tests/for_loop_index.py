from gp_algorithm.genetic_algorithm import GeneticAlgorithm
import random


def generate_inputs(number: int) -> list[list[str]]:
    inputs_list = []
    for _ in range(number):
        inputs_list.append([str(random.randint(0, 100)) for _ in range(3)])
    return inputs_list


inputs = [["5", "20", "3"],
          ["2", "50", "7"],
          ["12", "28", "4"],
          ["4", "12", "3"],
          ["1", "8", "2"]]


# inputs = generate_inputs(100)

expected_outputs = []

for input in inputs:
    start = int(input[0])
    end = int(input[1])
    step = int(input[2])
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
    fitness_function=fitness,
    error_threshold=.1,
    max_generations=1000,
    initial_individual_size=10,
).run(
    file_name="test_results/for_loop_index",
    verbose=True,
)
