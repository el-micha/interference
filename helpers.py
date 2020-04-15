import math


# scalars
def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


# vectors
def add(p1, p2):
    return p1[0] + p2[0], p1[1] + p2[1]


def sub(p1, p2):
    return p1[0] - p2[0], p1[1] - p2[1]


def negative(p):
    return times(p, -1)


def times(p, scalar):
    return pointwise_mult(p, (scalar, scalar))


def pointwise_mult(p1, p2):
    return p1[0] * p2[0], p1[1] * p2[1]


def round(p):
    return int(p[0]), int(p[1])