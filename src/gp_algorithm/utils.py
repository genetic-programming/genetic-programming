import random
from typing import Callable

from anytree import PreOrderIter

from gp_algorithm.builder import individual_builder
from gp_algorithm.individual import Individual
from gp_algorithm.interpreter.exceptions import LanguageException
from gp_algorithm.interpreter.interpreter import Interpreter
from gp_algorithm.node import LanguageNode
from gp_algorithm.tree_config import TREE_CONFIG


def swap_parents(node_1: LanguageNode, node_2: LanguageNode) -> None:
    parent_1 = node_1.parent
    parent_2 = node_2.parent
    children_1 = parent_1.children
    children_2 = parent_2.children

    children_1 = list(children_1)
    index_1 = children_1.index(node_1)
    children_1[index_1] = node_2
    children_1 = tuple(children_1)

    children_2 = list(children_2)
    index_2 = children_2.index(node_2)
    children_2[index_2] = node_1
    children_2 = tuple(children_2)

    parent_1.children = children_1
    parent_2.children = children_2


def random_crossover(individual_1: Individual, individual_2: Individual) -> None:
    random_node: LanguageNode = random.choice(list(individual_1.descendants)[1:])
    allowed_swaps = TREE_CONFIG[random_node.node_type].allowed_swaps

    swap_candidates_generator = PreOrderIter(individual_2, filter_=lambda node: node.node_type in allowed_swaps)
    swap_candidates = list(swap_candidates_generator)
    if not swap_candidates:
        return

    node_to_swap: LanguageNode = random.choice(swap_candidates)
    swap_parents(random_node, node_to_swap)


def calculate_fitness(
    interpreter: Interpreter,
    individual: Individual,
    fitness_function: Callable[[list[list[str]]], float],
    input_strings: list[list[str]],
) -> float:
    individual_as_str = individual.build_str()
    parsed_individual = interpreter.parse_str(data=individual_as_str)
    program_inputs = interpreter.interpret_inputs(input_strings=input_strings)

    outputs = []
    if not program_inputs:
        try:
            output = interpreter.interpret_tree(
                tree=parsed_individual,
                program_input=[],
            )
        except LanguageException:
            return float("inf")
        outputs.append(output)

    else:
        for program_input in program_inputs:
            try:
                output = interpreter.interpret_tree(
                    tree=parsed_individual,
                    program_input=program_input,
                )
            except LanguageException:
                return float("inf")
            outputs.append(output)

    return fitness_function(outputs)


def build_individual_from_file(file_path: str) -> Individual:
    with open(file_path, "r") as file:
        data = file.read()

    return individual_builder.build_from_parser_str(data=data)


def save_individual_to_file(individual: Individual, file_path: str) -> None:
    with open(file_path, "w+") as file:
        file.write(str(individual))
