#!/bin/env python3
from collections import defaultdict
import argparse

parser = argparse.ArgumentParser(description='Turn (almost) CNF to ChNF')
parser.add_argument('--grammar-data', action='store_true',
                    default="grammars/atis-grammar-original.cfg")
args = parser.parse_args()

to_reduce = []
data = defaultdict(lambda: set())

def is_terminal(symbol):
    return symbol[0] in "'\"" and symbol[-1] in "'\""

# load grammar data and create new rules by decomposing long ones
with open(args.grammar_data, 'r') as f:
    for i, line in enumerate(f):
        lh_single, rhs = line.rstrip().split(' -> ')
        rhs = rhs.split()
        if len(rhs) > 1:
            # A -> BC
            for j, rh_single in enumerate(rhs[:-1]):
                if j == 0:
                    new_a = lh_single
                else:
                    new_a = f'{i}_{j}_{lh_single}'

                if j == len(rhs) - 2:
                    new_c = rhs[-1]
                else:
                    new_c = f'{i}_{j+1}_{lh_single}'

                data[new_a].add((rh_single, new_c))
        else:
            data[lh_single].add((rhs[0],))

ignore_list = set()
# we loop because in every iteration we may break previous invariants
while True:
    to_reduce = None
    for lh_single, rhs_set in data.items():
        if lh_single in ignore_list:
            continue
        for rhs in rhs_set:
            if len(rhs) == 1 and (not is_terminal(rhs[0])):
                # singleton non-terminal
                to_reduce = (lh_single, rhs[0])
                break
        if to_reduce is not None:
            break

    if to_reduce is None:
        break

    lh_single, rh_single = to_reduce
    data[lh_single] |= data[rh_single]
    data[lh_single].remove((rh_single,))

# print the output
for lh_single, rhs_set in data.items():
    if lh_single in ignore_list:
        continue
    for rhs in rhs_set:
        if len(rhs) == 1:
            print(f'{lh_single} -> {rhs[0]}')
        else:
            print(f'{lh_single} -> {rhs[0]} {rhs[1]}')
