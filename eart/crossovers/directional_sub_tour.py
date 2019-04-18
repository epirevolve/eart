# -*- coding: utf-8 -*-

from ..utility import min_len
from . import SubTourCrossOver


class DirectionalSubTourCrossOver(SubTourCrossOver):
    def run(self, gene1, gene2):
        gene_size = min_len(gene1, gene2)
        sub_tours = []
        for x in gene1:
            pass
