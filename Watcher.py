#!/usr/bin/env python3

import pyfuse.ReadonlyPassthrough
import scanner
import mpipe
import sys
import os
import OutputHandler
import signal


class Watcher(pyfuse.ReadonlyPassthrough.ReadonlyPassthrough):
    def __init__(self, watched_path, pipeline):
        self.pipeline = pipeline
        super(Watcher, self).__init__(watched_path)

    def open(self, path, info):
        self.pipeline.put(super(Watcher, self)._full_path(path))
        return super(Watcher, self).open(path, info)


def main(watched_path, mountpoint, logfile="test_log.csv"):
    oh = OutputHandler.OutputHandler(logfile)

    def signal_handler(sig, frame):  # TODO maybe bug - needs two Ctrl+C to exit
        oh.close()

    signal.signal(signal.SIGINT, signal_handler)

    stage1 = mpipe.UnorderedStage(scanner.scan_file, size=3, max_backlog=3)
    stage2 = mpipe.OrderedStage(oh.write, size=1)
    pipeline = mpipe.Pipeline(stage1.link(stage2))

    watcher = Watcher(watched_path, pipeline)
    watcher.main([sys.argv[0], mountpoint], foreground=True)


if __name__ == "__main__":
    main(os.path.expanduser(sys.argv[-2]), os.path.expanduser(sys.argv[-1]))  # TODO abspath
