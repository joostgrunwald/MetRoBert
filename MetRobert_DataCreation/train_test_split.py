import random

sentences = 38654
splitpoint = 33000

with open('train.tsv','r') as source:
    data = [ (random.random(), line) for line in source ]
data.sort()
source.close()

with open('output.tsv','w') as toshuffle:
    for _, line in data:
        toshuffle.write( line )
toshuffle.close()

currentsentence = 0

train_split = open("train_split.tsv", "w")
test_split = open("test_split.tsv", "w")

with open('output.tsv', 'r') as tosplit:
    for lineno, line in enumerate(tosplit):
        if lineno >= splitpoint:
            test_split.write(line)
        else:
            train_split.write(line)
            
        
