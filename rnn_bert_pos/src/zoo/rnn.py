import torch
import torch.nn as nn
import numpy as np
from utils import DEVICE
from zoo.evaluatable import Fittable

class ModelRNN(Fittable):
    def __init__(self, unit, bidirectional, num_layers, embd_size, classes_count, hidden_dim, dropout, dense_model, batch):
        self.batch = batch
        super().__init__(0.0005)
        if unit == "rnn+relu":
            self.unit = nn.RNN(
                input_size=embd_size,
                hidden_size=hidden_dim,
                num_layers=num_layers,
                bidirectional=bidirectional,
                nonlinearity="relu",
                dropout=dropout,
            )
        elif unit == "rnn+tanh":
            self.unit = nn.RNN(
                input_size=embd_size,
                hidden_size=hidden_dim,
                num_layers=num_layers,
                bidirectional=bidirectional,
                nonlinearity="tanh",
                dropout=dropout,
            )
        elif unit == "lstm":
            self.unit = nn.LSTM(
                input_size=embd_size,
                hidden_size=hidden_dim,
                num_layers=num_layers,
                bidirectional=bidirectional,
                dropout=dropout,
            )
        elif unit == "gru":
            self.unit = nn.GRU(
                input_size=embd_size,
                hidden_size=hidden_dim,
                num_layers=num_layers,
                bidirectional=bidirectional,
                dropout=dropout,
            )
        if bidirectional:
            start_size = 2*hidden_dim
        else:
            start_size = hidden_dim

        if dense_model == 1:
            self.linear_layers = nn.Sequential(
                nn.Linear(start_size, classes_count)
            )
        elif dense_model == 2:
            self.linear_layers = nn.Sequential(
                nn.Linear(start_size, 128),
                nn.Tanh(),
                nn.Linear(128, classes_count)
            )
        elif dense_model == 3:
            self.linear_layers = nn.Sequential(
                nn.Linear(start_size, 256),
                nn.Tanh(),
                nn.Linear(256, 256),
                nn.Tanh(),
                nn.Linear(256, classes_count)
            )
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        lstm_out, _ = self.unit(x.view(len(x), 1, -1))
        tag_space = self.linear_layers(lstm_out.view(len(x), -1))
        tag_scores = self.softmax(tag_space)
        return tag_scores

    def evaluate(self, test):
        self.eval()
        matches = 0
        total = 0
        for x, y in test:
            x = torch.stack(x, dim=0).float().to(DEVICE)
            y = torch.ShortTensor(y).to(DEVICE)
            yhat = self(x).argmax(dim=1)
            matches += torch.sum(torch.eq(yhat, y))
            total += y.shape[0]
        return matches/total
    
    def train_epoch(self, data):
        self.train(True)
        losses = []

        for iteration, (x, y) in enumerate(data):
            x = torch.stack(x, dim=0).float().to(DEVICE)
            y = torch.LongTensor(y).to(DEVICE)
            pred = self(x)
            lossTrain = self.loss_fn(pred, y)
            losses.append(lossTrain.detach().cpu())
            lossTrain.backward(retain_graph=True)
            if iteration % self.batch == 0 or iteration == len(data)-1:
                self.opt.step()
                self.opt.zero_grad()
        return np.average(losses)