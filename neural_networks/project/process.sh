#!/bin/bash

cat data/{chtb_0223,phoenix_0001,pri_0016,wsj_1681}.gold_conll > data/sample.conll
grep -v -E "^#.*$" data/sample.conll | awk '/^$/ {print "*"} NF {print $3"\t"$4"\t"$5}' > data/sample.tsv