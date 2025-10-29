import random

CHROMOSOME_LENGTH = 50

def create_binary_individual() -> list[int]:
    return [random.randint(0, 1) for _ in range(CHROMOSOME_LENGTH)]


def onemax_fitness(individual) -> int:
    return sum(individual)


def select_two_parents(population, fitness_scores) -> list[list[int]]:
    return random.sample(population, 2)


def one_point_crossover(parent1, parent2) -> tuple[list[int], list[int]]:
    length = len(parent1)
    point = random.randint(1, length - 1)

    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]

    return child1, child2


def bit_flip_mutation(individual) -> list[int]:
    mutated_individual = individual[:]

    index = random.randint(0, len(mutated_individual) - 1)
    mutated_individual[index] = 1 - mutated_individual[index]

    return mutated_individual
