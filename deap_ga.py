__author__ = 'Eddie Pantridge'

import random
from deap import base, creator, tools

import four_body_integrater
import analize_system
import draw

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

IND_SIZE = 20

def rand_init_val():
    return random.uniform(0.0, 3.0)

toolbox = base.Toolbox()
toolbox.register("attribute", rand_init_val)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attribute, n=IND_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluate(individual):
    #print individual
    estimates = four_body_integrater.get_estimates(individual)
    draw.init_draw(estimates, individual[:4])
    return [analize_system.total_error(estimates,
                                      individual[4:])]

toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=5)
toolbox.register("evaluate", evaluate)

ERROR_TOLERANCE = 0.01

stable_system = None

def main():
    pop = toolbox.population(n=7)
    CXPB, MUTPB = 0.5, 0.2

    generation_number = 0

    is_stable = False

    # Evaluate the entire population
    fitnesses = map(toolbox.evaluate, pop)
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    while not is_stable:
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = map(toolbox.clone, offspring)

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            if fit < ERROR_TOLERANCE:
                is_stable = True
                global stable_system
                stable_system = ind
                print "SOLUTION FOUND!"
                print ind
            ind.fitness.values = fit

        # The population is entirely replaced by the offspring
        pop[:] = offspring

    return pop

if __name__ == "__main__":
    main()