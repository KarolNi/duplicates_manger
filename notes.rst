Separate tools for making lists and dealing with duplicates https://stackoverflow.com/a/4453715 UUID

Dealing:
Inputs:
Pregenerated lists of files
Duplicates dir
List of preferred paths (interactive?)

Algorithm:
Join list of files data
Sort by one of sums (shell sorting?)
Move through sums and for identical neighbors check preferred paths https://stackoverflow.com/a/4453715
When match add other files to list of redundant copies
move files from list to duplicates dir


UUID:
os.path.realpath("/dev/disk/by-uuid/74069f36-3b7f-4883-974f-9e6403db800d")
psutil.disk_partitions()
