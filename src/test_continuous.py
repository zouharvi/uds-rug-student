#!/usr/bin/env python3
from data.ontonotes import OntoNotesEmbd
import torch
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--data', default="data/embedding_",
                    help='Prefix of path to embedding_{train,dev,test}.pkl')
parser.add_argument('--batch', type=int, default=4096,
                    help='Batch size to use')
parser.add_argument('--no-keep-sent', action="store_true",
                    help='Flatten test data')
args = parser.parse_args()

data_test, classes_map, classes_count = OntoNotesEmbd(args.data).get("test", keep_sent=not args.no_keep_sent)
if not args.no_keep_sent:
    embd_size = data_test[0][0][0].size()[0]
else:
    embd_size = data_test[0][0].size()[0]
    data_test = torch.utils.data.DataLoader(data_test, batch_size=args.batch)
print("Embeddings size", embd_size)
print("Classes count", classes_count)

while True:
    try:
        model_path = input("Model path, including epoch and extension: ")
        model = torch.load(model_path)
        test_acc = model.evaluate(data_test)
        print(f"Test acc: {test_acc*100:.2f}%")
    except Exception:
        continue
