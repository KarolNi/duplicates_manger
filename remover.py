#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pyscript.py
A simple python script template.
http://ajminich.com/2013/08/01/10-things-i-wish-every-python-script-did/
"""

import argparse

import json
import os

preferred_paths = list()
number_of_copies = 1;
log = open("log", 'w')
paths_to_remove = open("test_to_remove", "w")


def process_duplicate(list_of_files, item, count, ignore_empty=True):
    if ignore_empty:
        if list_of_files[item]['s'] == 0:
            return 0
    # TODO add ignoring filies
    print('\n',item, count, list_of_files[item]['r'])
    paths = list()
    for i in range(count):
        paths.append(list_of_files[item + i]['u'] + ":" + list_of_files[item + i]['r'])
    # if all(x==uuids[0] for x in uuids): # check if all uuids are the same
    common_part = os.path.commonprefix(paths)
    paths_to_leave_unfiltered = list()
    paths_used = list()
    if not preferred_paths:  # list is empty
        print("List of duplicates:")
        for t in paths:
            print(t)
        print("Please select preferred path:")
        t = str(input(common_part))
        preferred_paths.append(common_part + t)  # TODO validate
    for preferred_path in preferred_paths:
        if any(preferred_path in path_used for path_used in paths_used):  # TODO check if preferred_paths are sorted from more specific to less specific
            print('\t',preferred_path, paths_used)
            continue
        if len(preferred_path) <= len(common_part): # this preferred path is to short to be valid
            continue
        for path in paths:
            if preferred_path in path: # possible match to keep
                if preferred_path in paths_used: # too wide definition of preferred path - needs narrowing
                    #append list
                    print("List of preferred paths:")
                    for t in preferred_paths:
                        print(t)
                    print("List of duplicates:")
                    for t in paths:
                        print(t)
                    print("Please narrow preferred path:")
                    t = str(input(preferred_path))
                    index = preferred_paths.index(preferred_path)
                    preferred_paths[index] = preferred_path + t # TODO validate
                    preferred_paths.insert(index+1, preferred_path)  # TODO check if leaving old path is OK in case of number_of_copies>1
                    return 1
                paths_used.append(preferred_path)
                paths_to_leave_unfiltered.append(path)
# If more then one file is in the same preferred path ask for clarification (return 1)
    paths_to_leave = list()
    for i in range(number_of_copies):
        try:
            paths_to_leave.append(paths_to_leave_unfiltered[i])
        except IndexError: # add new preferred path to specific position in list
            print("List of preferred paths:")
            j = 0
            while j < len(preferred_paths):
                print(str(j) + ": " + preferred_paths[j])
                j = j+1
            print("List of duplicates:")
            for t in paths:
                print(t)
            print("Please add new preferred path:")
            t = str(input(common_part))
            num = int(input("position:"))
            preferred_paths.insert(num, common_part + t)  # TODO validate
            return 2
    for t in paths_to_leave:
        paths.remove(t)
    paths_to_remove.write('\n'.join(paths) + '\n')
    return 0



def get_hash(list_of_files, item):
    try:
        return list_of_files[item]['sha512']
    except IndexError:
        return None


def main():
    list_file = 'test_sums.json'
    list_of_files = json.load(open(list_file))
    list_of_files = sorted(list_of_files, key=lambda file: file['sha512'])

    global preferred_paths
    preffered_paths_file = 'test_preffered_paths.csv'
    with open(preffered_paths_file,'r') as f:
        preferred_paths = preferred_paths + f.read().splitlines()

    # find duplicates
    i = 0
    while i < len(list_of_files):
        count = 1
        while get_hash(list_of_files, i) == get_hash(list_of_files, i + count): # get_hash(list_of_files, i) == get_hash(list_of_files, i + 1 + count):
            count += 1
        if count > number_of_copies:
            while (process_duplicate(list_of_files, i, count)):  # reprocess duplicate until sufficient list of preferred paths is created
                pass
        elif count < number_of_copies:
            log.write("To low number of copies: " + list_of_files[i]['u'] + ":" + list_of_files[i]['r'] + "\t" + list_of_files[i]['sha512'] + "\n")

        i += 1 + count




if __name__ == '__main__':
    main()
