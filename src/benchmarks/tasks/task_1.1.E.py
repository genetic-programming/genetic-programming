from gp_algorithm.genetic_algorithm import GeneticAlgorithm, GeneticAlgorithmStep

# 1.1.E Program powinien wygenerować na pierwszej pozycji na wyjściu liczbę 789.
# Poza liczbą 789 może też zwrócić inne liczby.


def fitness(outputs: list[list[str]]) -> float:
    output = outputs[0]
    if not output:
        return 1000.0

    first_output = output[0]

    if "789" == first_output:
        return 0.0
    elif first_output in ["true", "false"]:
        return 900.0
    else:
        return abs(int(first_output) - 789)


GeneticAlgorithm(
    steps=[
        GeneticAlgorithmStep(
            fitness_function=fitness,
            error_threshold=0.1,
            file_name="results/1.1.E",
        ),
    ],
    int_max_value=1000,
).run()
