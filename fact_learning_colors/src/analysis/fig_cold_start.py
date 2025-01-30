#!/usr/bin/env python3

from collections import defaultdict
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

    items_all = defaultdict(lambda: [])
    for user in data_main.values():
        items = defaultdict(lambda: [])
        for item in user:
            items[item["fact_id"]].append((item["alpha"], item["priora"]))

        for fact_id, item in items.items():
            items_all[fact_id].append(item[-1])

    plot_data_l = []
    plot_data_r = []
    for fact_id, item in items_all.items():
        alpha_avg = np.average([x[0] for x in item])
        priora = item[0][1]
        if len(item) > 10:
            plot_data_l.append(priora)
            plot_data_r.append(alpha_avg)

    # for l, r in zip(plot_data_l, plot_data_r):
    #     plt.plot([l,r])

    plot_data_l = sorted(list(range(len(plot_data_l))), key=lambda i: plot_data_l[i])
    plot_data_r = sorted(list(range(len(plot_data_r))), key=lambda i: plot_data_r[i])

    print(list(zip(plot_data_l, plot_data_r)))
    for l, r in zip(plot_data_l, plot_data_r):
        plt.plot([l,r], color="tab:red" if np.abs(l-r) > len(plot_data_l)//2 else "gray")
    plt.ylabel("")
    
    plt.show()