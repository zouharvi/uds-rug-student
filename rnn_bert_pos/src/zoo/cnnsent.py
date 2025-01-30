import torch
import torch.nn as nn
from utils import DEVICE
from zoo.evaluatable import Fittable
import numpy as np

class ModelCNNSent(Fittable):
    def __init__(self, embd_size, classes_count):
        super().__init__(lr=0.001)
        self.classes_count = classes_count

        cnn_kernel = (512, 5)
        self.conv = nn.Conv2d(1, 128, kernel_size=cnn_kernel, padding=(0, 2))
        self.mpl = nn.MaxPool2d((embd_size-cnn_kernel[0]+1, 1))
        self.conv_lin = nn.Conv2d(128, classes_count, kernel_size=1)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        y = self.conv(x.reshape((1, 1, x.shape[1], x.shape[0])))
        y = self.mpl(y)
        y = self.conv_lin(y)
        y = y.reshape((self.classes_count, x.shape[0]))
        y = self.softmax(y)
        return y.transpose(0, 1)

    def evaluate(self, test):
        self.eval()
        matches = 0
        total = 0
        for x, y in test:
            x = torch.stack(x, dim=0).float().to(DEVICE)
            y = torch.ShortTensor(y).to(DEVICE)
            # print("target shape", y.shape)
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