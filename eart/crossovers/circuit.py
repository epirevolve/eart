# -*- coding: utf-8 -*-

import numpy as np
from ..indivisual import Individual


# def circuit_crossover(parent1, parent2, generation):
#     gene_size = min(len(parent1.gene), len(parent2.gene))
#     cg1 = ['_' for _ in range(gene_size)]
#     cg2 = ['_' for _ in range(gene_size)]
#
#     r = np.random.randint(0, gene_size)
#     while parent1.gene[r] not in cg1:
#         cg1[r] = parent1.gene[r]
#         cg2[r] = parent2.gene[r]
#         r = np.where(parent1.gene == parent2.gene[r])[0][0]
#     p1_get = (p1 for p1 in parent1.gene if p1 not in cg1).__next__
#     p2_get = (p2 for p2 in parent2.gene if p2 not in cg2).__next__
#     child1 = Individual.new([c1 if c1 != '_' else p2_get() for c1 in cg1], generation)
#     child2 = Individual.new([c2 if c2 != '_' else p1_get() for c2 in cg2], generation)
#     return child1, child2


class CircuitCrossover:
    @staticmethod
    def _circuit(c, r, g1, g2):
        c[r] = g1[r]
        i = g1.index(g2[r])
        c[i] = g1[i]
    
    def run(self, parent1, parent2, generation):
        gene_size = min(len(parent1.gene), len(parent2.gene))
        child_gene1 = ['_' for _ in range(gene_size)]
        child_gene2 = ['_' for _ in range(gene_size)]
        
        while True:
            r = np.random.randint(gene_size)
            if parent1.gene[r] in child_gene1:
                break
            self._circuit(child_gene1, r, parent1.gene, parent2.gene)
            self._circuit(child_gene2, r, parent2.gene, parent1.gene)
        get_parent_gene1 = (x for x in parent1.gene if x not in child_gene1).__next__
        get_parent_gene2 = (x for x in parent2.gene if x not in child_gene2).__next__
        child1 = Individual.new([x if x != '_' else get_parent_gene2() for x in child_gene1], generation)
        child2 = Individual.new([x if x != '_' else get_parent_gene1() for x in child_gene2], generation)
        return child1, child2
