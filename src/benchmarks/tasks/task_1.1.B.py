from gp_algorithm.genetic_algorithm import GeneticAlgorithm, GeneticAlgorithmStep

# 1.1.B Program powinien wygenerować na wyjściu
# (na dowolnej pozycji w danych wyjściowych) liczbę 789.
# Poza liczbą 789 może też zwrócić inne liczby.


def fitness(outputs: list[list[str]]) -> float:
    output = outputs[0]
    if not output:
        return 1000.0

    if "789" in output:
        return 0.0
    else:
        closest = min(output, key=lambda x: abs(int(x) - 789) if x not in ["true", "false"] else 900)
        if closest in ["true", "false"]:
            return 900.0
        else:
            return abs(float(closest) - 789)


GeneticAlgorithm(
    int_max_value=1000,
    steps=[
        GeneticAlgorithmStep(
            fitness_function=fitness,
            error_threshold=0.1,
            file_name="results/1.1.B",
        ),
    ],
).run()
