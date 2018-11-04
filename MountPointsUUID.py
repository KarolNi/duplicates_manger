# MountPointsUUID.py
#
# This library provides method to generalize paths to files into form of uuid of device on which file is located and
# path relative to mount point. It provides method to reverse this generalization.
# Its intended use is unambiguously tracking of files on removable disk while connecting to various Linux machines.
#
# Usage:
#  Setup:
#    mount_points_uuid = MountPointsUUID()
#  Getting uuid and relative path pair:
#    mount_points_uuid.UUIDize_paths(file)
#  Getting absolute path from uuid and relative path pair:
#    mount_points_uuid.unUUIDize_paths(uuid, relative_path)
#
# (C) 2017 KarolNi (except find_mount_point() from https://stackoverflow.com/a/4453715 by Fred Foo)
#
# License: BSD-3-Clause (except find_mount_point() from https://stackoverflow.com/a/4453715 by Fred Foo)


import psutil
import os

# TODO abspath

class MountPointsUUID:

    block_devices = dict()
    mount_points = dict()
    uuids = dict()

    def __init__(self):
        for uuid in os.listdir("/dev/disk/by-uuid"):
            block_device = os.path.realpath(os.path.join(os.sep, "dev", "disk", "by-uuid", uuid))
            self.block_devices[block_device] = uuid
        mounted_devices = psutil.disk_partitions()
        for mounted_device in mounted_devices:
            uuid = self.block_devices[mounted_device.device]
            self.mount_points[mounted_device.mountpoint] = uuid
            self.uuids[uuid] = mounted_device.mountpoint

    @staticmethod
    def find_mount_point(path):  # https://stackoverflow.com/a/4453715 by Fred Foo
        path = os.path.abspath(path)
        while not os.path.ismount(path):
            path = os.path.dirname(path)
        return path

    def UUIDize_paths(self, path):
        mount_point = self.find_mount_point(path)
        uuid = self.mount_points[mount_point]
        relative_path = os.path.relpath(path, mount_point)
        return uuid, relative_path

    def unUUIDize_paths(self, uuid, relative_path):
        return os.path.join(self.uuids[uuid], relative_path)

# tests

import unittest


class MountPointsUUIDTestCase(unittest.TestCase):
    def setUp(self):
        self.mount_points_uuid = MountPointsUUID()

    def test_sanity(self):
        uuid, relative_path = self.mount_points_uuid.UUIDize_paths(__file__)
        self.assertEqual(self.mount_points_uuid.unUUIDize_paths(uuid, relative_path), __file__)


def test():
    mount_points_uuid = MountPointsUUID()
    print(mount_points_uuid.mount_points)


if __name__ == '__main__':
    test()
    unittest.main()
