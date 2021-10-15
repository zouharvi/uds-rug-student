#!/usr/bin/env python3

import argparse
import csv
from model_book import CustomBert
from misc.utils import *

def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument("-d", "--data", default="data/u1_classlabeled.csv")
    args.add_argument("-l", "--level", type=int, default=1)
    args.add_argument("-m", "--model-name", default='bert')
    args.add_argument("-dc", "--dev-count", type=float, default=100)
    args.add_argument("--do-filter", action="store_true")
    return args.parse_args()

if __name__ == "__main__":
    args = parse_args()
    data = read_data(args.data, level=args.level, do_filter=args.do_filter)
    assert args.dev_count < len(data)
    print(f"Using {len(data)-args.dev_count} for trainig and {args.dev_count} for dev validation, {len(data)} in total")
    data_freq_info(data)

    # model = CustomBert(model_name=args.model_name)
    # data = model.preprocess(data)
    # model.train_data(data[:-args.dev_count], data[-args.dev_count:])