# -*- coding: utf-8 -*-

import numpy as np


class Inverting:
    def __call__(self, individual):
        reverse_point = np.random.randint(0, len(individual.gene), size=2)
        if reverse_point[0] > reverse_point[1]:
            x = reverse_point[0]
            reverse_point[0] = reverse_point[1]
            reverse_point[1] = x
        individual.gene[reverse_point[0]:reverse_point[1]] = reversed(individual.gene[reverse_point[0]:reverse_point[1]])
        return individual
