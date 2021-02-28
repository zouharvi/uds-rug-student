import datasets
from transformers import AutoTokenizer, BertModel
import torch
import pickle

with open("data/embedding_test.pkl", "rb") as f:
    data_embd = pickle.load(f)

input()