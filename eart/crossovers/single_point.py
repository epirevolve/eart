# -*- coding: utf-8 -*-

import numpy as np
from ..indivisual import Individual


class SinglePointCrossover:
    def run(self, gene1, gene2):
        gene_size = min(len(gene1), len(gene2))
        point = np.random.randint(0, gene_size)
        gene3 = gene1[:point] + gene2[point:]
        gene4 = gene2[:point] + gene1[point:]
        return gene3, gene4
