# -*- coding: utf-8 -*-

import numpy as np


def default_counter(start=0):
    idx = start
    while True:
        yield idx
        idx += 1


class Individual:
    gene_size = 0
    identifier = default_counter(1)
    
    def __init__(self, id_, gene, generation):
        self.id = id_
        self.gene = gene
        self.born_at = generation
        self.adaptability = 0
    
    @staticmethod
    def _random_gene():
        gene = Individual.gene_kind[:] if len(Individual.gene_kind) == Individual.gene_size\
            else np.random.choice(Individual.gene_kind, Individual.gene_size)
        np.random.shuffle(gene)
        return gene
    
    @staticmethod
    def protobiont(generation):
        return Individual(next(Individual.identifier), Individual._random_gene(), generation)
    
    @staticmethod
    def new(gene, generation):
        return Individual(next(Individual.identifier), gene, generation)
