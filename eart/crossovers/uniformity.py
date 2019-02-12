# -*- coding: utf-8 -*-

import numpy as np

from ..utility import min_len


class UniformityCrossover:
    def run(self, gene1, gene2):
        gene_size = min_len(gene1, gene2)
        mask = [0 if np.random.randint(0, 1) <= 0.5 else 0 for _ in range(gene_size)]
        gene3 = [gene1[x] if mask[x] == 0 else gene2[x] for x in range(gene_size)]
        gene4 = [gene1[x] if mask[x] == 1 else gene2[x] for x in range(gene_size)]
        return gene3, gene4
