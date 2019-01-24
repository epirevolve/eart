# -*- coding: utf-8 -*-

import numpy as np
from ..indivisual import Individual


class Circuit:
    def __call__(self, parent1, parent2, id_, generation):
        gene_size = min(len(parent1.gene), len(parent2.gene))
        cg1 = ['_' for _ in range(gene_size)]
        cg2 = ['_' for _ in range(gene_size)]
    
        r = np.random.randint(0, gene_size)
        while parent1.gene[r] not in cg1:
            cg1[r] = parent1.gene[r]
            cg2[r] = parent2.gene[r]
            r = np.where(parent1.gene == parent2.gene[r])[0][0]
        p1_get = (p1 for p1 in parent1.gene if p1 not in cg1).__next__
        p2_get = (p2 for p2 in parent2.gene if p2 not in cg2).__next__
        child1 = Individual(next(id_), [c1 if c1 != '_' else p2_get() for c1 in cg1], generation)
        child2 = Individual(next(id_), [c2 if c2 != '_' else p1_get() for c2 in cg2], generation)
        return child1, child2
