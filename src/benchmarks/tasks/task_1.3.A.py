import random

from gp_algorithm.genetic_algorithm import GeneticAlgorithm, GeneticAlgorithmStep

# 1.3.A Program powinien odczytać dwie pierwsze liczy z wejścia
# i zwrócić na wyjściu (jedynie) większą z nich.
# Na wejściu mogą być tylko całkowite liczby dodatnie w zakresie [0,9]


inputs_1 = [
    ["5", "6"],
    ["6", "5"],
    ["5", "4"],
    ["9123", "7213"],
    ["7213", "9123"],
    ["9123", "1233"],
]


def fitness_1(outputs: list[list[str]]) -> float:
    total_error = 0.0
    if compare_arrays(outputs[0], outputs[1]):
        total_error += 1.0
    if compare_arrays(outputs[0], outputs[2]):
        total_error += 1.0
    if compare_arrays(outputs[3], outputs[4]):
        total_error += 1.0
    if compare_arrays(outputs[3], outputs[5]):
        total_error += 1.0
    return total_error


def compare_arrays(list_1: list, list_2: list) -> bool:
    if len(list_1) != len(list_2):
        return False

    for i in range(len(list_1)):
        if list_1[i] != list_2[i]:
            return False

    return True


def generate_data(start: int, end: int, n: int) -> list[list[str]]:
    data = []
    for _ in range(n):
        first = random.randint(start, end)
        second = random.randint(start, end)
        bigger = max(first, second)
        data.append([str(first), str(second), str(bigger)])
    return data


generated_data = generate_data(0, 9, 10)
inputs_2 = [i[:2] for i in generated_data]
expected_outputs = [int(i[2]) for i in generated_data]


def fitness_2(outputs: list[list[str]]) -> float:
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
    initial_individual_size=2,
    verbose=True,
    steps=[
        GeneticAlgorithmStep(
            fitness_function=fitness_1,
            error_threshold=0.1,
            max_generations=10,
            inputs=inputs_1,
        ),
        GeneticAlgorithmStep(
            fitness_function=fitness_2,
            error_threshold=0.1,
            max_generations=50,
            inputs=inputs_2,
            file_name="results/1.3.A",
        ),
    ],
).run()
