import json
from os import listdir
from os.path import isfile, join

files = [f for f in listdir('./') if isfile(join('./', f)) and '.json' in f]

combined = []

for file in files:
    with open(file, 'r') as f:
        data = json.load(f)
        for d in data:
            combined.append(d)
    print(file)

with open("combined.json", 'w') as f:
    json.dump(combined, f)
