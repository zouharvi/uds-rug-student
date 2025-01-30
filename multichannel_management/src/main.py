#!/usr/bin/env python3

import argparse
from model_book import CustomBert, mccc_report
from misc.utils import *
import sklearn.model_selection


def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument("-d", "--data", default="data/joint_labeled.csv")
    args.add_argument("-ds", "--data-second")
    args.add_argument("-t", "--task", type=int, default=1)
    args.add_argument("-m", "--model-name", default='bert')
    args.add_argument("-dc", "--dev-count", type=int, default=None)
    args.add_argument("--dropout", type=float, default=0)
    args.add_argument("--language", "--lang", default='english')
    args.add_argument("--paraphrases", "--pp", action='store_true')
    return args.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.data_second:
        data_t0 = read_data(args.data, language="english",
                            level=0, do_filter=False)
        data_second_t0 = read_data(
            args.data_second, language="english", level=0, do_filter=False)
        data_t1 = read_data(args.data, language="english",
                            level=1, do_filter=False)
        data_second_t1 = read_data(
            args.data_second, language="english", level=1, do_filter=False)
        iaa_report(data_t0, data_second_t0, data_t1, data_second_t1)
        exit()

    if args.task == 1:
        level = 0
        do_filter = False
        if args.dev_count is None:
            args.dev_count = 100
    elif args.task == 2:
        level = 1
        do_filter = True
        if args.dev_count is None:
            args.dev_count = 50
    elif args.task == 3:
        data = read_data(
            args.data, language=args.language,
            level=2, do_filter=False
        )
        print(Counter([x[1] for x in data]))
        exit()
    else:
        raise Exception("Invalid `task` parameter")

    data = read_data(
        args.data, language=args.language,
        level=level, do_filter=do_filter
    )
    data_train, data_dev = sklearn.model_selection.train_test_split(
        data, test_size=args.dev_count, random_state=0
    )

    mccc_report(data_train, data_dev)

    if args.paraphrases:
        print("Expanding paraphrases")
        # cut off development part to not cheat
        data_pp = read_data(
            args.data, language="paraphrase",
            level=level, do_filter=do_filter
        )
        data_pp_train, data_pp_dev = sklearn.model_selection.train_test_split(
            data_pp, test_size=args.dev_count, random_state=0
        )
        data_train += data_pp_train

    print(f"Using {len(data_train)} for trainig and {len(data_dev)} for dev validation, {len(data)+len(data_dev)} in total")
    data_freq_info(data)

    model = CustomBert(model_name=args.model_name, dropout=args.dropout)
    data_train = model.preprocess(data_train)
    data_dev = model.preprocess(data_dev)
    model.train_data(data_train, data_dev)
