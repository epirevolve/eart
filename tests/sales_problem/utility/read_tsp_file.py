# -*- coding: utf-8 -*-

import json


def read_text(file):
    def _separate(s):
        _s = s.split()
        return int(_s[0]), int(_s[1])
    with open(file, 'r') as f:
        data = f.readlines()
    return [(_separate(a)) for a in data]


def read_json(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return [(int(j.x), int(j.y)) for j in data]
