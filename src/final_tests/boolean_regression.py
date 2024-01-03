from gp_algorithm.genetic_algorithm import GeneticAlgorithm


def generate_bool_table(k: int) -> list[list[str]]:
    """Generates all possible boolean tables for k variables."""

    if k == 0:
        return [[]]

    table = generate_bool_table(k - 1)
    return [row + ["true"] for row in table] + [row + ["false"] for row in table]


inputs = generate_bool_table(5)

bool_function = "{0} or {1} and {2} or not {3} and {4}"
expected_outputs = []

for row in inputs:
    capitalized_row = [b.capitalize() for b in row]
    result = eval(bool_function.format(*capitalized_row))
    expected_outputs.append([str(result).lower()])


def fitness(outputs: list[list[str]]) -> float:
    total_error = 0.
    for output, expected_output in zip(outputs, expected_outputs):
        if output == expected_output:
            continue
        if len(output) != len(expected_output):
            total_error += 10.
        total_error += 1.

    return total_error


genetic_algorithm = GeneticAlgorithm(
    fitness_function=fitness,
    error_threshold=.1,
    initial_individual_size=1,
)
best = genetic_algorithm.run(
    inputs=inputs,
    file_name="test_results/boolean_regression",
)