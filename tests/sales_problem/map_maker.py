# -*- coding: utf-8 -*-

import json
import random


cities = []
n_max = 50

for n in range(n_max):
    city = dict()
    city['id'] = n
    city['x'] = (random.random() - 0.5)*2
    city['y'] = (random.random() - 0.5)*2
    cities.append(city)

with open('city_info.json', 'w') as f:
    json.dump(cities, f, sort_keys=True, indent=2)
