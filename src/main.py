#!/usr/bin/env python3

import argparse
import csv
from model_book import CustomBert

def parse_arg():
    arg = argparse.ArgumentParser()
    arg.add_argument("-d", "--data", default="../data/reviews_test.csv")
    return arg.parse_args()

def read_data(path):
    with open(path, "r") as f:
        return list(csv.reader(f))

if __name__ == "__main__":
    args = parse_arg()
    data = read_data(args.data)

    model = CustomBert()
    data = model.preprocess(data)
    model.train_epochs(data)