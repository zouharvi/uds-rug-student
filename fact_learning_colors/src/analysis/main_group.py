#!/usr/bin/env python3

from typing import Pattern
import utils
import argparse
import numpy as np

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

    data_test_control = np.average([len(set([l["fact_id"] for l in user])) for user in data_main.values() if user[0]["group"] == "control"]) 
    data_test_difficulty = np.average([len(set([l["fact_id"] for l in user])) for user in data_main.values() if user[0]["group"] == "difficulty"])
    data_test_random = np.average([len(set([l["fact_id"] for l in user])) for user in data_main.values() if user[0]["group"] == "random"]) 
    
    print(f"Control: {data_test_control:.2f}")
    print(f"Difficulty: {data_test_difficulty:.2f}")
    print(f"Random: {data_test_random:.2f}")

    data_test_control = ([np.average([l["correct"] for l in user]) for user in data_test.values() if user[0]["group"] == "control"]) 
    data_test_difficulty = ([np.average([l["correct"] for l in user]) for user in data_test.values() if user[0]["group"] == "difficulty"]) 
    data_test_random = ([np.average([l["correct"] for l in user]) for user in data_test.values() if user[0]["group"] == "random"]) 
    print(f"Control:", " ".join([f"{x:.2%}" for x in data_test_control]))
    print(f"Difficulty:", " ".join([f"{x:.2%}" for x in data_test_difficulty]))
    print(f"Random:", " ".join([f"{x:.2%}" for x in data_test_random]))

    print(f"Control: {np.average(data_test_control):.2f}")
    print(f"Difficulty: {np.average(data_test_difficulty):.2f}")
    print(f"Random: {np.average(data_test_random):.2f}")

    data_test_difficulty.pop(-1)
    data_test_random.pop(-2)
    print("Filtered")

    print(f"Control: {np.average(data_test_control):.2f}")
    print(f"Difficulty: {np.average(data_test_difficulty):.2f}")
    print(f"Random: {np.average(data_test_random):.2f}")
