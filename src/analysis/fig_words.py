#!/usr/bin/env python3

import utils
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

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

    exposed_bar = []
    learned_bar = []

    data_test_control = [len(set([l["fact_id"] for l in user])) for user in data_test.values() if user[0]["group"] == "control"]
    data_test_difficulty = [len(set([l["fact_id"] for l in user])) for user in data_test.values() if user[0]["group"] == "difficulty"]
    data_test_random = [len(set([l["fact_id"] for l in user])) for user in data_test.values() if user[0]["group"] == "random"]
    
    data_test_difficulty.pop(-1)
    data_test_random.pop(-2)
    print(f"Control: {np.average(data_test_control):.2f}")
    print(f"Difficulty: {np.average(data_test_difficulty):.2f}")
    print(f"Random: {np.average(data_test_random):.2f}")

    
    print("===Filtered")
    data_test_random.pop(0)


    print(f"Control: {np.average(data_test_control):.2f}")
    print(f"Difficulty: {np.average(data_test_difficulty):.2f}")
    print(f"Random: {np.average(data_test_random):.2f}")
    exposed_bar = [np.average(data_test_control), np.average(data_test_difficulty),np.average(data_test_random)]

    print("===both correct")
    data_test_control = [len(set([l["fact_id"] for l in user if l['pt'] == 0 and l["correct"]]) & set([l["fact_id"] for l in user if l["pt"] == 1 and l["correct"]])) for user in data_test.values() if user[0]["group"] == "control"]
    data_test_difficulty = [len(set([l["fact_id"] for l in user if l["pt"] == 0 and l["correct"]]) & set([l["fact_id"] for l in user if l["pt"] == 1 and l["correct"]])) for user in data_test.values() if user[0]["group"] == "difficulty"]
    
    #for user in data_test.values():
    #    if user[0]["group"] == "random":
    #        print(set([l["fact_id"] for l in user if l["pt"] == 0 and l["correct"]]))
    #        print(set([l["fact_id"] for l in user if l["pt"] == 1 and l["correct"]]))
    #        break

    data_test_random = [len(set([l["fact_id"] for l in user if l["pt"] == 0 and l["correct"]]) & set([l["fact_id"] for l in user if l["pt"] == 1 and l["correct"]])) for user in data_test.values() if user[0]["group"] == "random"]
    print(f"Control: {np.average(data_test_control):.2f}")
    print(f"Difficulty: {np.average(data_test_difficulty):.2f}")
    print(f"Random: {np.average(data_test_random):.2f}")

    
    data_test_difficulty.pop(-1)
    data_test_random.pop(-2)
    print(f"Control: {np.average(data_test_control):.2f}")
    print(f"Difficulty: {np.average(data_test_difficulty):.2f}")
    print(f"Random: {np.average(data_test_random):.2f}")

    print("===filtered")
    data_test_random.pop(0)

    print(f"Control:", " ".join([f"{x:.2f}" for x in data_test_control]))
    print(f"Difficulty:", " ".join([f"{x:.2f}" for x in data_test_difficulty]))
    print(f"Random:", " ".join([f"{x:.2f}" for x in data_test_random]))

    print(f"Control: {np.average(data_test_control):.2f}")
    print(f"Difficulty: {np.average(data_test_difficulty):.2f}")
    print(f"Random: {np.average(data_test_random):.2f}")
    learned_bar = [np.average(data_test_control), np.average(data_test_difficulty),np.average(data_test_random)]


    fig, ax = plt.subplots(figsize=(8,5))
    exposed_idx = np.arange(3)
    bar_width = 0.3
    learned_idx = exposed_idx + bar_width
    
    p1 = ax.bar(exposed_idx, height=exposed_bar, width=bar_width, color = ["yellow","green","red"],label="Exposed")
    p2 = ax.bar(learned_idx, height=learned_bar, width=bar_width, color = ["yellow","green","red"],label="Learned",hatch="\\\\")
    ax.set_ylabel("word number")
    ax.set_xticks(learned_idx-0.15)
    ax.set_xticklabels(('Control', 'Difficulty', 'Random'))
    h1 = mpatches.Patch(facecolor="lightgrey",edgecolor="black",lw=1,label="Exposed")
    h2 = mpatches.Patch(facecolor="lightgrey",edgecolor="black",lw=1,label="Learned",hatch="\\\\")
    plt.legend(handles=[h1,h2])
    plt.tight_layout()
    plt.show()
    