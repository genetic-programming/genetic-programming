from gp_algorithm.genetic_algorithm import GeneticAlgorithm, GeneticAlgorithmStep


def generate_bool_table(k: int) -> list[list[str]]:
    """Generates all possible boolean tables for k variables."""

    if k == 0:
        return [[]]

    table = generate_bool_table(k - 1)
    return [row + ["true"] for row in table] + [row + ["false"] for row in table]


inputs = generate_bool_table(3)

bool_function = "{0} or {1} and not {2}"
expected_outputs = []

for row in inputs:
    capitalized_row = [b.capitalize() for b in row]
    result = eval(bool_function.format(*capitalized_row))  # noqa: S307
    expected_outputs.append([str(result).lower()])


def fitness(outputs: list[list[str]]) -> float:
    total_error = 0.0
    for output, expected_output in zip(outputs, expected_outputs):
        if output == expected_output:
            continue
        if len(output) != len(expected_output):
            total_error += 10.0
        total_error += 1.0

    return total_error


gp = GeneticAlgorithm(
    initial_individual_size=1,
    population_size=1000,
    int_max_value=100,
    verbose=True,
    steps=[
        GeneticAlgorithmStep(
            fitness_function=fitness,
            error_threshold=0.1,
            max_generations=200,
            mutation_rate=0.2,
            crossover_rate=0.5,
            inputs=inputs,
            file_name="results/boolean_regression",
        ),
    ],
).run()
