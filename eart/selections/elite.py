# -*- coding: utf-8 -*-


class EliteSelection:
    def __init__(self, elite_rate=0.05):
        self._elite_rate = elite_rate
    
    def run(self, population):
        return population[:int(self._elite_rate * len(population))]
