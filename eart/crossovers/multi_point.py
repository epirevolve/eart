# -*- coding: utf-8 -*-

import numpy as np
from ..indivisual import Individual


def multi_point_crossover(parent1, parent2, generation):
    gene_size = min(len(parent1.gene), len(parent2.gene))
    times = np.random.randint(0, gene_size)
    child_gene1 = parent1[:]
    child_gene2 = parent2[:]
    for _ in times:
        point = np.random.randint(0, gene_size)
        child_gene1, child_gene2 =\
            child_gene1.gene[:point] + child_gene2.gene[point:],\
            child_gene2.gene[:point] + child_gene1.gene[point:]
    child1 = Individual.new(child_gene1, generation)
    child2 = Individual.new(child_gene2, generation)
    return child1, child2
