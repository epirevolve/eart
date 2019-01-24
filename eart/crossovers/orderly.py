# -*- coding: utf-8 -*-

import numpy as np
from ..indivisual import Individual


class Orderly:
    def __init__(self, gene_size):
        self._gene_size = gene_size
    
    def __call__(self, parent1, parent2, id_, generation):
        break_point = np.random.randint(self._gene_size)
        c_g1 = parent1.gene[:break_point]
        c_g2 = parent2.gene[:break_point]
        child1 = Individual(id_(), np.hstack((c_g1, [g for g in parent2.gene if g not in c_g1])), generation)
        child2 = Individual(id_(), np.hstack((c_g2, [g for g in parent1.gene if g not in c_g2])), generation)
        return child1, child2
