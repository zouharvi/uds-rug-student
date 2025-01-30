#!/usr/bin/env python3

import argparse
import csv
import matplotlib.pyplot as plt
import numpy as np
import random

args = argparse.ArgumentParser()
args.add_argument("-d", "--data", default="swahili_english_100.csv")
args.add_argument("-b", "--beta", default=0.5, type=float,
                  help="Weight of the dynamic difficulty")
args.add_argument("-a", "--alpha", default=0.3, type=float,
                  help="Uninformed prior (constant difficulty)")
args.add_argument("-m", "--method", default="min-max",
                  help="Options: min-max, z-like")
args.add_argument("-s", "--shift", default=0.0, type=float,
                  help="How much to shift afterwards")
args.add_argument("--anjali", action="store_true",
                  help="Store in Anjali format: Fact(...)")
args.add_argument("--paper", action="store_true",
                  help="Figure for paper")
args = args.parse_args()

# load data
with open(args.data, "r") as f:
    csv_reader = csv.DictReader(f)
    data = [
        (
            (row["Swahili"], row["English"]),
            float(row["Prop. Correct T1"]),
        )
        for row in csv_reader
    ]
min_diff = min([x[1] for x in data])
max_diff = max([x[1] for x in data])

# define scaling method and estimator
if args.method == "min-max":
    def rescaler(x): return (x - min_diff) / (max_diff - min_diff)
elif args.method == "z-like":
    # almost like a z-score but we subtract minimum to avoid negative difficulty estimates
    std = np.std([x[1] for x in data])
    min_diff = min([x[1] for x in data])
    def rescaler(x): return (x - min_diff) / std
else:
    raise Exception("Unknown scaling method")


def estimator(x): return (1 - args.beta) * \
    args.alpha + args.beta * x - args.shift


data_new = [
    (x[0], max_diff - estimator(rescaler(x[1])))
    for x in data
]

random.shuffle(data_new)

# print data
if args.anjali:
    # Fact(2,"pearl","lulu",0.51),
    for i, ((sw, en), diff) in enumerate(data_new):
        print(f'Fact({i+1}, "{en}", "{sw}", {diff:.3f}),')
else:
    for (sw, en), diff in data_new:
        print(sw, en, diff, sep=",")

# show histograms
bins = np.linspace(0, 1, 41)
if args.paper:
    plt.figure(figsize=(4.5, 3))
plt.hist(
    [x[1] for x in data_new],
    width=0.015,
    color="tab:blue",
    label="New data",
    bins=[b for b in bins],
)
plt.hist(
    [x[1] for x in data],
    width=0.005,
    color="tab:red",
    label="Original data",
    bins=[b + 0.005 for b in bins],
)
# plt.xticks()
plt.xlim(-0.02, 0.55)
plt.xlabel("Difficulty estimate")
plt.ylabel("Number of examples")
if not args.paper:
    plt.title(
        f"Reestimating prior difficulties using\n"
        f"{args.method} scaling,"
        f"and combination {1-args.beta:.2f} $\\cdot$ {args.alpha:.2f} + {args.beta:.2f} $\\cdot$ x + ({args.shift:.2f})",
    )
plt.legend()
plt.tight_layout()
plt.show()
