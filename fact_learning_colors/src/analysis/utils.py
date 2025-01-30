import os
import re
import csv
import collections

def load_all(root_dir, flatten=True):
    """
    root_dir: Path to the directory containing all results files
    if flatten:
        output: tuple of (main, test) data (dictionary mapping subject ids to )
    else:
        output: tuple of dictionaries mapping uids to lists of dicts as above
    """

    files = os.listdir(root_dir)

    def parse_file_name(regex):
        return {
            int(re.match(regex, f).groups()[0]): root_dir + f
            for f in files if re.match(regex, f)
        }

    # parse file names
    files_main = parse_file_name(r"subject-(\d+)\.csv")
    files_test = parse_file_name(r"subject-(\d+)Test\.csv")

    def parse_raw(filenames):
        return {
            k: [
                l.strip()
                for l in open(f, "r").readlines() if len(l.strip()) > 0
            ]
            for k, f in filenames.items()
        }

    # load and parse raw files
    files_main = parse_raw(files_main)
    files_test = parse_raw(files_test)

    def parse_color_main(color):
        # TODO:
        return color

    def parse_line_main_typed(line):
        return {
            **line,
            "trial": int(line["trial"]),
            "start_time": float(line["start_time"]),
            "rt": float(line["rt"]),
            "correct": line["correct"] == "True",
            "alpha": float(line["alpha"]),
            "priora": float(line["priora"]),
            "fact_id": int(line["fact_id"]),
            "color": parse_color_main(line["color"])
        }

    # parse learning data
    for filename, data in files_main.items():
        # heuristics to determine the group
        if "colour" in data[0]:
            group = "random"
            palette = None
        elif data[0].count(",") == 8:
            group = "control"
            palette = None
        elif len(data[0]) <= 20:
            group = "difficulty"
            palette = data.pop(0)
        else:
            raise Exception("Head parsing failed with", filename)

        data = list(csv.DictReader(data))
        if group == "difficulty":
            data = [
                parse_line_main_typed({
                    **line, "color": line["bgcol"], "group": group, "palette": palette
                })
                for line in data
            ]
            [line.pop("bgcol") for line in data]
        elif group == "random":
            data = [
                parse_line_main_typed({
                    **line, "color": line["colour"], "group": group, "palette": palette
                })
                for line in data
            ]
            [line.pop("colour") for line in data]
        elif group == "control":
            data = [
                parse_line_main_typed({
                    **line, "color": None, "group": group, "palette": palette
                })
                for line in data
            ]

        # possibly dangerous to mutate currently iterated container
        files_main[filename] = data

    def parse_color_test(color):
        # TODO:
        if color == "NA":
            return None
        else:
            return color

    def parse_line_test_typed(line, pt_subtract=0):
        return {
            **line,
            "id": int(line["id"]),
            "start_time": float(line["start_time"]),
            "rt": float(line["rt"]),
            "correct": line["correct"] == "True",
            "alpha": float(line["alpha"]),
            "pt": int(line["pt"]) - pt_subtract,
            "priora": float(line["priora"]),
            "fact_id": int(line["fact_id"]),
            "color": parse_color_test(line["color"])
        }
    # parse test data
    for filename, data in files_test.items():
        # hack to get around missing column in subject-3Test.csv
        # extract group from the matching learning data
        group = files_main[filename][0]["group"]
        if group == "control":
            data[0] = data[0].replace("fact_id,question,answer", "question,answer,fact_id")
        data = list(csv.DictReader(data))

        if group == "difficulty":
            data = [
                parse_line_test_typed({
                    **line, "color": line["bgcol"], "group": group, "palette": palette
                })
                for line in data
            ]
            [line.pop("bgcol") for line in data]
        elif group == "random":
            data = [
                parse_line_test_typed({
                    **line, "color": line["colour"], "group": group, "palette": palette
                })
                for line in data
            ]
            [line.pop("colour") for line in data]
        elif group == "control":
            data = [
                parse_line_test_typed({
                    **line, "color": None, "group": group, "palette": palette
                }, pt_subtract=1)
                for line in data
            ]

        # possibly dangerous to mutate currently iterated container
        files_test[filename] = data

    print(
        "Distribution",
        dict(collections.Counter([v[0]["group"] for x,v in files_test.items()]))
    )

    def flatten_dicts(data):
        # trick to flatten an array in one comprehension
        return [
            {**line, "uid": uid}
            for uid, subdata in data.items()
            for line in subdata
        ]

    # flatten files if desired
    if flatten:
        files_main = flatten_dicts(files_main)
        files_test = flatten_dicts(files_test)
    else:
        # we dont care what ordering this is as long as its stable
        sorted_users = sorted(files_main.keys())
        files_main = {k:files_main[k] for k in sorted_users}
        files_test = {k:files_test[k] for k in sorted_users}

    return files_main, files_test
