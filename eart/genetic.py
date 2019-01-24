# -*- coding: utf-8 -*-

import numpy as np
from .indivisual import (
    Individual, default_counter
)


class Genetic:
    def __init__(self, gene_size, evaluation,
                 selection, mutation, crossover,
                 *,
                 identifier=default_counter,
                 generation_size=10000, population_size=1000, mutate_rate=0.03):
        self.era = 0

        self._adaptability_history = []
        self._activators: [Individual] = []

        Individual.gene_size = gene_size
        self._evaluation = evaluation
        self._selection = selection
        self._mutation = mutation
        self._crossover = crossover
        
        self.identifier = identifier(start=1)

        self._population_size = population_size
        self._generation_size = generation_size

        self._mutation_rate = mutate_rate

        self._individual_threshold = 0.90
        self._society_threshold = 0.85
        self._give_up_threshold = 0.001
        self._until_give_up = 100

    def _generate_protobiont(self):
        self._activators = [Individual.new_individual(i, self.era) for i in range(self._population_size)]

    def _select(self):
        return self._selection(self._activators)

    def _crossover(self, parent1, parent2):
        return self._crossover(parent1, parent2)

    def _mutate(self, children):
        _method = np.random.choice(self._mutation)
        return [_method(c) for c in children]

    def _birth(self):
        _extend = self._activators.extend
        parents = iter(self._select())
        for p1, p2 in zip(parents, parents):
            children = self._crossover(p1, p2, self.identifier, self.era)
            if np.random.rand() < self._mutation_rate:
                map(self._mutate, children)
            _extend(children)
        self.era += 1

    def _evaluate(self):
        for i in self._activators:
            if not i.adaptability:
                self._evaluation(i)
        self._adaptability_history.append(max(self._activators, key=lambda m: m.adaptability))

    def _generation_transition(self):
        self._activators = sorted(self._activators, key=lambda x: x.born_at, reverse=True)[:self._population_size]

    def _is_appeared_adaptable_individual(self):
        return max(self._activators, key=lambda m: m.adaptability) > self._individual_threshold

    def _is_appeared_adaptable_society(self):
        return np.average([i.adaptability for i in self._activators]) > self._society_threshold

    def _cant_evolute_more(self):
        return False

    def _excess_crossover(self):
        return self.era > self._generation_size

    def _is_terminate(self):
        return self._cant_evolute_more() | self._excess_crossover()

    def make_protobiont(self):
        self._generate_protobiont()
        self._evaluate()

    def __call__(self, *args, **kwargs):
        for _ in range(self._generation_size):
            self._birth()
            self._evaluate()
            self._generation_transition()
            yield sorted(self._activators, key=lambda x: x.adaptability, reverse=True)[0]
