# -*- coding: utf-8 -*-

import numpy as np
from ..indivisual import Individual


class SinglePoint:
    def __init__(self, gene_size):
        self._gene_size = gene_size
    
    def __call__(self, parent1, parent2, id1, id2, generation):
        point = np.random.randint(0, self._gene_size)
        child1 = Individual(id1, np.hstack((parent1[:point], parent2[point])), generation)
        child2 = Individual(id2, np.hstack((parent2[:point], parent1[point])), generation)
        return child1, child2
