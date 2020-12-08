#!/bin/env python3
import nltk

# load the grammar and sentences
grammar = nltk.data.load("grammars/atis-grammar-cnf.cfg")
sents = nltk.data.load("grammars/atis-test-sentences.txt")
sents = nltk.parse.util.extract_test_sentences(sents)
parser =  nltk.parse.BottomUpChartParser(grammar)

for sent, _ in sents:
    try:
        no_trees = len(list(parser.parse(sent)))
    except Exception:
        no_trees = 0
    print(' '.join(sent), '\t', no_trees)