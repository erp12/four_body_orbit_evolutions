__author__ = 'Eddie Pantdige'

import scipy.integrate as ode
import numpy as np
import math
import util as u

import pygame
from pygame.locals import *

print 'Program Starting'

# The basic structure of a body (planet/start)
body = {"mass": 1,
        "x": 0,
        "y": 0,
        "xVel": 0,
        "yVel": 0}

# representation of the earth
earth = {}

# representation of the sun
sun = {}

# test system
test_system = [{"mass": 10,
                "x": -100,
                "y": 0,
                "xVel": 0,
                "yVel": 0},
                {"mass": 10,
                 "x": 100,
                 "y": 0,
                 "xVel": 0,
                 "yVel": 0}]

######################################################################################
# Simulation information
######################################################################################

dt = .1 # time increment
T = 1 # finial time
N = T/dt # num steps
times = u.frange(0, T, dt)

gravity = 1
params = []

def set_params(sys):
    for b in sys:
        params.append(gravity * b["mass"])


def cowells_method(i, sys):
    #print i, " :HIT: ", sys
    temp = []
    for j_ind in range(len(sys)):
        if u.distance(i[0], i[1], sys[j_ind][0], sys[j_ind][1]) > 0:
            pos_sub = u.position_sub([sys[j_ind][0], sys[j_ind][1]],
                                     [i[0], i[1]])
            #print "pos_sub: ", pos_sub
            mult_by_params = u.position_mult_scalars(pos_sub, [params[j_ind]])
            distance_cubed = math.pow(u.distance(i[0], i[1], sys[j_ind][0], sys[j_ind][1]), 3)
            #print mult_by_params, " / ", distance_cubed
            temp.append(u.position_div_scalars(mult_by_params,
                                               [distance_cubed]))
    return u.sum_vectors(temp)

def func(y, t0):
    y_list = np.array(y).tolist()
    vels = y_list[:len(y_list)/2]
    pairs = u.pair_list(y_list[len(y_list)/2:])
    accels = []
    for p in pairs:
        accels.append(cowells_method(p, pairs))
    #print "vels&acc: ", u.flatten(vels + accels)
    return np.array(u.flatten(vels + accels))

def integrate_system(sys):
    initial = []
    for b in sys:
        initial.append(b["x"])
        initial.append(b["y"])
    for b in sys:
        initial.append(b["xVel"])
        initial.append(b["yVel"])

    #print "init: ", initial
    #print "times: ", times
    estimate = ode.odeint(func, np.array(initial), np.array(times))
    estimate = np.array(estimate).tolist()
    return estimate[-1]


#################################################################
# Visualizing the simulation
#################################################################

def run_sim(sys):
    pygame.init()
    screen=pygame.display.set_mode((600, 600), 0, 24)
    caption=pygame.display.set_caption("Evovling Orbits")

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((15, 15, 15))

    set_params(sys)

    system = sys
    running = True


    while running:
        # Get Key Events
        pressed=pygame.key.get_pressed()
        for i in pygame.event.get():
            if i.type==QUIT or pressed[K_ESCAPE]:
                running = False
                exit()

        # Fill background
        screen.blit(background, (0, 0))

        # Draw Circles
        # print "Draw"
        centerX = screen.get_size()[0]/2
        centery = screen.get_size()[1]/2
        for b in system:
            pygame.draw.circle(screen, (200, 200, 200), [int(b["x"]+centerX), int(b["y"]+centery)], 5)
        pygame.display.flip()

        # step system
        estimate = integrate_system(sys)

        xy_pairs = u.pair_list(estimate)
        for p_ind in range(len(xy_pairs)/2):
            system[p_ind]["x"] = xy_pairs[p_ind][0]
            system[p_ind]["y"] = xy_pairs[p_ind][1]
            system[p_ind]["xVel"] = xy_pairs[p_ind+len(xy_pairs)/2][0]
            system[p_ind]["yVel"] = xy_pairs[p_ind+len(xy_pairs)/2][1]

        #print "Frame Finished"





run_sim(test_system)