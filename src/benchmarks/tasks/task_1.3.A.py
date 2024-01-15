import random

from gp_algorithm.genetic_algorithm import GeneticAlgorithm


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


def fitness(outputs: list[list[str]]) -> float:
    total_error = 0.0
    for expected, output in zip(expected_outputs, outputs):
        if len(output) == 0:
            total_error += 100.0
            continue
        
        if len(output) != 1:
            total_error += 1.0

        try:
            result = int(output[0])
        except ValueError:
            total_error += 10.0
            continue

        error = abs(result - expected)
        total_error += error

    return total_error


def fitness(outputs: list[list[str]]) -> float:
    total_error = 0.0
    for expected, output in zip(expected_outputs, outputs):
        if len(output) == 0:
            total_error += 100.0
            continue
        
        if len(output) != 1:
            total_error += 1.0

        try:
            result = int(output[0])
        except ValueError:
            total_error += 10.0
            continue

        error = abs(result - expected)
        total_error += error

    return total_error


best = GeneticAlgorithm(
    fitness_function=fitness,
    error_threshold=0.1,
    initial_individual_size=5,
    max_generations=100,
    verbose=True,
).run(
    inputs=inputs,
    file_name="results/1.3.A",
)
