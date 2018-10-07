#!/user/bin/env python3 -tt
"""
Duplicate detector
"""

# Imports
import sys
import hashlib
import shutil
import json
import os

import MountPointsUUID
from multiprocessing import Process, Queue

#import whrilpool
#import rhash
#import multiprocessing



# Global variables
hashes=['sha512']
mount_points_UUID = MountPointsUUID.MountPointsUUID()
# Class declarations

# Function declarations


def hash_file(path, blocksize=65536):
    out=dict()
    if not hashes:
        return out
    afile = open(path, 'rb')

    sha512er = hashlib.sha512()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        sha512er.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return sha512er.hexdigest()





def scan_file(path):
    out=dict()
    stats=os.stat(path)
    out['p'] = os.path.abspath(path)
    out['u'], out['r'] = mount_points_UUID.UUIDize_paths(path)
    out['s'] = stats.st_size
    out['t'] = stats.st_mtime
    out['sha512'] = hash_file(path)
    #print(out)
    return out


def scan_dir(tree, recursive=True):
    out = list()
    for dirname, dirnames, filenames in os.walk(tree):
        print(dirname) # verbose
        for filename in filenames:
            out.append(scan_file(os.path.join(dirname, filename)))
    return out


def main():
    args = sys.argv[1:]

    if not args:
        print('usage: [--flags options] [inputs] ')
        sys.exit(1)

# Main body
    # print(args)

    t = list()
    for path in args:
        t += scan_dir(path)
    f = open("sums.json", 'w')
    f.write(json.dumps(t))
    f.close()
    # print(t) # debug

if __name__ == '__main__':
    main()
