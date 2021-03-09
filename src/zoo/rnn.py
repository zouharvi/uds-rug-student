import torch
import torch.nn as nn
import numpy as np
from utils import DEVICE
from zoo.evaluatable import Fittable

class ModelRNN(Fittable):
    def __init__(self, type, bidirectional, num_layers, embd_size, classes_count, hidden_dim=None):
        super().__init__(0.001)
        if hidden_dim == None:
            hidden_dim = classes_count+1
        if type == "rnn":
            self.unit = nn.RNN(
                input_size=embd_size,
                hidden_size=hidden_dim,
                num_layers=num_layers,
                bidirectional=bidirectional
            )
        elif type == "lstm":
            self.unit = nn.LSTM(
                input_size=embd_size,
                hidden_size=hidden_dim,
                num_layers=num_layers,
                bidirectional=bidirectional
            )
        elif type == "gru":
            self.unit = nn.GRU(
                input_size=embd_size,
                hidden_size=hidden_dim,
                num_layers=num_layers,
                bidirectional=bidirectional
            )
        if bidirectional:
            self.linear = nn.Linear(2*hidden_dim, classes_count)
        else:
            self.linear = nn.Linear(hidden_dim, classes_count)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        lstm_out, _ = self.unit(x.view(len(x), 1, -1))
        tag_space = self.linear(lstm_out.view(len(x), -1))
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

        for x, y in data:
            x = torch.stack(x, dim=0).float().to(DEVICE)
            y = torch.LongTensor(y).to(DEVICE)
            pred = self(x)
            lossTrain = self.loss_fn(pred, y)
            losses.append(lossTrain.detach().cpu())
            lossTrain.backward(retain_graph=True)
            self.opt.step()
            self.opt.zero_grad()
        return np.average(losses)