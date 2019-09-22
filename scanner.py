#!/user/bin/env python3 -tt
"""
Duplicate detector
"""

# Imports
import sys
import hashlib
import shutil
import csv
import os
import zlib
import time

import MountPointsUUID
from multiprocessing import Process, Queue

#import whrilpool
#import rhash
#import multiprocessing



# Global variables
mount_points_UUID = MountPointsUUID.MountPointsUUID()
# Class declarations

# Function declarations


def hash_file(path, block_size=65536, enable_sha512 = True, enable_crc32 = True, integer=False):
    out = dict()

    if (not enable_crc32) and (not enable_sha512):
        return out

    afile = open(path, 'rb')

    if enable_sha512:
        sha512er = hashlib.sha512()
    if enable_crc32:
        crc32 = 0

    buf = afile.read(block_size)
    while len(buf) > 0:
        if enable_sha512:
            sha512er.update(buf)
        if enable_crc32:
            crc32 = zlib.crc32(buf, crc32)
        buf = afile.read(block_size)
    afile.close()

    if enable_sha512:
        if integer:
            out['sha512'] = int.from_bytes(sha512er.digest(), byteorder='big')
        else:
            out['sha512'] = sha512er.hexdigest()
    if enable_crc32:
        if integer:
            out['crc32'] = crc32 & 0xFFFFFFFF
        else:
            out['crc32'] = format(crc32 & 0xFFFFFFFF, '08x')
    return out


def scan_file(path, ignore_symlinks=True):
    if (ignore_symlinks and os.path.islink(path)):
        return
    if (not os.path.isfile(path)):
        return
    out = dict()
    stats = os.stat(path)
    out['p'] = os.path.abspath(path)
    out['u'], out['r'] = mount_points_UUID.UUIDize_paths(path)
    out['s'] = stats.st_size
    out['t'] = stats.st_mtime
    out.update(hash_file(path))
    #print(out)
    return out


def scan_dir(tree, recursive=True, writer=None):
    out = list()
    for dirname, dirnames, filenames in os.walk(tree):
        # print(dirname) # verbose
        for filename in filenames:
            tmp = scan_file(os.path.join(dirname, filename))
            if tmp:
                if(writer):
                    writer(tmp)
                out.append(tmp)
    return out


def main():
    args = sys.argv[1:]

    if not args:
        print('usage: [--flags options] [inputs] ')
        sys.exit(1)

# Main body
    # print(args)

    t = list()
    f = open(str(int(time.time()))+"_DMScan.csv", 'w')
    header = sorted(list(scan_file(os.path.realpath(__file__)).keys()))
    writer = csv.DictWriter(f, header, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    writer.writeheader()
    for path in args:
        t += scan_dir(path, writer=writer.writerow)
    f.close()
    # print(t) # debug

if __name__ == '__main__':
    main()
