import random
from typing import Callable

from anytree import PreOrderIter

from gp_algorithm.builder import individual_builder
from gp_algorithm.grammar import GRAMMAR
from gp_algorithm.individual import Individual
from gp_algorithm.interpreter.interpreter import Interpreter
from gp_algorithm.nodes import LanguageNode, swap_parents


def random_crossover(
        individual_1: Individual,
        individual_2: Individual,
) -> None:
    random_node: LanguageNode = random.choice(list(individual_1.descendants))
    allowed_swaps = GRAMMAR[random_node.node_type].allowed_swaps
    allowed_swaps.add(random_node.node_type)

    swap_candidates = PreOrderIter(individual_2, filter_=lambda node: node.node_type in allowed_swaps)
    if not swap_candidates:
        return

    node_to_swap: LanguageNode = random.choice(list(swap_candidates))
    swap_parents(random_node, node_to_swap)


def calculate_fitness(
        interpreter: Interpreter,
        individual: Individual,
        fitness_function: Callable[[list[list[str]]], float],
        input_strings: list[list[str]],
) -> float:
    individual_as_str = individual.cast_to_str()
    parsed_individual = interpreter.parse_str(data=individual_as_str)
    program_inputs = interpreter.interpret_inputs(input_strings=input_strings)

    outputs = []
    for program_input in program_inputs:
        output = interpreter.interpret_tree(
            tree=parsed_individual,
            program_input=program_input,
        )
        outputs.append(output)

    return fitness_function(outputs)


def build_individual_from_file(file_path: str) -> Individual:
    with open(file_path, "r") as file:
        data = file.read()

    return individual_builder.build_from_parser_str(data=data)


def save_individual_to_file(individual: Individual, file_path: str) -> None:
    with open(file_path, "w") as file:
        file.write(individual.cast_to_str())
