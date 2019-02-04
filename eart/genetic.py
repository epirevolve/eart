# -*- coding: utf-8 -*-

import numpy as np
from .indivisual import Individual
from .selections.selection import (
    MarriageSelection, TransitionSelection
)
from .crossovers import (
    CircuitCrossover, SinglePointCrossover
)
from .mutations import (
    WholeMutation, TranslocateMutation, InvertMutation
)


class Genetic:
    def __init__(self, *, evaluation,
                 gene_kind, gene_size=None,
                 duplicatable=False, homo_progeny_restriction=False,
                 proliferate_mutation=False, proliferate_mutation_max=0.1, proliferate_mutation_rate=0.0001,
                 generation_size=100000, population_size=10000, mutation_rate=0.01):
        self.era = 1

        self._adaptability_history = []
        self._activators: [Individual] = []
        
        gene_kind = list(set(gene_kind))
        if not gene_size:
            gene_size = len(gene_kind)
        self._duplicatable = duplicatable
        if len(gene_kind) != gene_size:
            self._duplicatable = True
        
        Individual.gene_kind = gene_kind
        Individual.gene_size = gene_size
        self._evaluation = evaluation
        self._homo_progeny_restriction = homo_progeny_restriction
        self._proliferate_mutation = proliferate_mutation
        self._proliferate_mutation_max = proliferate_mutation_max
        self._proliferate_mutation_rate = proliferate_mutation_rate
        
        self.generation_size = generation_size
        self.population_size = population_size

        self._mutation_rate = mutation_rate
        
        self.marriage_selection = None
        self.transition_selection = None
        self.mutations = None
        self.crossovers = None
        
        self._individual_threshold = 0.90
        self._society_threshold = 0.85
        self._give_up_threshold = 0.001
        self._until_give_up = 100

        print("""
Start Eart
==== parameters ====
    gene kind: {}
    gene size: {}
    duplicatable: {}
    homo progeny restriction: {}
    proliferate mutation: {}
    proliferate mutation max: {}
    proliferate mutation rate: {}
    generation size: {}
    population size: {}
    mutate rate: {}
        """.format(Individual.gene_kind, Individual.gene_size, self._duplicatable,
                   self._homo_progeny_restriction, self._proliferate_mutation,
                   self._proliferate_mutation_max, self._proliferate_mutation_rate,
                   self.generation_size, self.population_size, self._mutation_rate))

    def _generate_protobiont(self):
        self._activators = [Individual.protobiont(self.era) for _ in range(self.population_size)]

    def _crossover(self, parent1, parent2):
        _method = np.random.choice([SinglePointCrossover().run, CircuitCrossover().run])
        children = _method(parent1, parent2, self.era)
        if self._homo_progeny_restriction:
            for child in children:
                if child.gene in [parent1.gene, parent2.gene]:
                    self._mutate(child)
        return children
    
    def _mutate(self, child):
        _method = np.random.choice([WholeMutation().run, InvertMutation().run, TranslocateMutation().run])
        return _method(child)
    
    def _birth(self):
        _extend = self._activators.extend
        np.random.shuffle(self._activators)
        
        for parent1, parent2 in self.marriage_selection.run(self._activators):
            children = self._crossover(parent1, parent2)
            if np.random.rand() < self._mutation_rate:
                map(self._mutate, children)
            _extend(children)
        
        self.era += 1
        if self._proliferate_mutation and self._mutation_rate < self._proliferate_mutation_max:
            self._mutation_rate += self._proliferate_mutation_rate
    
    def _evaluate(self):
        for i in self._activators:
            if not i.adaptability:
                self._evaluation(i)
        self._activators = sorted(self._activators, key=lambda x: x.adaptability, reverse=True)
        self._adaptability_history.append(self._activators[0])

    def _transition(self):
        self._activators = self.transition_selection.run(self._activators)
        # population = self._activators[:]
        # self._activators.clear()
        # self._activators.extend(elite_selection(population))
        # require_count = int((self._population_size - len(self._activators)) / 10)
        # for i in np.split(np.array(population), 10):
        #     self._activators.extend(roulette_selection(i, require_count))
    
    def _is_appeared_adaptable_individual(self):
        return max(self._activators, key=lambda m: m.adaptability) > self._individual_threshold

    def _is_appeared_adaptable_society(self):
        return np.average([i.adaptability for i in self._activators]) > self._society_threshold

    def _cant_evolute_more(self):
        return False

    def _excess_crossover(self):
        return self.era > self.generation_size

    def _is_terminate(self):
        return self._cant_evolute_more() | self._excess_crossover()

    def make_protobiont(self):
        self._generate_protobiont()
        self._evaluate()
        return self._adaptability_history[-1]

    def __call__(self, *args, **kwargs):
        for _ in range(self.generation_size):
            self._birth()
            self._evaluate()
            self._transition()
            yield self._adaptability_history[-1]
