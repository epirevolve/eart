# -*- coding: utf-8 -*-

import numpy as np


class Translocating:
    def __call__(self, individual):
        reverse_point = np.random.randint(0, len(individual.gene), size=2)
        x = individual.gene[reverse_point[0]]
        individual.gene[reverse_point[0]] = individual.gene[reverse_point[1]]
        individual.gene[reverse_point[1]] = x
        return individual
