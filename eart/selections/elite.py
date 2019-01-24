# -*- coding: utf-8 -*-


class Elite:
    def __init__(self, elite_rate):
        self._elite_rate = elite_rate
    
    def __call__(self, *args, **kwargs):
        population = args
        s = sorted(population, key=lambda x: x.adaptability, reverse=True)
        return s[: int(self._elite_rate * len(population))]
