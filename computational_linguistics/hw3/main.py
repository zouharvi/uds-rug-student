#!/bin/env python3
import nltk
from collections import defaultdict
from itertools import product
from nltk.tree import *


def process_cfg_grammar(grammar):
    """
    data structure which maps right hand sides to left hand sides
    this is the most common lookup, but could be sped up by using a trie
    the grammar is split up for terminals/non-terminals to increase performance
    """
    grammar_lexical = defaultdict(lambda: set())
    grammar_nonterm = defaultdict(lambda: set())
    for production in grammar.productions():
        # CFG assumption: exactly one terminal
        if production.is_lexical():
            grammar_lexical[production.rhs()].add(production.lhs())
        else:
            grammar_nonterm[production.rhs()].add(production.lhs())
    return grammar_lexical, grammar_nonterm


def cky(grammar_lexical, grammar_nonterm, sent):
    sent_len = len(sent)
    chart = [[set() for _ in range(sent_len-pos)] for pos in range(sent_len)]
    # [tag, ((newCol, tagR), (newRow, tagL))]

    # lexical parts
    for col, token in enumerate(sent):
        tags = grammar_lexical[(token,)]
        chart[col][sent_len-col - 1] = {(tag, None) for tag in tags}

    # go right to left, but skip lexical
    for col, colData in reversed(list(enumerate(chart[:-1]))):
        # go bottom up, but skip lexical
        for row, cell in reversed(list(enumerate(colData[:-1]))):
            for newCol in range(col+1, sent_len-row):
                newRow = sent_len - newCol
                tagsL = chart[col][newRow]
                tagsR = chart[newCol][row]
                for (tagL, _), (tagR, _) in product(tagsL, tagsR):
                    chart[col][row] |= {
                        (newTag, ((newCol, tagR), (newRow, tagL)))
                        for newTag in grammar_nonterm[(tagL, tagR)]
                    }
    return chart


def cky_recognizer(*args):
    """
    returns True if the given sentence can be parsed with the suppplied grammar
    """
    chart = cky(*args)
    for tag, _ in chart[0][0]:
        if tag.symbol() == 'SIGMA':
            return True
    return False


def _cky_subtree(sent, chart, col, row, parent):
    """
    returns a generator of parsed trees
    """
    # reached word
    if row == len(chart) - col - 1:
        for tag, _ in chart[col][row]:
            if tag.symbol() != parent:
                continue
            yield Tree(tag.symbol(), [sent[col]])
    else:
        for tag, ((newCol, tagR), (newRow, tagL)) in chart[col][row]:
            if tag.symbol() != parent:
                continue
            for treeL in _cky_subtree(sent, chart, col, newRow, tagL.symbol()):
                for treeR in _cky_subtree(sent, chart, newCol, row, tagR.symbol()):
                    yield Tree(tag.symbol(), [treeL, treeR])


def cky_generate(grammar_lexical, grammar_nonterm, sent):
    chart = cky(grammar_lexical, grammar_nonterm, sent)
    # start and end indicies
    return _cky_subtree(sent, chart, 0, 0, 'SIGMA')


def _cky_count_partial(chart, col, row, parent):
    """
    returns a generator of parsed trees
    """
    # reached word
    if row == len(chart) - col - 1:
        return len([tag for tag, _ in chart[col][row] if tag.symbol() == parent])
    else:
        return sum([
            _cky_count_partial(chart, col, newRow, tagL.symbol()) *
            _cky_count_partial(chart, newCol, row, tagR.symbol())
            for tag, ((newCol, tagR), (newRow, tagL)) in chart[col][row]
            if tag.symbol() == parent
        ])


def cky_count(*args):
    chart = cky(*args)
    # start and end indicies
    return _cky_count_partial(chart, 0, 0, 'SIGMA')


# load the grammar and sentences
grammar = nltk.data.load("grammars/atis-grammar-cnf.cfg")
sents = nltk.data.load("grammars/atis-test-sentences.txt")
sents = nltk.parse.util.extract_test_sentences(sents)

grammar_lexical, grammar_nonterm = process_cfg_grammar(grammar)
parser = nltk.parse.BottomUpChartParser(grammar)

for sent, _ in sents:
    # print(' '.join(sent))
    # print(cky_recognizer(grammar_lexical, grammar_nonterm, sent))
    # tree_generator = cky_generate(grammar_lexical, grammar_nonterm, sent)
    # print(' '.join(sent), '\t', len(list(tree_generator)), sep='')
    # for tree in tree_generator:
    #     tree.pretty_print()
    tree_count = cky_count(grammar_lexical, grammar_nonterm, sent)
    print(' '.join(sent), '\t', tree_count, sep='')
