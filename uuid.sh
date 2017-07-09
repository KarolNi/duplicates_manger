my_uuid=...
while IFS=' ' read -r dev mnt remainder; do
  case "$dev" in
  /dev/*)
    if [ "$dev" -ef "/dev/disk/by-uuid/$my_uuid" ]; then
      echo "$my_uuid ($dev) mounted at $mnt"
      break
    fi;;
  esac
done < /proc/mounts
