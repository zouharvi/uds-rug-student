#!/usr/bin/env python3
from collections import Counter
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file_tsv', type=argparse.FileType('r'))
args = parser.parse_args()

tags = Counter()
sequence = 0  # current sequence length
sequences = []  # sequence lengths
for line in args.file_tsv:
    # every line is tab separated triplet: word position, word, tag
    line = line.strip("\n").split("\t")
    if line == ["*"]:
        sequences.append(sequence)
        sequence = 0
    else:
        sequence += 1
        tags.update([line[2]])

print(f"Max sequence length:  {max(sequences):6.0f}")
print(f"Min sequence length:  {min(sequences):6.0f}")
print(f"Mean sequence length: {sum(sequences)/len(sequences):6.2f}")
print(f"Number of sequences:  {len(sequences):6.0f}")

print("\nTags:")
total = sum(tags.values())
print("\n".join(
    f'{k:<7} {v/total*100:6.2f}%' for k, v in sorted(tags.items(), key=lambda x: -x[1])
))