import random

from gp_algorithm.genetic_algorithm import GeneticAlgorithm, GeneticAlgorithmStep

# 1.3.B Program powinien odczytać dwie pierwsze liczy z wejścia
# i zwrócić na wyjściu (jedynie) większą z nich.
# Na wejściu mogą być tylko całkowite liczby w zakresie [-9999,9999]


def generate_inputs(start: int, end: int, n: int) -> list[list[str]]:
    inputs = []
    for _ in range(n):
        inputs.append([str(random.randint(start, end)), str(random.randint(start, end))])
    return inputs


inputs = generate_inputs(-9999, 9999, 20)


def fitness(outputs: list[list[str]]) -> float:
    total_error = 0.0
    for input_data, output_data in zip(inputs, outputs):
        if len(output_data) != 1:
            return float("inf")

        try:
            result = int(output_data[0])
        except ValueError:
            return float("inf")

        bigger = max(int(input_data[0]), int(input_data[1]))

        error = abs(result - bigger)
        total_error += error

    return total_error


best = GeneticAlgorithm(
    initial_individual_size=5,
    verbose=True,
    steps=[
        GeneticAlgorithmStep(
            fitness_function=fitness,
            error_threshold=0.1,
            max_generations=100,
            inputs=inputs,
            file_name="results/1.3.B",
        ),
    ],
).run()
