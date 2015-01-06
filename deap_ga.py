__author__ = 'Eddie Pantridge'

import random
from deap import base, creator, tools, algorithms
import math
import numpy
import csv
import multiprocessing

import four_body_integrater
import analize_system
import draw

############################################################
# System arguments
############################################################
SINGLE_THREAD = False
DRAW_WHILE_EVO = False
ERROR_TOLERANCE = 0.01
POPULATION_SIZE = 50
CROSSOVER_PROB = 0.7
MUTATION_PROB = 0.3
MUTATION_SIGMA = 0.3
INDIVIDUAL_SIZE = 20  # 4 Masses, 4 xy position pairs (8 total), 4 xy velocity pairs (8 total)
NUM_BEST_INDS_TO_RECORD = 5
NUM_GENERATIONS = 1000
LENGTH_OF_SIMULATIONS = 800  # not implemented yet
INITIAL_POSITION_MAGNITUDE = 3.0
INITIAL_VELOCITY_MAGNITUDE = 3.0
INITIAL_MASS_MAX = 3.0
MIN_MASS = 0.1
MAX_MASS = 3.0
MIN_POS_VEL = -3.0
MAX_POS_VEL = 3.0

# Global initialization of deap creators needed for creation of individuals
creator.create("Fitness", base.Fitness, weights=(-1.0, -1.0))
creator.create("Individual", list, fitness=creator.Fitness)

def rand_init_pos():
    return random.uniform(-INITIAL_POSITION_MAGNITUDE, INITIAL_POSITION_MAGNITUDE)


def rand_init_vel():
    return random.uniform(-INITIAL_VELOCITY_MAGNITUDE, INITIAL_VELOCITY_MAGNITUDE)


def rand_init_mass():
    return random.uniform(0.0, INITIAL_MASS_MAX)


def create_ind(numMasses, numPositions, numVelocites, creator):
    ind = creator.Individual()
    for i in range(numMasses):
        ind.append(rand_init_mass())
    for i in range(numPositions):
        ind.append(rand_init_pos())
    for i in range(numVelocites):
        ind.append(numVelocites)
    return ind

# Function to evaluate an individual
# Will draw the simulation running
def evaluate(individual):
    estimates = four_body_integrater.get_estimates(individual)
    masses = []
    for i in individual[:4]:
        masses.append(math.fabs(i))
    if DRAW_WHILE_EVO:
        draw.init_draw(estimates, masses)
    return analize_system.total_return_error(estimates, individual[4:]), analize_system.delta_direction(estimates, individual[4:])

# Decorator for mutation and crossover to keep the values in bounds.

def checkBounds():
    def decorator(func):
        def wrapper(*args, **kargs):
            offspring = func(*args, **kargs)
            for child in offspring:
                for i in xrange(len(child)):
                    if i < 4:
                        if child[i] > MAX_MASS:
                            child[i] = MAX_MASS
                        elif child[i] < MIN_MASS:
                            child[i] = MIN_MASS
                    else:
                        if child[i] > MAX_POS_VEL:
                            child[i] = MAX_POS_VEL
                        elif child[i] < MIN_POS_VEL:
                            child[i] = MIN_POS_VEL
            return offspring
        return wrapper
    return decorator

def main():

    #####################################################################################
    # Setting up GA
    #####################################################################################

    toolbox = base.Toolbox()
    # toolbox.register("attribute", rand_init_pos)
    # toolbox.register("massAttr", rand_init_mass)
    # toolbox.register("positionAttr", rand_init_pos)
    # toolbox.register("velocityAttr", rand_init_vel)
    toolbox.register("individual", create_ind, 4, 8, 8, creator)
    #toolbox.register("individual", tools.initRepeat, creator.Individual,
    #                 (toolbox.positionAttr, toolbox),
    #                 n=INDIVIDUAL_SIZE)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Set up multithreading
    if not SINGLE_THREAD:
        pool = multiprocessing.Pool()
        toolbox.register("map", pool.map)

    toolbox.register("mate", tools.cxUniform, indpb=0.5)
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=MUTATION_SIGMA, indpb=0.1)
    toolbox.decorate("mate", checkBounds())
    toolbox.decorate("mutate", checkBounds())
    toolbox.register("select", tools.selNSGA2)
    toolbox.register("evaluate", evaluate)

    # have DEAP keep track of some stats
    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    #stats.register("std", numpy.std)
    stats.register("min", numpy.min)


    #####################################################################################
    # START GA
    #####################################################################################
    pop = toolbox.population(n=POPULATION_SIZE)
    HoF = tools.HallOfFame(NUM_BEST_INDS_TO_RECORD)
    pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=CROSSOVER_PROB, mutpb=MUTATION_PROB, ngen=NUM_GENERATIONS,
                                       stats=stats, halloffame=HoF, verbose=True)

    # Write Hall of Fame to CSV file
    resultFile = open("best_systems.csv", 'wb')
    wr = csv.writer(resultFile)
    wr.writerows(HoF)

    # Print CSV
    for i in range(NUM_BEST_INDS_TO_RECORD):
        print i, "best : ", HoF[i]


if __name__ == "__main__":
    #multiprocessing.freeze_support()
    main()


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