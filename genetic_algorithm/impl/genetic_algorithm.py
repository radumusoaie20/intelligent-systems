import random
import copy


class GeneticAlgorithm:
    """
    Assumes a "higher is better" fitness score. For minimization
    problems, you should invert the score (e.g., return -error or 1/(1+error))
    """

    def __init__(self,
                 population_size: int, fitness_func, create_individual_func,
                 selection_func, crossover_func, mutation_func,
                 crossover_rate: float=0.8, mutation_rate: float=0.1,
                 elitism_count: int=1,
                 explorative_elitism=False,
                 minimize_solution=False):
        """

        :param population_size: The size of a population for a generation
        :param fitness_func: Applied to an individual (returns a score)
        :param create_individual_func: Creates an individual
        :param selection_func: Selects a group of individuals (at least 2)
        :param crossover_func: Combines 2 individuals to form another one (from 2 parents we have 1 child)
        :param mutation_func: Mutates an individual, resulting in different genes (for exploring other solutions)
        :param crossover_rate: The probability of a crossover (0 means no crossover, 1 means always crossover)
        :param mutation_rate: The probability of a mutation (0 means no mutation, 1 means always mutate)
        :param elitism_count: Hlow many individuals with the best fitness score to keep in the next generation from the previous generation
        :param explorative_elitism: If set to `True`, the  best fitness score individuals kept in the next population
        won't be part of the selection population(exploration), otherwise they will be used in the selection(exploitation)
        :param minimize_solution If set to `False`, it will consider the highest fitness scores as characterizing
        an optimum solution, otherwise the lowest.
        """

        self.population_size = population_size
        self.fitness_func = fitness_func
        self.create_individual_func = create_individual_func
        self.selection_func = selection_func
        self.crossover_func = crossover_func
        self.mutation_func = mutation_func

        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.elitism_count = elitism_count

        self.population = []
        self.fitness_scores = []
        self.best_global_individual = None

        self.minimize = minimize_solution
        self.best_current_individual = None

        if minimize_solution is False:
            self.best_global_fitness = -float('inf')
            self.best_current_fitness = -float('inf')
        else:
            self.best_global_fitness = float('inf')
            self.best_current_fitness = float('inf')

        self.generation = 0

        self.explorative_elitism = explorative_elitism

    def _initialize_population(self):
        self.population = [self.create_individual_func() for _ in range(self.population_size)]
        self._calculate_fitness()

    def _calculate_fitness(self):
        self.fitness_scores = [self.fitness_func(individual) for individual in self.population]

        if self.minimize:
            self.best_current_fitness = min(self.fitness_scores)
        else:
            self.best_current_fitness = max(self.fitness_scores)

        best_current_index = self.fitness_scores.index(self.best_current_fitness)
        self.best_current_individual = copy.deepcopy(self.population[best_current_index])

        if self.minimize:
            condition = self.best_current_fitness < self.best_global_fitness
        else:
            condition = self.best_current_fitness > self.best_global_fitness

        if condition:
            self.best_global_fitness = self.best_current_fitness
            self.best_global_individual = copy.deepcopy(self.population[best_current_index])

    def _evolve_one_generation(self):
        new_population = []

        # 1. Elitism: Carry over the best individuals

        # sort based on fitness score
        self.population = sorted(self.population, key= lambda ind: self.fitness_func(ind), reverse=self.minimize is False)

        #  put the best in the new_population
        new_population.extend(self.population[:self.elitism_count])

        # 2. Fill the rest of the population with new offspring
        num_offspring = self.population_size - self.elitism_count
        children = []


        if self.explorative_elitism is True:
            selection_pool = self.population[self.elitism_count:]
        else:
            selection_pool = self.population

        while len(children) < num_offspring:
            # 2a. Selection
            parent1, parent2 = self.selection_func(selection_pool, self.fitness_scores)

            # 2b. Crossover
            if random.random() < self.crossover_rate:
                child1, child2 = self.crossover_func(parent1, parent2)
            else:
                # No crossover, parents pass through (cloned)
                child1 = copy.deepcopy(parent1)
                child2 = copy.deepcopy(parent2)

            # 2c. Mutation
            if random.random() < self.mutation_rate:
                child1 = self.mutation_func(child1)
            if random.random() < self.mutation_rate:
                child2 = self.mutation_func(child2)

            children.append(child1)
            if len(children) < num_offspring:
                children.append(child2)

        # 4. Add the new children to the population
        new_population.extend(children)
        self.population = new_population[:self.population_size]  # Ensure exact size

        # 5. Re-evaluate the new population
        self._calculate_fitness()
        self.generation += 1

    def run(self, num_generations: int, verbose=True):
        """
        Runs the GA for the given number of generations
        :param num_generations: The number of generations
        :param verbose: If the output shall be printed
        :return: The best global individual and the best global fitness function
        """
        self._initialize_population()

        if verbose:
            print(f"Generation 0: Best Fitness = {self.best_global_fitness}")

        for gen in range(1, num_generations + 1):
            self._evolve_one_generation()

            if verbose:
                print(f"Generation {gen}: Best Current Fitness = {self.best_current_fitness}")

        if verbose:
            print("\nOptimization finished.")
            print(f"Best Global individual: {self.best_global_individual}")
            print(f"Best Global fitness: {self.best_global_fitness}")

        return self.best_global_individual, self.best_global_fitness