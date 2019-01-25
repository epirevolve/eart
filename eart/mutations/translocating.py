# -*- coding: utf-8 -*-

import numpy as np


def translocate_mutation(individual):
    point = np.random.randint(0, len(individual.gene), size=2)
    individual.gene[point[0]], individual.gene[point[1]] =\
        individual.gene[point[1]], individual.gene[point[0]]
    return individual
