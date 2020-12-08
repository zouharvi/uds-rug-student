#!/bin/env python3
from collections import defaultdict
import argparse

# # 1 Test with
# is_chomsky_normal_form

# # 2 Compare to supplied cnf 

# # 3 compare to
# nltk.test.unit.test_cfg2chomsky.ChomskyNormalFormForCFGTest (Python class, in 

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--grammar-data', action='store_true',
                    # default="grammars/test.cfg")
                    default="grammars/atis-grammar-original.cfg")
args = parser.parse_args()
to_reduce = []
data = defaultdict(lambda: set())


def is_terminal(symbol):
    return symbol[0] == "'" and symbol[-1] == "'"

with open(args.grammar_data, 'r') as f:
    for i, line in enumerate(f):
        lh_single, rhs = line.rstrip().split(' -> ')
        rhs = rhs.split()
        if len(rhs) > 1:
            for j, rh_single in enumerate(rhs[:-1]):
                # A -> BC
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
            
replace_rules = []
remove_list = set()

# we loop because in every iteration we may break previous invariatns
while True:
    to_reduce = set()
    for lh_single, rhs_set in data.items():
        if lh_single in remove_list:
            continue
        for rhs in rhs_set:
            if len(rhs) == 1 and (not is_terminal(rhs[0])):
                # singleton non-terminal
                to_reduce.add((lh_single, rhs[0]))

    if len(to_reduce) == 0:
        break

    for lh_single, rh_single in list(to_reduce)[:1]:
        data[lh_single] |= data[rh_single]
        remove_list.add(rh_single)
        data[lh_single].remove((rh_single,))
        replace_rules.append((lh_single, (rh_single, lh_single)))

def replace_all(context, replace_rules, symbol):
    for context_head, rule in replace_rules:
        if context_head == context and symbol == rule[0]:
            symbol = rule[1]
    return symbol

# print the output
for lh_single, rhs_set in data.items():
    # if lh_single in remove_list:
    #     continue
    for rhs in rhs_set:
        if len(rhs) == 1:
            print(f'{lh_single} -> {replace_all(lh_single, replace_rules, rhs[0])}')
        else:
            print(f'{lh_single} -> {replace_all(lh_single, replace_rules, rhs[0])} {replace_all(lh_single, replace_rules, rhs[1])}')