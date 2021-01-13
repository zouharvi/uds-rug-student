from itertools import product
import numpy as np

"""
Extracts hard alignment from scores
"""


def extract(scores_data, agregation):
    data = []
    for scores in scores_data:
        sent_buffer = []
        for tok1_i, probline in enumerate(scores):
            # prefix with current token index
            sent_buffer += [(tok1_i, i) for i in agregation(probline)]
        data.append(sent_buffer)
    return data


def extract_rev(scores_data, agregation):
    data = []
    for scores in scores_data:
        sent_buffer = []
        for tok2_i, prob in enumerate(scores[0]):
            tok2_scores = [scores[i][tok2_i] for i in range(len(scores))]
            # suffix with current token index
            sent_buffer += [(i, tok2_i) for i in agregation(tok2_scores)]
        data.append(sent_buffer)
    return data

def extract_0(*args):
    def agregation(tok_scores):
        return [np.argmax(tok_scores)]

    return extract(*args, agregation=agregation)

def extract_0_rev(*args):
    def agregation(tok_scores):
        return [np.argmax(tok_scores)]

    return extract_rev(*args, agregation=agregation)

def extract_1(*args):
    return extract_3(*args, alpha=1)


def extract_2(*args, alpha):
    def agregation(tok_scores):
        return [i for i, score in enumerate(tok_scores) if score >= alpha]

    return extract(*args, agregation=agregation)

def extract_3(*args, alpha):
    def agregation(tok_scores):
        boundary = np.max(tok_scores)
        boundary = min(boundary*alpha, -np.inf if alpha == 0 else boundary/alpha)
        return [i for i, score in enumerate(tok_scores) if score >= boundary]

    return extract(*args, agregation=agregation)

def extract_4(*args, alpha):
    def agregation(tok_scores):
        boundary = np.max(tok_scores)
        boundary = min(boundary*alpha, -np.inf if alpha == 0 else boundary/alpha)
        return [i for i, score in enumerate(tok_scores) if score >= boundary]

    return extract_rev(*args, agregation=agregation)

def intersect_align(algns1, algns2):
    return [list(set(algn1) & set(algn2)) for algn1, algn2 in zip(algns1, algns2)]