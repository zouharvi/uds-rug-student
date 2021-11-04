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

    users_d_pt0 = [
        100 * np.average([x["correct"]for x in user if x["pt"] == 0])
        for user in data_test.values()
        if user[0]["group"] == "difficulty"
    ]
    users_d_pt1 = [
        100 * np.average([x["correct"]for x in user if x["pt"] == 1])
        for user in data_test.values()
        if user[0]["group"] == "difficulty"
    ]
    print(np.average(users_d_pt0))
    users_cond = [user[0]["group"] for user in data_test.values()]

    # plt.figure(figsize=(8.5, 4.5))

    # plt.bar(
    #     0, users_d_pt0
    # )
    # plt.legend()
    # plt.ylabel("Test accuracy (%)")
    # plt.xlabel("User / Condition")
    # plt.tight_layout()
    # plt.show()
