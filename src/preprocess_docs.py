#!/usr/bin/env python3

import argparse
import csv
import re


def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument("-i", "--data-in", default="data/wj_annotated.txt")
    args.add_argument("-o", "--data-out", default="data/wj.csv")
    args.add_argument("-u", "--user", default="wj")
    return args.parse_args()


def line_filter(line):
    if "transcript" in line and len(line) == 11:
        return True
    elif re.match("\d\d:\d\d:\d\d", line):
        return True
    elif line.startswith("Jikke Overdiep: "):
        return True
    elif len(line) == 0:
        return True
    elif re.match("^\[[a-z]{1,4}\]", line):
        # remove annotations
        return True
    return False


def line_modifier(line):
    line = re.sub("^[\w]+ [\w]+: ", "", line)
    # remove annotation signatures
    line = re.sub("\[[a-z]{1,4}\]", "", line)
    return line


def line_has_annotations(line):
    # make sure it does not start
    if re.match(".+\[[a-z]{1,4}\]", line):
        return True
    else:
        return False


def line_annotation(line):
    return re.search(r"\[([a-z]{1,4})\]", line).group(1)


if __name__ == "__main__":
    args = parse_args()
    with open(args.data_in, "r") as f:
        data = [x.strip() for x in f.readlines()]

    annotations = [re.search(r"^\[([a-z]{1,4})\](.*)", x)
                   for x in data if re.match("^\[[a-z]{1,4}\]", x)]
    annotations = {x.group(1): x.group(2) for x in annotations}
    # print(annotations)
    # print(data[:10])

    # print([x for x in data if line_has_annotations(x)])

    data = [
        [
            (
                sent,
                annotations[line_annotation(x)] if line_has_annotations(x) else ""
            )
            for sent in line_modifier(x).split(". ")
            if sent != ""
        ]
        for x in data if not line_filter(x)
    ]

    data = [x for y in data for x in y]

    with open(args.data_out, "w") as f:
        csv.writer(f, quoting=csv.QUOTE_ALL).writerows(
            [
                (args.user, x[0], x[1])
                for x in data
            ]
        )
