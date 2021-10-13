#!/usr/bin/env python3

import csv
import torch
from sklearn.preprocessing import LabelBinarizer
from misc.ontology import ONTOLOGY

if torch.cuda.is_available():
    DEVICE = torch.device("cuda")
else:
    DEVICE = torch.device("cpu")
DEVICE_CPU = torch.device("cpu")


def binarize_labels(sents):
    binarizer = LabelBinarizer()
    return (binarizer, binarizer.fit_transform([x[1] for x in sents]))

def reverse_ontology(val, stack=[], ontology_rev={}):
    if type(val) is str:
        if val in ontology_rev:
            print(f"WARNING: {val} is in the ontology at least twice")
        ontology_rev[val] = [val] + stack
    elif type(val) is dict:
        for key, item in val.items():
            reverse_ontology(item, [key] + stack, ontology_rev)
    elif type(val) is list:
        for item in val:
            reverse_ontology(item, stack, ontology_rev)
    else:
        raise Exception("Unknown type")
    return ontology_rev


def ontology_level(ontology, level=None):
    return {k: v[:level][0] for k, v in ontology.items()}


def print_ontology(ontology):
    for k, v in ontology.items():
        print(k, v)


def read_data(path, reviews=False, level=1):
    with open(path, "r") as f:
        data = list(csv.reader(f))

    # if not reviews:
    ontology_rev = reverse_ontology(ONTOLOGY)
    ontology_rev = ontology_level(ontology_rev, level=level)
    data = [
        (sent_txt, ontology_rev[sent_label])
        for sent_txt, sent_label in data
    ]
    used_labels = {sent_label for _sent_txt, sent_label in data}
    all_labels = set(ontology_rev.values())
    print(all_labels - used_labels, "are not represented")
    print(used_labels, "are used")
    return data
