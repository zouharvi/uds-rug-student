#!/bin/python3

import sys
import argparse
import numpy as np
from extractor import *

sents = []
words1 = set()
words2 = set()

parser = argparse.ArgumentParser(description='IBM Model 1')
parser.add_argument('filefw', help='FW algn')
parser.add_argument('filebw', help='BW algn')
args = parser.parse_args()

with open(args.filefw, 'r') as ffw, open(args.filebw, 'r') as fbw:
    for linefw, linebw in zip(ffw, fbw):
        afw = set(linefw.strip('\n').split())
        def parser_bw(x):
            x = x.split('-')
            return f'{x[1]}-{x[0]}'
        abw = {parser_bw(tup) for tup in linebw.strip('\n').split()}
        print(' '.join(x for x in afw & abw))