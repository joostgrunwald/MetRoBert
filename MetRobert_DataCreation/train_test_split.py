import random

with open('train.tsv','r') as source:
    data = [ (random.random(), line) for line in source ]
data.sort()

with open('output.tsv','w') as target:
    for _, line in data:
        target.write( line )