from gp_algorithm.genetic_algorithm import GeneticAlgorithm, GeneticAlgorithmStep

# 1.2.E Program powinien odczytać dwie pierwsze liczy z wejścia
# i zwrócić na wyjściu (jedynie) ich iloczyn.
# Na wejściu mogą być tylko całkowite liczby dodatnie w zakresie [-9999,9999]


inputs = [
    ["-5421", "2783"],
    ["2196", "-3847"],
    ["9438", "2156"],
    ["1243", "-7894"],
    ["3567", "6234"],
    ["-6789", "-4321"],
]


def fitness(outputs: list[list[str]]) -> float:
    total_error = 0.0
    for input_data, output_data in zip(inputs, outputs):
        if len(output_data) != 1:
            return float("inf")

        try:
            result = int(output_data[0])
        except ValueError:
            total_error += float("inf")
            continue

        expected_result = int(input_data[0]) * int(input_data[1])
        error = abs(result - expected_result)
        total_error += error

    return total_error


genetic_algorithm = GeneticAlgorithm(
    steps=[
        GeneticAlgorithmStep(
            fitness_function=fitness,
            error_threshold=0.1,
            inputs=inputs,
            file_name="results/1.2.E",
        ),
    ],
    initial_individual_size=1,
)
best = genetic_algorithm.run()
