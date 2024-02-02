import random

from gp_algorithm.genetic_algorithm import GeneticAlgorithm, GeneticAlgorithmStep


# 1.3.A Program powinien odczytać dwie pierwsze liczy z wejścia
# i zwrócić na wyjściu (jedynie) większą z nich.
# Na wejściu mogą być tylko całkowite liczby dodatnie w zakresie [0,9]


def generate_data(start: int, end: int, n: int) -> list[list[str]]:
    data = []
    for _ in range(n):
        first = random.randint(start, end)
        second = random.randint(start, end)
        bigger = max(first, second)
        data.append([str(first), str(second), str(bigger)])
    return data


generated_data = generate_data(0, 9, 10)
inputs = [i[:2] for i in generated_data]
expected_outputs = [int(i[2]) for i in generated_data]


def fitness_1(outputs: list[list[str]]) -> float:
    total_error = 0.0
    for i, output in enumerate(outputs):
        if len(output) != 2:
            total_error += 100.0
            continue
        input = inputs[i]

        if not output[0] in ["true", "false"]:
            total_error += 50.0
            continue
        if output[0] == "false" and int(input[0]) > int(input[1]):
            total_error += 10.0
        if output[0] == "true" and int(input[0]) <= int(input[1]):
            total_error += 10.0

    return total_error


def fitness_2(outputs: list[list[str]]) -> float:
    total_error = 0.0
    for expected, output in zip(expected_outputs, outputs):
        if len(output) != 2:
            return float('inf')

        total_error += fitness_1(outputs)

        try:
            result = int(output[1])
        except ValueError:
            total_error += 20.0
            continue

        if result < expected:
            total_error += 100.0
        if result > expected:
            return float('inf')

    return total_error


best = GeneticAlgorithm(
    initial_individual_size=4,
    verbose=True,
    steps=[
        GeneticAlgorithmStep(
            fitness_function=fitness_1,
            error_threshold=0.1,
            max_generations=10,
            inputs=inputs,
        ),
        GeneticAlgorithmStep(
            fitness_function=fitness_2,
            error_threshold=0.1,
            max_generations=200,
            inputs=inputs,
            crossover_rate=0.7,
            mutation_rate=0.7,
            file_name="results/1.3.A",
        ),
    ],
).run()
