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
    data_main, data_test = utils.load_all(args.data)

    
    print("Test line keys:", list(data_test[0].keys()))
    print("Main line keys:", list(data_main[0].keys()))
    print()

    print("Test")
    data_test_control = np.average([l["correct"] for l in data_test if l["group"] == "control"]) 
    data_test_difficulty = np.average([l["correct"] for l in data_test if l["group"] == "difficulty"]) 
    data_test_random = np.average([l["correct"] for l in data_test if l["group"] == "random"]) 
    print(f"Control:    {data_test_control:.2%}")
    print(f"Difficulty: {data_test_difficulty:.2%}")
    print(f"Random:     {data_test_random:.2%}")

    print("Main:")
    data_test_control = np.average([l["correct"] for l in data_main if l["group"] == "control"]) 
    data_test_difficulty = np.average([l["correct"] for l in data_main if l["group"] == "difficulty"]) 
    data_test_random = np.average([l["correct"] for l in data_main if l["group"] == "random"]) 
    print(f"Control:    {data_test_control:.2%}")
    print(f"Difficulty: {data_test_difficulty:.2%}")
    print(f"Random:     {data_test_random:.2%}")

    print("Test PT0")
    data_test_control = np.average([l["correct"] for l in data_test if l["group"] == "control" and l["pt"] == 0]) 
    data_test_difficulty = np.average([l["correct"] for l in data_test if l["group"] == "difficulty" and l["pt"] == 0]) 
    data_test_random = np.average([l["correct"] for l in data_test if l["group"] == "random" and l["pt"] == 0]) 
    print(f"Control:    {data_test_control:.2%}")
    print(f"Difficulty: {data_test_difficulty:.2%}")
    print(f"Random:     {data_test_random:.2%}")
    print("Test PT1")
    data_test_control = np.average([l["correct"] for l in data_test if l["group"] == "control" and l["pt"] == 1]) 
    data_test_difficulty = np.average([l["correct"] for l in data_test if l["group"] == "difficulty" and l["pt"] == 1]) 
    data_test_random = np.average([l["correct"] for l in data_test if l["group"] == "random" and l["pt"] == 1]) 
    print(f"Control:    {data_test_control:.2%}")
    print(f"Difficulty: {data_test_difficulty:.2%}")
    print(f"Random:     {data_test_random:.2%}")
    
    data_test_pt0 = np.average([l["correct"] for l in data_test if l["pt"] == 0]) 
    data_test_pt1 = np.average([l["correct"] for l in data_test if l["pt"] == 1]) 
    print(f"PT0:    {data_test_pt0:.2%}")
    print(f"PT1:    {data_test_pt1:.2%}")
    
    data_test_control = np.average([l["rt"] for l in data_test if l["group"] == "control" and l["rt"] != float("inf")]) 
    data_test_difficulty = np.average([l["rt"] for l in data_test if l["group"] == "difficulty" and l["rt"] != float("inf")]) 
    data_test_random = np.average([l["rt"] for l in data_test if l["group"] == "random" and l["rt"] != float("inf")]) 

    data_main_control = np.average([l["rt"] for l in data_main if l["group"] == "control" and l["rt"] != float("inf")]) 
    data_main_difficulty = np.average([l["rt"] for l in data_main if l["group"] == "difficulty" and l["rt"] != float("inf")]) 
    data_main_random = np.average([l["rt"] for l in data_main if l["group"] == "random" and l["rt"] != float("inf")]) 
    print(f"RT Control:    {data_test_control/1000:.2}s (test), {data_main_control/1000:.2}s (main)")
    print(f"RT Difficulty: {data_test_difficulty/1000:.2}s (test), {data_main_difficulty/1000:.2}s (main)")
    print(f"RT Random:     {data_test_random/1000:.2}s (test), {data_main_random/1000:.2}s (main)")
    
