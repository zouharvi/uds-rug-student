#!/usr/bin/env python3

import argparse
import csv
from model_book import CustomBert, mccc_report
from misc.utils import *

def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument("-d", "--data", default="data/joint_labeled.csv")
    args.add_argument("-ds", "--data-second")
    args.add_argument("-t", "--task", type=int, default=1)
    args.add_argument("-m", "--model-name", default='bert')
    args.add_argument("-dc", "--dev-count", type=int, default=100)
    args.add_argument("--dropout", type=float, default=0.3)
    args.add_argument("--language", "--lang", default='english')
    args.add_argument("--paraphrases", "--pp", action='store_true')
    return args.parse_args()

if __name__ == "__main__":
    args = parse_args()
    
    if args.data_second:
        data_t0 = read_data(args.data, language="english", level=0, do_filter=False)
        data_second_t0 = read_data(args.data_second, language="english", level=0, do_filter=False)
        data_t1 = read_data(args.data, language="english", level=1, do_filter=False)
        data_second_t1 = read_data(args.data_second, language="english", level=1, do_filter=False)
        iaa_report(data_t0, data_second_t0, data_t1, data_second_t1)
        exit()
    
    if args.task == 0:
        level = 0
        do_filter = False
    elif args.task == 1:
        level = 1
        do_filter = True
    elif args.task == 2:
        data = read_data(args.data, language=args.language, level=2, do_filter=False)
        print(Counter([x[1] for x in data]))
        exit()
    else:
        raise Exception("Invalid `task` parameter")

    data = read_data(args.data, language=args.language, level=level, do_filter=do_filter)
    mccc_report(data)
    assert args.dev_count < len(data)

    if args.paraphrases:
        print("Expanding paraphrases")
        # cut off development part to not cheat
        data += read_data(args.data, language="paraphrase", level=level, do_filter=do_filter)[args.dev_count:]

    print(f"Using {len(data)-args.dev_count} for trainig and {args.dev_count} for dev validation, {len(data)} in total")
    data_freq_info(data)

    model = CustomBert(model_name=args.model_name, dropout=args.dropout)
    data = model.preprocess(data)
    # model.train_data(data[:-args.dev_count], data[-args.dev_count:])
    model.train_data(data[args.dev_count:], data[:args.dev_count])