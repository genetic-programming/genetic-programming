import random

from gp_algorithm.genetic_algorithm import GeneticAlgorithm, GeneticAlgorithmStep


# 1.4.A Program powinien odczytać dziesięć pierwszych liczy z wejścia
# i zwrócić na wyjściu (jedynie) ich średnią arytmetyczną (zaokrągloną do pełnej liczby całkowitej).
# Na wejściu mogą być tylko całkowite liczby w zakresie [-99,99]


def generate_inputs(start: int, end: int, n: int) -> list[list[str]]:
    inputs = []
    for _ in range(n):
        inputs.append([str(random.randint(start, end)) for _ in range(10)])
    return inputs


inputs = generate_inputs(-99, 99, 30)


def fitness_1(outputs: list[list[str]]) -> float:
    total_error = 0.0
    for input_data, output_data in zip(inputs, outputs):
        if len(output_data) == 0:
            return float("inf")

        try:
            result = int(output_data[0])
        except ValueError:
            return float("inf")

        expected_result = sum(int(i) for i in input_data[:4])
        error = abs(result - expected_result) ** 2
        total_error += error

    return total_error


def fitness_2(outputs: list[list[str]]) -> float:
    total_error = 0.0
    for input_data, output_data in zip(inputs, outputs):
        if len(output_data) == 0:
            return float("inf")

        try:
            result = int(output_data[0])
        except ValueError:
            return float("inf")

        expected_result = sum(int(i) for i in input_data[:6])
        error = abs(result - expected_result)
        total_error += error

    return total_error


best = GeneticAlgorithm(
    initial_individual_size=3,
    verbose=True,
    steps=[
        GeneticAlgorithmStep(
            fitness_function=fitness_1,
            error_threshold=0.1,
            max_generations=100,
            mutation_rate=0.2,
            crossover_rate=0.5,
            inputs=inputs,
        ),
        GeneticAlgorithmStep(
            fitness_function=fitness_2,
            error_threshold=0.1,
            max_generations=100,
            mutation_rate=0.2,
            crossover_rate=0.7,
            inputs=inputs,
            file_name="results/1.4.A",
        ),
    ],
).run()
