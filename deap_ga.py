__author__ = 'Eddie Pantridge'

import random
from deap import base, creator, tools, algorithms
import math
import numpy
import csv

import four_body_integrater
import analize_system
import draw

############################################################
# System arguments
############################################################
DRAW_WHILE_EVO = False
ERROR_TOLERANCE = 0.01
POPULATION_SIZE = 50
CROSSOVER_PROB = 0.7
MUTATION_PROB = 0.3
INDIVIDUAL_SIZE = 20 # 4 Masses, 4 xy position pairs (8 total), 4 xy velocity pairs (8 total)
NUM_BEST_INDS_TO_RECORD = 5
NUM_GENERATIONS = 1000
LENGTH_OF_SIMULATIONS = 800
INITIAL_POSITION_MAGNITUDE = 3.0
INITIAL_VELOCITY_MAGNITUDE = 3.0
INITIAL_MASS_MAX = 3.0

####################
# Setting up GA
####################
creator.create("Fitness", base.Fitness, weights=(-1.0, -1.0))
creator.create("Individual", list, fitness=creator.Fitness)

def rand_init_pos():
    return random.uniform(-INITIAL_POSITION_MAGNITUDE, INITIAL_POSITION_MAGNITUDE)

def rand_init_vel():
    return random.uniform(-INITIAL_VELOCITY_MAGNITUDE, INITIAL_VELOCITY_MAGNITUDE)

def rand_init_mass():
    return random.uniform(0.0, INITIAL_MASS_MAX)

def create_ind(numMasses, numPositions, numVelocites):
    ind = creator.Individual()
    for i in range(numMasses):
        ind.append(rand_init_mass())
    for i in range(numPositions):
        ind.append(rand_init_pos())
    for i in range(numVelocites):
        ind.append(numVelocites)
    return ind

toolbox = base.Toolbox()
#toolbox.register("attribute", rand_init_pos)

toolbox.register("massAttr", rand_init_mass)
toolbox.register("positionAttr", rand_init_pos)
toolbox.register("velocityAttr", rand_init_vel)
toolbox.register("individual", create_ind, 4, 8, 8)
#toolbox.register("individual", tools.initRepeat, creator.Individual,
#                 (toolbox.positionAttr, toolbox),
#                 n=INDIVIDUAL_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluate(individual):
    #print individual
    estimates = four_body_integrater.get_estimates(individual)
    masses = []
    for i in individual[:4]:
        masses.append(math.fabs(i))
    if DRAW_WHILE_EVO:
        draw.init_draw(estimates, masses)
    return analize_system.total_return_error(estimates, individual[4:]), analize_system.delta_direction(estimates, individual[4:])

toolbox.register("mate", tools.cxUniform, indpb=0.5)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.1)
toolbox.register("select", tools.selNSGA2)
toolbox.register("evaluate", evaluate)

# have DEAP keep track of some stats
stats = tools.Statistics(key=lambda ind: ind.fitness.values)
stats.register("avg", numpy.mean)
#stats.register("std", numpy.std)
stats.register("min", numpy.min)

stable_system = None

def main():
    pop = toolbox.population(n=POPULATION_SIZE)

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
            if random.random() < CROSSOVER_PROB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTATION_PROB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # The population is entirely replaced by the offspring
        pop[:] = offspring
        #print generation_number
        generation_number += 1

    return pop


def test_main():
    pop = toolbox.population(n=POPULATION_SIZE)
    HoF = tools.HallOfFame(NUM_BEST_INDS_TO_RECORD)
    pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=CROSSOVER_PROB, mutpb=MUTATION_PROB, ngen=NUM_GENERATIONS,
                                       stats=stats, halloffame= HoF, verbose=True)

    # Write Hall of Fame to CSV file
    resultFile = open("best_systems.csv",'wb')
    wr = csv.writer(resultFile)
    wr.writerows(HoF)

    # Print CSV
    for i in range(NUM_BEST_INDS_TO_RECORD):
        print i, "best : ", HoF[i]



if __name__ == "__main__":
    test_main()


# Simple, stable, orbiting system
test_system = [1, 1, 1, 1,
               1, 0,
               0, 1,
               -1, 0,
               0, -1,
               0, .8,
               -.8, 0,
               0, -.8,
               .8, 0]

# Code to be added later
# if fit < ERROR_TOLERANCE-4:
#     is_stable = True
#     global stable_system
#     stable_system = ind
#     print "SOLUTION FOUND!"
#     print ind