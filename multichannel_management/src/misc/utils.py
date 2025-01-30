#!/usr/bin/env python3

import csv
import numpy as np
import torch
from sklearn.preprocessing import LabelBinarizer
from misc.ontology import ONTOLOGY
import re
from collections import Counter

if torch.cuda.is_available():
    DEVICE = torch.device("cuda")
else:
    DEVICE = torch.device("cpu")
DEVICE_CPU = torch.device("cpu")


def binarize_labels(sents):
    binarizer = LabelBinarizer()
    return (binarizer, binarizer.fit_transform([x[1] for x in sents]))


def read_data(path, language, level=1, do_filter=False):
    with open(path, "r") as f:
        data = list(csv.DictReader(f))

    assert level in {0, 1, 2}
    
    data = [
        (
            sent[language],
            {
                ONTOLOGY[label.strip()][-min(level+1, len(ONTOLOGY[label.strip()]))]
                for label in sent["label"].split(",") if not re.match("^\s*$", label)
            }
        )
        for sent in data
    ]

    for i, (sent_txt, sent_label) in enumerate(data):
        sent_label = list(sent_label)
        if len(sent_label) > 1:
            # pick the first element in indecisive cases
            data[i] = (sent_txt, sent_label[0])
        elif len(sent_label) == 1:
            # get the single element
            data[i] = (sent_txt, sent_label[0])
        else:
            data[i] = (sent_txt, ONTOLOGY[None])

    used_labels = {sent_label for _sent_txt, sent_label in data}
    print(used_labels, "are used")

    if do_filter and level == 1:
        data = [x for x in data if x[1] != "not_interesting"]
    return data


def data_freq_info(data):
    data = Counter([x[1] for x in data])
    print(data)

def iaa_report(data_t0, data_second_t0, data_t1, data_second_t1):
    task_0 = [xl==yl for (x,xl), (y,yl) in zip(data_t0, data_second_t0)]
    print([(x,xl) for x,xl in data_t1 if xl != "not_interesting"][:10])
    task_1 = [xl==yl for (x,xl), (y,yl) in zip(data_t1, data_second_t1) if xl != "not_interesting" and yl != "not_interesting"]
    print(f"Task 1 second annotator ACC: {np.average(task_0):.2%}")
    print(f"Task 2 second annotator ACC: {np.average(task_1):.2%}")