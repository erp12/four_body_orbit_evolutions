__author__ = 'Eddie Pantridge'

import scipy.integrate as ode
import numpy as np
import math
import util as u
import draw
import analize_system

# Global simulation variables
gravity = 1
dt = .01
T = 10
N = T/dt+1
times = u.frange(0, T, dt)

def four_body_func(vecs, t, *args):

    pos_1 = vecs[0:2]
    pos_2 = vecs[2:4]
    pos_3 = vecs[4:6]
    pos_4 = vecs[6:8]
    vel_1 = vecs[8:10]
    vel_2 = vecs[10:12]
    vel_3 = vecs[12:14]
    vel_4 = vecs[14:16]

    acc_1_2 = u.position_div_scalars(u.position_mult_scalars( (u.position_sub(pos_2, pos_1)), [args[1]] ),
                                     math.pow(u.length(u.position_sub(pos_2, pos_1)), 3))
    acc_2_1 = u.position_div_scalars(u.position_mult_scalars( (u.position_sub(pos_1, pos_2)), [args[0]] ),
                                     math.pow(u.length(u.position_sub(pos_2, pos_1)), 3))
    acc_3_1 = u.position_div_scalars(u.position_mult_scalars( (u.position_sub(pos_1, pos_3)), [args[0]] ),
                                     math.pow(u.length(u.position_sub(pos_3, pos_1)), 3))
    acc_1_3 = u.position_div_scalars(u.position_mult_scalars( (u.position_sub(pos_3, pos_1)), [args[2]] ),
                                     math.pow(u.length(u.position_sub(pos_3, pos_1)), 3))
    acc_4_1 = u.position_div_scalars(u.position_mult_scalars( (u.position_sub(pos_1, pos_4)), [args[0]] ),
                                     math.pow(u.length(u.position_sub(pos_4, pos_1)), 3))
    acc_1_4 = u.position_div_scalars(u.position_mult_scalars( (u.position_sub(pos_4, pos_1)), [args[3]] ),
                                     math.pow(u.length(u.position_sub(pos_4, pos_1)), 3))
    acc_3_2 = u.position_div_scalars(u.position_mult_scalars( (u.position_sub(pos_2, pos_3)), [args[1]] ),
                                     math.pow(u.length(u.position_sub(pos_3, pos_2)), 3))
    acc_2_3 = u.position_div_scalars(u.position_mult_scalars( (u.position_sub(pos_3, pos_2)), [args[2]] ),
                                     math.pow(u.length(u.position_sub(pos_3, pos_2)), 3))
    acc_4_2 = u.position_div_scalars(u.position_mult_scalars( (u.position_sub(pos_2, pos_4)), [args[1]] ),
                                     math.pow(u.length(u.position_sub(pos_4, pos_2)), 3))
    acc_2_4 = u.position_div_scalars(u.position_mult_scalars( (u.position_sub(pos_4, pos_2)), [args[3]] ),
                                     math.pow(u.length(u.position_sub(pos_4, pos_2)), 3))
    acc_3_4 = u.position_div_scalars(u.position_mult_scalars( (u.position_sub(pos_4, pos_3)), [args[3]] ),
                                     math.pow(u.length(u.position_sub(pos_4, pos_3)), 3))
    acc_4_3 = u.position_div_scalars(u.position_mult_scalars( (u.position_sub(pos_3, pos_4)), [args[3]] ),
                                     math.pow(u.length(u.position_sub(pos_4, pos_3)), 3))

    acc_1 = u.sum_vectors([acc_1_2, acc_1_3, acc_1_4])
    acc_2 = u.sum_vectors([acc_2_1, acc_2_3, acc_2_4])
    acc_3 = u.sum_vectors([acc_3_1, acc_3_2, acc_3_4])
    acc_4 = u.sum_vectors([acc_4_1, acc_4_2, acc_4_3])

    result = np.array(u.flatten([vel_1.tolist(), vel_2.tolist(), vel_3.tolist(), vel_4.tolist(),
                                  acc_1, acc_2, acc_3, acc_4]))
    #print "Result of func: ", result
    return result


def get_estimates(initial_system_state):
    masses = initial_system_state[:4]
    initial = initial_system_state[4:]
    parms = (masses[0]*gravity,
             masses[1]*gravity,
             masses[2]*gravity,
             masses[3]*gravity)

    result_array = ode.odeint(four_body_func, np.array(initial), np.array(times), parms)  # rtol=1e-12, atol=1e-12
    #for step in result_array:
    #    print step[8:]
    #    print step
    return result_array.tolist()

test_system = [1, 1, 1, 1,
               1, 0,
               0, 1,
               -1, 0,
               0, -1,
               0, .8,
               -.8, 0,
               0, -.8,
               .8, 0]

#e = get_estimates(test_system)
#draw.init_draw(e, test_system[:4])
#print
#print analize_system.delta_direction(e, test_system[4:])
