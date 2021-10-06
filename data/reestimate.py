#!/usr/bin/env python3

import argparse
import csv
import matplotlib.pyplot as plt
import numpy as np

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


def estimator(x): return (1 - args.beta) * args.alpha + args.beta * x + args.shift


data_new = [
    (x[0], estimator(rescaler(x[1])))
    for x in data
]

# print data to stdout
for (sw, en), diff in data:
    print(sw, en, diff, sep=",")

# show histograms
bins = np.linspace(0, 1, 41)
plt.hist(
    [x[1] for x in data_new],
    width=0.01,
    color="tab:blue",
    label="New data",
    bins=[b + 0.005 for b in bins],
)
plt.hist(
    [x[1] - 0.01 for x in data],
    width=0.01,
    color="tab:red",
    label="Original data",
    bins=[b - 0.005 for b in bins],
)
plt.xticks()
plt.xlabel("Difficulty estimate")
plt.ylabel("Number of examples")
plt.title(
    f"Reestimating prior difficulties using\n"
    f"{args.method} scaling,"
    f"and combination {1-args.beta:.2f} $\\cdot$ {args.alpha:.2f} + {args.beta:.2f} $\\cdot$ x + ({args.shift:.2f})",
)
plt.legend()
plt.show()
