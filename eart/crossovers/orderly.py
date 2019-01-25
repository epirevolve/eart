# -*- coding: utf-8 -*-

import numpy as np
from ..indivisual import Individual


def orderly_crossover(parent1, parent2, generation):
    gene_size = min(len(parent1.gene), len(parent2.gene))
    break_point = np.random.randint(gene_size)
    child_gene1 = parent1.gene[:break_point]
    child_gene2 = parent2.gene[:break_point]
    child_gene1.extend([x for x in parent2.gene if x not in child_gene1])
    child_gene2.extend([x for x in parent1.gene if x not in child_gene2])
    child1 = Individual.new(child_gene1, generation)
    child2 = Individual.new(child_gene2, generation)
    return child1, child2
