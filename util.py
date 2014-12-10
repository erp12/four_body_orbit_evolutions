__author__ = 'Eddie Pantridge'

import math

# merges dict1 and dict2 into 1 dict. Dict2 items will override dict1 when needed.
def merge(dict1, dict2):
    return dict(dict1.items() + dict2.items())

# returns the distance between the two positions.
def distance(x, y, x2, y2):
    return math.sqrt((math.pow(x-x2, 2)) + (math.pow(y-y2, 2)))

# returns length of vector
def length(vec):
    return math.sqrt(math.pow(vec[0], 2) + math.pow(vec[1], 2))

# vector subtraction
def position_sub(v1, v2):
    return [v1[0]-v2[0], v1[1]-v2[1]]

# multiplies a vector by all the scalars in a list
def position_mult_scalars(v, scalars):
    new_vec = v
    for s in scalars:
        new_vec[0] = new_vec[0]*s
        new_vec[1] = new_vec[1]*s
    return new_vec

# divides a vector by all the scalars in a list
def position_div_scalars(v, scalars):
    if type(scalars) == list:
        new_vec = v
        for s in scalars:
            new_vec[0] = new_vec[0]/s
            new_vec[1] = new_vec[1]/s
        return new_vec
    else:
        new_vec = v
        new_vec[0] = new_vec[0]/scalars
        new_vec[1] = new_vec[1]/scalars
        return new_vec

# pairs the elements of a list
def pair_list(l):
    res = []
    for i in range(0, len(l), 2):
        res.append([l[i], l[i+1]])
    return res

# returns the vector sum of all the vectors in vs
def sum_vectors(vs):
    xs = []
    ys = []
    for v in vs:
        xs.append(v[0])
        ys.append(v[1])
    return [sum(xs), sum(ys)]

# Takes a list with sub-lists and flattens it into 1 list
def flatten(l):
    result = []
    for i in l:
        if type(i) == list:
            result += flatten(i)
        else:
            result.append(i)
    return result

# same as range() but works with floats for step
def frange(start, stop, step):
    result = []
    i = start
    while i < stop:
        result.append(i)
        i += step
    return result