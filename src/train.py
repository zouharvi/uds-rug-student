#!/usr/bin/env python3
from data.ontonotes import OntoNotesEmbd
import torch
import argparse
import wandb
from zoo import factory


parser = argparse.ArgumentParser()
parser.add_argument('model', help='Model to use (majority, dense, rnn+tanh, rnn+relu, lstm, gru)')
parser.add_argument('--epochs', type=int, default=50,
                    help='Number of epochs to use')
parser.add_argument('--batch', type=int, default=768,
                    help='Batch size to use')
parser.add_argument('--data', default="data/embedding_",
                    help='Prefix of path to embedding_{train,dev,test}.pkl')
parser.add_argument('--save-path', default="data/models",
                    help='Directory to which store models')
parser.add_argument('--train-size', type=int, default=None,
                    help='Number of training examples to use')
parser.add_argument('--dev-size', type=int, default=None,
                    help='Number of dev examples to use')
parser.add_argument('--seed', type=int, default=0,
                    help='Seed to use for shuffling')
# Model parameters 
parser.add_argument('--dropout', type=float, default=0,
                    help='Dropout probability')
# Dense model parameters
parser.add_argument('--dense-model', type=int, default=1,
                    help='Dense model (1, 2, 3)')
# RNN model parameters
parser.add_argument('--rnn-hidden-size', type=int, default=128,
                    help='RNN hidden state size')
parser.add_argument('--rnn-layers', type=int, default=1,
                    help='RNN stacked recurrent layers')
parser.add_argument('--rnn-bidir', action="store_true",
                    help='RNN bidirectional')
parser.add_argument('--rnn-dense-model', type=int, default=1,
                    help='RNN dense model (1,2,3)')
args = parser.parse_args()

torch.manual_seed(args.seed)
run = wandb.init(project='bert-pos')
wandb.config.update(args)

keep_sent = any(args.model.startswith(x) for x in {"lstm", "gru", "rnn", "cnnsent"})

data_dev, _, _ = OntoNotesEmbd(args.data).get("dev", args.dev_size, keep_sent)
data_train, classes_map, classes_count = OntoNotesEmbd(args.data).get("train", args.train_size, keep_sent)
if keep_sent:
    embd_size = data_train[0][0][0].size()[0]
else:
    embd_size = data_train[0][0].size()[0]
    data_train = torch.utils.data.DataLoader(data_train, batch_size=args.batch)
    data_dev = torch.utils.data.DataLoader(data_dev, batch_size=args.batch)

print("Embeddings size", embd_size)
print("Classes count", classes_count)


params = {"embd_size": embd_size, "classes_count": classes_count, "classes_map": classes_map}
model = factory(args.model, run.name, params, args)
model.fit(data_train, data_dev, args.epochs, args.save_path)
