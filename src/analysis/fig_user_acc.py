#!/usr/bin/env python3

import utils
import argparse
import numpy as np
import matplotlib.pyplot as plt


def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument(
        "-d", "--data", default="data/results/",
        help="Path to the directory containing all results files"
    )
    return args.parse_args()


if __name__ == "__main__":
    args = parse_args()
    data_main, data_test = utils.load_all(args.data, flatten=False)

    print()

    users_pt0 = [
        100 * np.average([x["correct"]for x in user if x["pt"] == 0])
        for user in data_test.values()
    ]
    users_pt1 = [
        100 * np.average([x["correct"]for x in user if x["pt"] == 1])
        for user in data_test.values()
    ]
    users_cond = [user[0]["group"] for user in data_test.values()]

    users_pt0, users_pt1, users_cond = zip(
        *sorted(list(zip(users_pt0, users_pt1, users_cond)), key=lambda x: x[0], reverse=True))

    plt.figure(figsize=(8.5, 4.5))

    plt.plot(
        list(range(len(users_pt0))),
        users_pt0,
        linestyle="-",
        marker=".",
        color="tab:green",
        label="Testing without cues (first)",
    )

    plt.plot(
        list(range(len(users_pt1))),
        users_pt1,
        linestyle="-",
        marker=".",
        color="tab:red",
        label="Testing with cues (second)",
    )
    GROUP_MAP = {
        "difficulty": "D",
        "random": "R",
        "control": "C",
    }
    plt.xticks(
        list(range(len(users_cond))),
        [f"{i+1}\n{GROUP_MAP[x]}" for i, x in enumerate(users_cond)],
    )
    plt.legend()
    plt.ylabel("Test accuracy (%)")
    plt.xlabel("User / Condition")
    plt.tight_layout()
    plt.show()
