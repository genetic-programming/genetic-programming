from gp_algorithm.genetic_algorithm import GeneticAlgorithm, GeneticAlgorithmStep

# 1.1.D Program powinien wygenerować na pierwszej pozycji na wyjściu liczbę 1.
# Poza liczbą 1 może też zwrócić inne liczby.


def fitness(outputs: list[list[str]]) -> float:
    output = outputs[0]
    if not output:
        return 2.0

    if "1" == output[0]:
        return 0.0
    else:
        return 1.0


GeneticAlgorithm(
    steps=[
        GeneticAlgorithmStep(fitness_function=fitness, error_threshold=0.1, file_name="results/1.1.D"),
    ],
).run()
