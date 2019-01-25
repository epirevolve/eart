# -*- coding: utf-8 -*-

import numpy as np


def invert_mutation(individual):
    rp = np.random.randint(0, len(individual.gene), size=2)
    if rp[0] > rp[1]:
        rp[0], rp[1] = rp[1], rp[0]
    individual.gene[rp[0]:rp[1]] = reversed(individual.gene[rp[0]:rp[1]])
    return individual
