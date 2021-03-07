# UdS NNIA Project 2021

## Table of Contents

- [General](#General): information about this project
- [Pipeline](#Pipeline): technical information for set up
- - [Data Preprocessing](##Data-Preprocessing): POS extraction, aggregation
- - [Tokenization & Embedding](##Tokenization-&-Embedding): embedding creation
- - [Models](##Models): training

## General

This repository is mandatory for the UdS NNIA class of 2020/2021. This project is centered around POS prediction using BERT embeddings and variety of different models.

# Pipeline

This project is written in Python, with the environment defined in `envirovnment.yml` (managed by Anaconda). We further assume, that all data are stored in `data/`.

## Data Preprocessing

- Concatenate all files into one, e.g. by `cat data/ontonetes-4.0/*.gold_conll > data/all.conll`
- Extract the tripet (word position, word, POS) using `src/data/extract_pos.sh data/all.conll data/all.tsv`
- For overview of the POS data (in .tsv), run `./src/data/info.py data/all.tsv > data/all.info`:

```
Tags:                   Overall:
NN       12.93%         Max sequence length:      73
IN        9.94%         Min sequence length:       2
DT        9.68%         Mean sequence length:  18.75
PRP       7.01%         Number of sequences:     309
,         6.44%
RB        5.56%
.         5.23%
VBD       5.20%
...
```

## Tokenization & Embedding

<!-- TODO: this is incorrect -->
This part tokenizes the words (in a sense of subword units + BERT specific indexing) with BERT Tokenizer. The input is then fed into BERT and the hidden states in the last layer are used as embeddings. Run `python3 src/embedding.py train INPUT_TSV OUTPUT_PKL` to compute the embeddings and store them. Caution, this is a highly memory sensitive task, requiring for save usage ~15GB of free memory (CPU and GPU in total). There is a mechanism that starts swapping sentences to CPU RAM when GPU is about to be full. To disable this, add `--no-hotswap`.

## Models

TODO
