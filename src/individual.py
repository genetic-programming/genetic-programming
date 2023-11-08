import random
from typing import Callable

from anytree import PreOrderIter

from nodes import LanguageNode, NodeType, GRAMMAR, swap_parents, random_value


class Individual(LanguageNode):
    def __init__(self) -> None:
        super().__init__(node_type=NodeType.PROGRAM)
        
    def mutate(self) -> None:
        mutate_candidates = PreOrderIter(self, filter_=lambda node: node.value is not None)
        node_to_mutate: LanguageNode = random.choice(list(mutate_candidates))
        node_to_mutate.value = random_value(node_to_mutate.node_type)


def create_individual(size: int) -> Individual:
    individual = Individual()
    
    for _ in range(size):
        individual.grow()
    
    return individual


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


class Interpreter:
    def interpret(self, individual: Individual, inputs: list[str]) -> list[str]:
        return inputs


def calculate_fitness(
    individual: Individual,
    fitness_function: Callable[[list[str], list[str]], float],
    input_list: list[list[str]],
    expected_output_list: list[list[str]],
) -> float:
    fitness = 0
    for inputs, expected_outputs in zip(input_list, expected_output_list):
        actual_outputs = Interpreter().interpret(individual, inputs=inputs)
        fitness += fitness_function(actual_outputs, expected_outputs)
        
    return fitness
