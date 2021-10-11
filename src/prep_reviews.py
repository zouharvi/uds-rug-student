import csv

with open("../data/reviews_test.txt", "r") as f:
    lines = [(' '.join(x.split()[3:]), x.split()[0]) for x in f.readlines()]
with open("../data/reviews_test.csv", "w") as f:
    csv.writer(f, quoting=csv.QUOTE_ALL).writerows(lines)