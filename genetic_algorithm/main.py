from genetic_algorithm.impl.genetic_algorithm import GeneticAlgorithm
import example.one_max.one_max as ex


ga_onemax = GeneticAlgorithm(
    population_size=100,
    fitness_func=ex.onemax_fitness,
    create_individual_func=ex.create_binary_individual,
    selection_func=ex.select_two_parents,
    crossover_func=ex.one_point_crossover,
    mutation_func=ex.bit_flip_mutation,
    crossover_rate=0.8,
    mutation_rate=0.05,
    elitism_count=2
)

best_ind, best_fit = ga_onemax.run(num_generations=50, verbose=True)