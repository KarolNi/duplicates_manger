#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pyscript.py
A simple python script template.
http://ajminich.com/2013/08/01/10-things-i-wish-every-python-script-did/
"""

import json
import os
import sys
import shutil

def create_dir_tree(path):
    dirname = os.path.dirname(path)
    if (dirname == '' or os.path.exists(dirname)):
        return
    else:
        create_dir_tree(dirname)
        os.mkdir(dirname)

def main():
    list_file = sys.argv[1]
    list_of_files = json.load(open(list_file))

    prefix = sys.argv[2]


    for item in list_of_files:
        path = item['r']
        path_new = (os.path.join(prefix, path))
        create_dir_tree(path_new)
        try:
            shutil.move(path, path_new)
        except FileNotFoundError:
            continue


if __name__ == '__main__':
    main()
