#!/bin/python3
from collections import Counter

tags = Counter()
sequence = 0
sequences = []
with open("data/sample.tsv", "r") as f:
    for line in f:
        line = line.strip("\n").split("\t")
        if line == ["*"]:
            sequences.append(sequence)
            sequence = 0
        else:
            sequence += 1
            tags.update([line[2]])

print("Max sequence length:", max(sequences))
print("Min sequence length:", min(sequences))
print("Mean sequence length:", sum(sequences)/len(sequences))
print("Number of sequences:", len(sequences))

print("\nTags:")
total = sum(tags.values())
print("\n".join(f'{k:<7} {v/total:.2f}%' for k,v in tags.items()))