#!/bin/python3

import sys
import argparse
import numpy as np
from extractor import *

sents = []
words1 = set()
words2 = set()

parser = argparse.ArgumentParser(description='Aligner model')
parser.add_argument('--file1', help='SRC file', default='jhu-mt-hw/hw2/data/hansards.e')
parser.add_argument('--file2', help='TGT file', default='jhu-mt-hw/hw2/data/hansards.f')
parser.add_argument('-n', '--number', help='Number of lines to use', default=None, type=int)
parser.add_argument('-s', '--steps', help='Number of epochs to use', default=5, type=int)
parser.add_argument('-e', '--extractor', help='Which hard alignmnet extractor method to use', default='A0')
parser.add_argument('-d', '--diagonal', help='Prefer diagonal', action='store_true')
args = parser.parse_args()

print('loading data', file=sys.stderr)
with open(args.file1, 'r') as f1, open(args.file2, 'r') as f2:
    def tokenize(sent):
        return [x for x in sent.lower().split() if len(x) != 0]
    fiterator = list(zip(f1, f2))[:args.number] if args.number is not None else zip(f1, f2)
    for line1, line2 in fiterator:
        items1 = tokenize(line1)
        items2 = tokenize(line2)
        if 'NULL' in args.extractor:
            items2 += ['NULL']
        sents.append((items1, items2))
        words1 |= set(items1)
        words2 |= set(items2)


print('generating vocabulary', file=sys.stderr)
words1 = list(words1)
words1 = {k:words1.index(k) for k in words1}
words2 = list(words2)
words2 = {k:words2.index(k) for k in words2}
sents = [
    ([words1[x] for x in sent1], [words2[x] for x in sent2])
    for sent1, sent2 in sents
]

print('generating initial probabilities', file=sys.stderr)
alignment_probs = [
    np.full((len(sent2), len(sent1)), 1/len(sent2))
    for sent1, sent2 in sents
]

# EM
for step in range(args.steps):
    print(f'step {step:>3}', file=sys.stderr)

    # expectation
    words_prob = np.zeros((len(words2), len(words1)))
    for (sent_src, sent_tgt), probs in zip(sents, alignment_probs):
        for word_tgt, probline in zip(sent_tgt, probs):
            for word_src, prob in zip(sent_src, probline):
                words_prob[word_tgt][word_src] += prob
    # normalize rows
    words_prob = (words_prob.T / np.sum(words_prob, axis=1)).T

    # maximization
    for sent_i, (sent_src, sent_tgt) in enumerate(sents):
        probs = np.zeros((len(sent_tgt), len(sent_src)))
        for pos_src, word_src in enumerate(sent_src):
            for pos_tgt, word_tgt in enumerate(sent_tgt):
                probs[pos_tgt][pos_src] = words_prob[word_tgt][word_src]
        # normalize sentence columns
        alignment_probs[sent_i] = probs / np.sum(probs, axis=0)


if args.extractor == 'A0+NULL':
    alignment = extract_0_rev(alignment_probs)
    new_alignment = []
    # remove NULL alignments
    for align, (sent1, sent2) in zip(alignment, sents):
        new_alignment.append([(x,y) for x,y in align if y < len(sent2)-1])
    alignment = new_alignment
elif args.extractor == 'A0':
    alignment = extract_0_rev(alignment_probs)
elif args.extractor == 'A1':
    alignment = extract_1(alignment_probs)
elif args.extractor == 'A2':
    alignment = extract_2(alignment_probs, alpha=0.35)
elif args.extractor == 'A3':
    alignment = extract_3(alignment_probs, alpha=0.98)
elif args.extractor == 'A4':
    alignment = extract_4(alignment_probs, alpha=0.98)
elif args.extractor == 'A2*A3*A4':
    alignment = intersect_align(
        extract_2(alignment_probs, alpha=0.25),
        intersect_align(
            extract_3(alignment_probs, alpha=0.98),
            extract_4(alignment_probs, alpha=0.98),
        )
    )
elif args.extractor == 'A2*A3*A4*diag':
    alignment = intersect_align(
        extract_2(alignment_probs, alpha=0.25),
        intersect_align(
            extract_3(alignment_probs, alpha=0.9),
            extract_4(alignment_probs, alpha=0.9),
        )
    )
elif args.extractor == 'A2*A3*A4*int':
    alignment = intersect_align(
        extract_2(alignment_probs, alpha=0.2),
        intersect_align(
            extract_3(alignment_probs, alpha=0.5),
            extract_4(alignment_probs, alpha=0.5),
        )
    )

if args.diagonal:
    alignment = [
        [(x,y,) for x,y in line if abs(x-y) <= 8]
        for line in alignment
    ]

# output alignment
for alignment_line in alignment:
    print(' '.join([f'{x}-{y}' for x, y in alignment_line]))