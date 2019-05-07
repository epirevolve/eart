# -*- coding: utf-8 -*-

import numpy as np

from ..utility import min_len


class MirrorCrossover:
    def run(self, gene1, gene2):
        gene_size = min_len(gene1, gene2)
        mask = [0 if np.random.rand() <= 0.5 else 1 for _ in range(gene_size)]
        gene3 = []
        gene4 = []
        
        for i, (g1, g2) in enumerate(zip(gene1, gene2)):
            if g1 == g2:
                gene3.append(g1)
                gene4.append(g2)
            elif mask[i]:
                gene3.append(g1)
                gene4.append(g2)
            else:
                gene3.append(g2)
                gene4.append(g1)
        return gene3, gene4

