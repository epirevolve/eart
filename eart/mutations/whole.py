# -*- coding: utf-8 -*-

from ..indivisual import Individual


class WholeMutation:
    def run(self, individual):
        individual = Individual.protobiont(individual.born_at)
        return individual
