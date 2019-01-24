# -*- coding: utf-8 -*-

import numpy as np


def default_counter(start=0):
    idx = start
    while True:
        yield idx
        idx += 1


class Individual:
    gene_size = 0
    
    def __init__(self, id_, gene, generation):
        self.id = id_
        self.gene = gene
        self.born_at = generation
        self.adaptability = 0
    
    @classmethod
    def _random_gene(cls):
        gene = np.arange(cls.gene_size)
        np.random.shuffle(gene)
        return gene
    
    @classmethod
    def new_individual(cls, id_, generation):
        return Individual(id_, cls._random_gene(), generation)
