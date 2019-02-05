# -*- coding: utf-8 -*-

import numpy as np
from .indivisual import Individual


class Genetic:
    def __init__(self, *, evaluation,
                 gene_kind, gene_size=None,
                 gene_duplicatable=False, homo_progeny_restriction=False,
                 generation_size=100000, population_size=10000,
                 saturated_limit=10):
        self.era = 1

        self._adaptability_history = []
        self._activators: [Individual] = []
        
        gene_kind = list(set(gene_kind))
        if not gene_size:
            gene_size = len(gene_kind)
        self._gene_duplicatable = gene_duplicatable
        if len(gene_kind) != gene_size:
            self._gene_duplicatable = True
        
        Individual.gene_kind = gene_kind
        Individual.gene_size = gene_size
        self._evaluation = evaluation
        self._homo_progeny_restriction = homo_progeny_restriction
        
        self.generation_size = generation_size
        self.population_size = population_size
        
        self.marriage_selection = None
        self.transition_selection = None
        self.mutation = None
        self.crossover = None
        
        self._saturated_limit = saturated_limit

        print("""
Start Eart
==== parameters ====
    gene kind: {}
    gene size: {}
    duplicatable: {}
    homo progeny restriction: {}
    generation size: {}
    population size: {}
        """.format(Individual.gene_kind, Individual.gene_size, self._gene_duplicatable,
                   self._homo_progeny_restriction, self.generation_size, self.population_size))

    def _generate_protobiont(self):
        self._activators = [Individual.protobiont(self.era) for _ in range(self.population_size)]

    def _birth(self):
        _extend = self._activators.extend
        np.random.shuffle(self._activators)
        
        for parent1, parent2 in self.marriage_selection.run(self._activators):
            genes = self.crossover.run(parent1.gene, parent2.gene)
            children = [Individual.new(x, self.era) for x in genes]
            map(lambda x: self.mutation.run(x), children)
            if self._homo_progeny_restriction:
                for child in children:
                    if child.gene in [parent1.gene, parent2.gene]:
                        self.mutation.run(child)
            _extend(children)
        
        self.era += 1
        self.mutation.proliferate()
    
    def _evaluate(self):
        for i in self._activators:
            if not i.adaptability:
                self._evaluation(i)
        self._activators = sorted(self._activators, key=lambda x: x.adaptability, reverse=True)
        self._adaptability_history.append(self._activators[0])

    def _transition(self):
        self._activators = self.transition_selection.run(self._activators)
    
    def _is_saturated(self):
        return len(set(self._adaptability_history[:-self._saturated_limit])) == 1

    def _is_excess_era(self):
        return self.era > self.generation_size

    def _is_terminate(self):
        return self._is_saturated() or self._is_excess_era()

    def init(self):
        self._generate_protobiont()
        self._evaluate()
        return self._adaptability_history[-1]
    
    def _run(self):
        self._birth()
        self._evaluate()
        self._transition()
        return self._adaptability_history[-1]
        
    def run_by_step(self):
        try:
            for _ in range(self.generation_size):
                if self._is_terminate():
                    break
                yield self._run()
        except Exception as e:
            print(e)
    
    def run(self):
        try:
            for _ in range(self.generation_size):
                if self._is_terminate():
                    break
                self._run()
        except Exception as e:
            print(e)
        else:
            return self._adaptability_history[-1]
