# -*- coding: utf-8 -*-

import numpy as np

from ..utility import min_len


class MultiPointCrossover:
    def run(self, gene1, gene2):
        gene_size = min_len(gene1, gene2)
        times = np.random.randint(0, gene_size)
        gene3 = gene1[:]
        gene4 = gene2[:]
        for _ in range(times):
            point = np.random.randint(0, gene_size)
            gene3, gene4 = gene3[:point] + gene4[point:], gene4[:point] + gene3[point:]
        return gene3, gene4
