#!/usr/bin/env python3

import argparse
import csv
from model_book import CustomBert

def parse_arg():
    arg = argparse.ArgumentParser()
    arg.add_argument("-d", "--data", default="../data/reviews_test.csv")
    arg.add_argument("-m", "--model-name", default='bert')
    return arg.parse_args()

def read_data(path):
    with open(path, "r") as f:
        return list(csv.reader(f))

if __name__ == "__main__":
    args = parse_arg()
    data = read_data(args.data)

    model = CustomBert(model_name=args.model_name)
    data = model.preprocess(data)
    model.train_epochs(data)