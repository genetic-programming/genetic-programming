from gp_algorithm.genetic_algorithm import GeneticAlgorithm, GeneticAlgorithmStep


# 1.1.A Program powinien wygenerować na wyjściu
# (na dowolnej pozycji w danych wyjściowych) liczbę 1.
# Poza liczbą 1 może też zwrócić inne liczby.


def fitness(outputs: list[list[str]]) -> float:
    output = outputs[0]
    if not output:
        return 2.0

    if "1" in output:
        return 0.0
    else:
        return 1.0


gp = GeneticAlgorithm(
    population_size=1000,
    initial_individual_size=1,
    int_max_value=100,
    steps=[
        GeneticAlgorithmStep(
            fitness_function=fitness,
            error_threshold=0.1,
            max_generations=100,
            mutation_rate=0.2,
            crossover_rate=0.5,
            file_name="results/1.1.A"),
    ]).run()
