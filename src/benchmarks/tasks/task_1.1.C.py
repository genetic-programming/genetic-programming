from gp_algorithm.genetic_algorithm import GeneticAlgorithm, GeneticAlgorithmStep

# 1.1.C Program powinien wygenerować na wyjściu
# (na dowolnej pozycji w danych wyjściowych) liczbę 31415.
# Poza liczbą 31415 może też zwrócić inne liczby.


def fitness(outputs: list[list[str]]) -> float:
    output = outputs[0]
    if not output:
        return 40000.0

    if "31415" in output:
        return 0.0
    else:
        closest = min(output, key=lambda x: abs(int(x) - 31415) if x not in ["true", "false"] else 35000)
        if closest in ["true", "false"]:
            return 35000.0
        else:
            return abs(int(closest) - 31415)


best = GeneticAlgorithm(
    int_max_value=10000,
    initial_individual_size=2,
    steps=[
        GeneticAlgorithmStep(
            fitness_function=fitness,
            error_threshold=0.1,
            file_name="results/1.1.C",
        ),
    ],
).run()
