import csv
import json
import sys

output_file = sys.argv.pop(-1) + '.json'
sys.argv.pop(0)

data = list()

for input_file in sys.argv:
  with open(input_file) as file:
    data = data + (list(csv.DictReader(file)))

f = open(output_file, 'w')
f.write(json.dumps(data))
f.close()

