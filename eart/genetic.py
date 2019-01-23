# -*- coding: utf-8 -*-

import numpy as np
from abc import abstractmethod


class Individual:
    def __init__(self, identifier, gene, generation):
        self.identifier = identifier
        self.gene = gene
        self.born_at = generation
        self.adaptability = 0


class Genetic:
    def __init__(self, gene_size, generation_size=1000000, population_size=10000,
                 elite_rate=0.05, mutate_rate=0.03):
        self.era = 0

        self._adaptability_history = []
        self._moderns: [Individual] = []

        self._gene_size = gene_size

        self._population_size = population_size
        self._generation_size = generation_size

        self._elite_rate = elite_rate
        self._mutation_rate = mutate_rate

        self._individual_threshold = 0.90
        self._society_threshold = 0.85
        self._give_up_threshold = 0.001
        self._until_give_up = 100

    def _random_gene(self):
        gene = np.arange(self._gene_size)
        np.random.shuffle(gene)
        return gene

    def _generate_protobiont(self):
        self._moderns = [Individual(i, self._random_gene(), self.era) for i in range(self._population_size)]

    # belows are selection methods
    def _elite_select(self, population):
        s = sorted(population, key=lambda x: x.adaptability, reverse=True)
        return s[: int(self._elite_rate * self._population_size)]

    @staticmethod
    def _roulette_select(population, demand_count):
        s = sum([w.adaptability for w in population])
        return np.random.choice(population, demand_count, replace=False, p=[w.adaptability/s for w in population])

    @staticmethod
    def _tournament_select(population, demand_count):
        group = np.random.choice(population, (demand_count, 3), replace=False)
        return [max(g, key=lambda f: f.adaptability) for g in group]

    # belows are crossover methods
    def _point_crossover(self):
        pass

    def _multipoint_crossover(self):
        pass

    def _uniformity_crossover(self):
        pass

    @staticmethod
    def _circuit(c, r, g1, g2):
        c[r] = g1[r]
        i = np.where(g1 == g2[r])[0][0]
        c[i] = g1[i]

    def _circuit_crossover(self, gene1, gene2):
        child1 = ['_' for _ in range(self._gene_size)]
        child2 = ['_' for _ in range(self._gene_size)]

        _circuit = self._circuit
        while True:
            r = np.random.randint(self._gene_size)
            if gene1[r] in child1:
                break
            _circuit(child1, r, gene1, gene2)
            _circuit(child2, r, gene2, gene1)
        parent1_get = (p1 for p1 in gene1 if p1 not in child1).__next__
        parent2_get = (p2 for p2 in gene2 if p2 not in child2).__next__
        return [[c1 if c1 != '_' else parent2_get() for c1 in child1],
                [c2 if c2 != '_' else parent1_get() for c2 in child2]]

    @staticmethod
    def _partial(c, x1, x2):
        i1 = np.where(c == x1)[0][0]
        i2 = np.where(c == x2)[0][0]
        c[i1] = x2
        c[i2] = x1

    def _partial_crossover(self, gene1, gene2):
        child1 = gene1[:]
        child2 = gene2[:]
        break_point = np.random.randint(self._gene_size)

        _partial = self._partial
        for i in range(break_point + 1, self._gene_size):
            if child1[i] == child2[i]:
                continue
            x1 = child1[i]
            x2 = child2[i]
            _partial(child1, x1, x2)
            _partial(child2, x1, x2)
        return [child1, child2]

    def _orderly_crossover(self, gene1, gene2):
        break_point = np.random.randint(self._gene_size)
        child1 = gene1[:break_point]
        child2 = gene2[:break_point]
        child1.append([g for g in gene2 if g not in child1])
        child2.append([g for g in gene1 if g not in child2])
        return [child1, child2]

    def _uniformity_orderly_crossover(self):
        pass

    def _uniformity_rank_crossover(self):
        pass

    def _crossover(self, parent1, parent2):
        _methods = [self._circuit_crossover, self._partial_crossover, self._orderly_crossover]
        _method = np.random.choice(_methods)
        return _method(parent1.gene[:], parent2.gene[:])

    # belows are mutation methods
    def _whole_mutate(self, _):
        return self._random_gene()

    def _inverting_mutate(self, gene):
        reverse_point = np.random.randint(0, self._gene_size + 1, size=2)
        if reverse_point[0] > reverse_point[1]:
            x = reverse_point[0]
            reverse_point[0] = reverse_point[1]
            reverse_point[1] = x
        gene[reverse_point[0]:reverse_point[1]] = reversed(gene[reverse_point[0]:reverse_point[1]])
        return gene

    def _translocating_mutate(self, gene):
        reverse_point = np.random.randint(0, self._gene_size, size=2)
        x = gene[reverse_point[0]]
        gene[reverse_point[0]] = gene[reverse_point[1]]
        gene[reverse_point[1]] = x
        return gene

    def _mutate(self, children):
        _methods = [self._whole_mutate, self._inverting_mutate, self._translocating_mutate]
        _method = np.random.choice(_methods)
        return [_method(c) for c in children]

    def _birth(self):
        _extend = self._moderns.extend
        parents = iter(self._tournament_select(self._moderns, int(len(self._moderns)/3)))
        for p1, p2 in zip(parents, parents):
            children = self._crossover(p1, p2)
            if np.random.rand() < self._mutation_rate:
                children = self._mutate(children)
            _extend(Individual(len(self._moderns) + 1, g, self.era) for g in children)
        self.era += 1

    @abstractmethod
    def _evaluate_adaptability(self, i: Individual):
        raise NotImplementedError

    def _evaluate(self):
        for i in self._moderns:
            if not i.adaptability:
                self._evaluate_adaptability(i)
        self._adaptability_history.append(max(self._moderns, key=lambda m: m.adaptability))

    def _generation_transition(self):
        self._moderns = [m for m in self._moderns if self.era - m.born_at <= 2]

    def _is_appeared_adaptable_individual(self):
        return max(self._moderns, key=lambda m: m.adaptability) > self._individual_threshold

    def _is_appeared_adaptable_society(self):
        return np.average([i.adaptability for i in self._moderns]) > self._society_threshold

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
            yield sorted(self._moderns, key=lambda x: x.adaptability, reverse=True)[0]
