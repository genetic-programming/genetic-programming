from gp_algorithm.genetic_algorithm import GeneticAlgorithm

# 1.2.B Program powinien odczytać dwie pierwsze liczy z wejścia
# i zwrócić na wyjściu (jedynie) ich sumę.
# Na wejściu mogą być tylko całkowite liczby w zakresie [-9,9]


inputs = [["-5", "2"], ["2", "-4"], ["9", "2"], ["1", "-7"], ["0", "6"], ["-6", "-4"]]


def fitness(outputs: list[list[str]]) -> float:
    total_error = 0.0
    for input_data, output_data in zip(inputs, outputs):
        if len(output_data) != 1:
            return 900.0

        try:
            result = int(output_data[0])
        except ValueError:
            total_error += 800.0
            continue

        expected_result = int(input_data[0]) + int(input_data[1])
        error = abs(result - expected_result)
        total_error += error

    return total_error


best = GeneticAlgorithm(
    fitness_function=fitness,
    error_threshold=0.1,
    initial_individual_size=1,
).run(
    inputs=inputs,
    file_name="results/1.2.B",
)
