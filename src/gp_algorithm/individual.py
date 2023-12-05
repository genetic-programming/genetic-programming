import random
from typing import Callable

from anytree import PreOrderIter

from gp_algorithm.grammar import GRAMMAR, NodeType
from gp_algorithm.interpreter.interpreter import Interpreter
from gp_algorithm.nodes import LanguageNode, random_value, swap_parents


class Individual(LanguageNode):
    def __init__(self, size: int = 0) -> None:
        super().__init__(node_type=NodeType.PROGRAM)
        for _ in range(size):
            self.grow()

    def mutate(self) -> None:
        mutate_candidates = PreOrderIter(self, filter_=lambda node: node.value is not None)
        node_to_mutate: LanguageNode = random.choice(list(mutate_candidates))
        node_to_mutate.value = random_value(node_to_mutate.node_type)


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
