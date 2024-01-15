from gp_algorithm.genetic_algorithm import GeneticAlgorithm

# 1.1.B Program powinien wygenerować na wyjściu
# (na dowolnej pozycji w danych wyjściowych) liczbę 789.
# Poza liczbą 789 może też zwrócić inne liczby.


def fitness(outputs: list[list[str]]) -> float:
    output = outputs[0]
    if not output:
        return 2000.0

    if "1789" in output:
        return 0.0
    else:
        closest = min(output, key=lambda x: abs(int(x) - 1789) if x not in ["true", "false"] else 900)
        if closest in ["true", "false"]:
            return 1900.0
        else:
            return abs(float(closest) - 1789)


GeneticAlgorithm(
    fitness_function=fitness,
    error_threshold=0.1,
    int_max_value=1000,
).run(file_name="results/1.1.B")
