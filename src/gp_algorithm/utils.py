import random
from copy import deepcopy
from typing import Callable, TypeAlias

from anytree import PreOrderIter

from gp_algorithm.builder import individual_builder
from gp_algorithm.individual import Individual
from gp_algorithm.interpreter.exceptions import IncorrectIndividualException, LanguageException
from gp_algorithm.interpreter.expression import Expression
from gp_algorithm.interpreter.interpreter import Interpreter
from gp_algorithm.node import LanguageNode
from gp_algorithm.tree_config import TREE_CONFIG

FitnessFunction: TypeAlias = Callable[[list[list[str]]], float]


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


def mutate(individual: Individual) -> Individual:
    individual_copy = deepcopy(individual)
    individual_copy.mutate()
    return individual_copy


def random_crossover(individual_1: Individual, individual_2: Individual) -> tuple[Individual, Individual]:
    individual_1_copy = deepcopy(individual_1)
    individual_2_copy = deepcopy(individual_2)

    random_node: LanguageNode = random.choice(list(individual_1_copy.descendants)[1:])
    allowed_swaps = TREE_CONFIG[random_node.node_type].allowed_swaps

    swap_candidates_generator = PreOrderIter(individual_2_copy, filter_=lambda node: node.node_type in allowed_swaps)
    swap_candidates = list(swap_candidates_generator)
    if not swap_candidates:
        return individual_1_copy, individual_2_copy

    node_to_swap: LanguageNode = random.choice(swap_candidates)
    swap_parents(random_node, node_to_swap)
    return individual_1_copy, individual_2_copy


def calculate_fitness(
    individual: Individual,
    interpreter: Interpreter,
    fitness_function: FitnessFunction,
    program_inputs: list[list[Expression]],
) -> float:
    individual_as_str = individual.build_str()
    try:
        parsed_individual = interpreter.parse_str(data=individual_as_str)
    except LanguageException:
        raise IncorrectIndividualException(individual=individual)

    if not program_inputs:
        output = interpreter.interpret_tree(
            tree=parsed_individual,
            program_input=[],
        )
        return fitness_function([output])

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
    with open(file_path, "w+") as file:
        file.write(str(individual))
