import pickle  # noqa: S403
import random
from typing import Callable, Protocol

from anytree import PreOrderIter

from gp_algorithm.grammar import GRAMMAR, NodeType
from gp_algorithm.nodes import LanguageNode, random_value, swap_parents


class Individual(LanguageNode):
    def __init__(self, size: int = 0) -> None:
        super().__init__(node_type=NodeType.PROGRAM)
        for _ in range(size):
            self.grow()

    def mutate(self) -> None:
        mutate_candidates = PreOrderIter(self, filter_=lambda node: node.value is not None)
        node_to_mutate: LanguageNode = random.choice(list(mutate_candidates))  # noqa: S311
        node_to_mutate.value = random_value(node_to_mutate.node_type)

    def cast_to_str(self) -> str:
        return ""

    def save_to_file(self, file_name: str) -> None:
        with open(file_name, "wb+") as file:
            pickle.dump(self, file)


def read_individual_from_file(file_name: str) -> Individual:
    with open(file_name, "rb") as file:
        return pickle.load(file)  # noqa: S301


def random_crossover(
    individual_1: Individual,
    individual_2: Individual,
) -> None:
    random_node: LanguageNode = random.choice(list(individual_1.descendants))  # noqa: S311
    allowed_swaps = GRAMMAR[random_node.node_type].allowed_swaps
    allowed_swaps.add(random_node.node_type)

    swap_candidates = PreOrderIter(individual_2, filter_=lambda node: node.node_type in allowed_swaps)
    if not swap_candidates:
        return

    node_to_swap: LanguageNode = random.choice(list(swap_candidates))  # noqa: S311
    swap_parents(random_node, node_to_swap)


class IndividualInterpreter(Protocol):
    def interpret_str(self, data: str, inputs: list[str]) -> list[str]:
        ...


def calculate_fitness(
    interpreter: IndividualInterpreter,
    individual: Individual,
    fitness_function: Callable[[list[str], list[str]], float],
    input_list: list[list[str]],
    expected_output_list: list[list[str]],
) -> float:
    fitness: float = 0
    for inputs, expected_outputs in zip(input_list, expected_output_list):
        actual_outputs = interpreter.interpret_str(
            data=individual.cast_to_str(),
            inputs=inputs,
        )
        fitness += fitness_function(actual_outputs, expected_outputs)

    return fitness
