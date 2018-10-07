Separate tools for making lists and dealing with duplicates https://stackoverflow.com/a/4453715 UUID

Dealing:
Inputs:
Pregenerated lists of files
Duplicates dir
List of preferred paths (interactive?)


check uuids are different

join uuid and relative path
find if any of joint paths in on list of preferred paths (top down)
if so mark another ones for removal
if no ask user for preferred file and give him path to edit then reprocess



Algorithm:
Join list of files data
Sort by one of sums (shell sorting?)
Move through sums and for identical neighbors check preferred paths https://stackoverflow.com/a/4453715
When match add other files to list of redundant copies
move files from list to duplicates dir


UUID:
os.path.realpath("/dev/disk/by-uuid/74069f36-3b7f-4883-974f-9e6403db800d")
psutil.disk_partitions()
