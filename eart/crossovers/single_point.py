# -*- coding: utf-8 -*-

import numpy as np
from ..indivisual import Individual


def single_point_crossover(parent1, parent2, generation):
    gene_size = min(len(parent1.gene), len(parent2.gene))
    point = np.random.randint(0, gene_size)
    child_gene1 = parent1.gene[:point] + parent2.gene[point:]
    child_gene2 = parent2.gene[:point] + parent1.gene[point:]
    child1 = Individual.new(child_gene1, generation)
    child2 = Individual.new(child_gene2, generation)
    return child1, child2
