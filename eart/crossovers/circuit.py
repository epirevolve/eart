# -*- coding: utf-8 -*-

import numpy as np

from ..utility import min_len


class CircuitCrossover:
    def run(self, gene1, gene2):
        gene_size = min_len(gene1, gene2)
        gene3 = ['_' for _ in range(gene_size)]
        gene4 = ['_' for _ in range(gene_size)]
    
        r = np.random.randint(0, gene_size)
        while gene1[r] not in gene3:
            gene3[r] = gene1[r]
            gene4[r] = gene2[r]
            r = gene1.index(gene2[r])
        p1_get = (p1 for p1 in gene1 if p1 not in gene4)
        p2_get = (p2 for p2 in gene2 if p2 not in gene3)
        
        gene3 = [x if x != '_' else next(p2_get) for x in gene3]
        gene4 = [x if x != '_' else next(p1_get) for x in gene4]
        return gene3, gene4
