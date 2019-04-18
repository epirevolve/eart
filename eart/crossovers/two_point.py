# -*- coding: utf-8 -*-

import numpy as np


class TwoPointCrossover:
    def run(self, gene1, gene2):
        gene_size = min(len(gene1), len(gene2))
        points = [np.random.randint(0, gene_size) for _ in range(2)]
        point1 = min(*points)
        point2 = max(*points)
        gene3 = gene1[:point1] + gene2[point1: point2] + gene1[point2:]
        gene4 = gene2[:point1] + gene1[point1: point2] + gene2[point2:]
        return gene3, gene4
