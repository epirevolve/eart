# -*- coding: utf-8 -*-

import numpy as np


class OrderlyCrossover:
    def run(self, gene1, gene2):
        gene_size = min(len(gene1), len(gene2))
        break_point = np.random.randint(gene_size)
        gene3 = gene1[:break_point]
        gene4 = gene2[:break_point]
        gene3.extend([x for x in gene2 if x not in gene3])
        gene4.extend([x for x in gene1 if x not in gene4])
        return gene3, gene4
