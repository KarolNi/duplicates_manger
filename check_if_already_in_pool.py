#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pyscript.py
A simple python script template.
http://ajminich.com/2013/08/01/10-things-i-wish-every-python-script-did/

usage: check_if_already_in_pool.py pool.json candidates.json result.json
"""

# import argparse

import json
import os
import sys



def check_if_already_in_pool(list_of_candidates, list_of_pool):
    list_of_candidates = sorted(list_of_candidates, key=lambda file: file['sha512'])
    list_of_pool = sorted(list_of_pool, key=lambda file: file['sha512'])
    i = 0
    ret = list()
    for candidate in list_of_candidates:
        while candidate['sha512'] > list_of_pool[i]['sha512']:  # other file in pool
            i = i+1
            if i >= len(list_of_pool):
                break
        if i >= len(list_of_pool):
            break
        if candidate['sha512'] == list_of_pool[i]['sha512']:  # same file
            continue
        if candidate['sha512'] < list_of_pool[i]['sha512']:  # file is not present in pool
            ret.append(candidate)
            continue

    return ret

def main():
    candidates_file = sys.argv[2]
    list_of_candidates = json.load(open(candidates_file))

    pool_file = sys.argv[1]
    list_of_pool = json.load(open(pool_file))


    data = check_if_already_in_pool(list_of_candidates, list_of_pool)

    f = open(sys.argv[3], 'w')
    f.write(json.dumps(data))
    f.close()


if __name__ == '__main__':
    main()
