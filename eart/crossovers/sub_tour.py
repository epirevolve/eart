# -*- coding: utf-8 -*-

import numpy as np

from ..utility import min_len


class SubTourCrossOver:
    def __init__(self, min_count=3, max_count=None):
        self._min_count = min_count
        self._max_count = max_count
    
    def run(self, gene1, gene2):
        gene_size = min_len(gene1, gene2)
        if not self._max_count:
            self._max_count = int(gene_size / 10)
