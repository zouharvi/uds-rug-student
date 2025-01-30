#!/usr/bin/env python3
from data.ontonotes import OntoNotesEmbd
import torch
import argparse
from zoo import factory


parser = argparse.ArgumentParser()
parser.add_argument('model', help='Path to the model to use')
parser.add_argument('--data', default="data/embedding_",
                    help='Prefix of path to embedding_{train,dev,test}.pkl')
parser.add_argument('--batch', type=int, default=4096,
                    help='Batch size to use')
args = parser.parse_args()

model = torch.load(args.model)

keep_sent = any(x in args.model for x in {"lstm", "gru", "rnn"})
data_test, classes_map, classes_count = OntoNotesEmbd(args.data).get("test", keep_sent=keep_sent)
if keep_sent:
    embd_size = data_test[0][0][0].size()[0]
else:
    embd_size = data_test[0][0].size()[0]
    data_test = torch.utils.data.DataLoader(data_test, batch_size=args.batch)
print("Embeddings size", embd_size)
print("Classes count", classes_count)

test_acc = model.evaluate(data_test)
print(f"Test acc: {test_acc*100:.2f}%")