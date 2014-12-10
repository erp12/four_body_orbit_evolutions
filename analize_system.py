__author__ = 'Eddie Panrtidge'

import math
import util as u

##############################
# Position Fitness Functions
##############################

def body_1_pos_error(estimate, initial):
    error = u.distance(estimate[0], estimate[1], initial[0], initial[1])
    return error

def body_2_pos_error(estimate, initial):
    error = u.distance(estimate[2], estimate[3], initial[2], initial[3])
    return error

def body_3_pos_error(estimate, initial):
    error = u.distance(estimate[4], estimate[5], initial[4], initial[5])
    return error

def body_4_pos_error(estimate, initial):
    error = u.distance(estimate[6], estimate[7], initial[6], initial[7])
    return error

##############################
# Velocity Fitness Functions
##############################

def body_1_vel_error(estimate, initial):
    error = u.distance(estimate[8], estimate[9], initial[8], initial[9])
    return error

def body_2_vel_error(estimate, initial):
    error = u.distance(estimate[10], estimate[11], initial[10], initial[11])
    return error

def body_3_vel_error(estimate, initial):
    error = u.distance(estimate[12], estimate[13], initial[12], initial[13])
    return error

def body_4_vel_error(estimate, initial):
    error = u.distance(estimate[14], estimate[15], initial[14], initial[15])
    return error

##################################
# Delta Angle Fitness
##################################

def angle_between_velocities(new_vel, inital_vel):
    return math.fabs(u.length(new_vel)*u.length(inital_vel))


def total_state_angular_fitness(estimate, initial):
    e_pairs = u.pair_list(estimate)
    init_pairs = u.pair_list(initial)
    angles = []
    for i in range(len(e_pairs[4:])):
        angles.append(angle_between_velocities(e_pairs[i], init_pairs[i]))
    return sum(angles)


####################################
# Total Error / Fitness Functions
####################################

def total_state_return_error(estimate, initial):
    return sum([body_1_pos_error(estimate, initial),
                body_2_pos_error(estimate, initial),
                body_3_pos_error(estimate, initial),
                body_4_pos_error(estimate, initial),
                body_1_vel_error(estimate, initial),
                body_2_vel_error(estimate, initial),
                body_3_vel_error(estimate, initial),
                body_4_vel_error(estimate, initial)])

def total_return_error(estimates, initial):
    errors = []
    for e in estimates[5:]:
        #print total_state_error(e, initial)
        errors.append(total_state_return_error(e, initial))
    return min(errors)

def delta_direction(estimates, initial):
    changes_in_direction = [] # in degrees
    for e in estimates:
        changes_in_direction.append(total_state_angular_fitness(e, initial))
    return min(changes_in_direction)
