# -*- coding: utf-8 -*-

import numpy as np

from ..utility import min_len


class UniformityOrderlyCrossover:
    def run(self, gene1, gene2):
        gene_size = min_len(gene1, gene2)
        mask = [0 if np.random.rand() <= 0.5 else 1 for _ in range(gene_size)]
