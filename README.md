# UdS NNIA Project 2021

This repository is mandatory for the UdS NNIA class of 2020/2021. It will be deleted later.

## Table of Contents

- [General](#General): information about this project
- [Pipeline](#Pipeline): technical information for set up
- - [Data Preprocessing](##Data-Preprocessing) POS extraction, aggregation

## General

General information is TODO.

# Pipeline

This project is written in Python, with the environment defined in `envirovnment.yml` (managed by Anaconda). We further assume, that all data are stored in `data/`.

## Data Preprocessing

First, concatenate all files into one, e.g. by `cat data/*.gold_conll > data/sample.conll`.

Extract the tripet (word position, word, POS) using the following snippet. Alternatively, run `src/data/extract_pos.sh INPUT_CONLL OUTPUT_TSV` (same code).

```
grep -vE "^#.*$" data/sample.conll | awk '/^$/ {print "*"} NF {print $3"\t"$4"\t"$5}' > data/sample.tsv
```


For overview of the POS data (in .tsv), run `src/data/info.py data/sample.tsv > data/sample.info`:

```
Max sequence length:      73
Min sequence length:       2
Mean sequence length:  18.75
Number of sequences:     309

Tags:
NN       12.93%
IN        9.94%
DT        9.68%
PRP       7.01%
,         6.44%
RB        5.56%
.         5.23%
VBD       5.20%
...
```