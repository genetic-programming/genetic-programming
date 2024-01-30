from gp_algorithm.genetic_algorithm import GeneticAlgorithm, GeneticAlgorithmStep

# 1.1.F Program powinien wygenerować na wyjściu liczbę jako jedyną liczbę 1.
# Poza liczbą 1 NIE powinien nic więcej wygenerować.


def fitness(outputs: list[list[str]]) -> float:
    output = outputs[0]
    if not output or len(output) > 1:
        return 2.0

    if "1" == output[0]:
        return 0
    else:
        return 1


GeneticAlgorithm(
    steps=[
        GeneticAlgorithmStep(fitness_function=fitness, error_threshold=1, file_name="results/1.1.F"),
    ],
).run()
