import torch.nn as nn
from utils import DEVICE
from zoo.evaluatable import Evaluatable

class ModelDense(Evaluatable):
    def __init__(self, dense_model, dropout, embd_size, classes_count):
        super().__init__(lr=0.005)

        assert(dropout in {0, 0.1})

        if dense_model == 1:
            self.layers = nn.Sequential(
                nn.Linear(embd_size, classes_count)
            )
        elif dense_model == 2:
            self.layers = nn.Sequential(
                nn.Linear(embd_size, 64),
                nn.LeakyReLU(),
                nn.Dropout(dropout),
                nn.Linear(64, classes_count),
            )
        elif dense_model == 3:
            self.layers = nn.Sequential(
                nn.Linear(embd_size, 64),
                nn.LeakyReLU(),
                nn.Dropout(dropout),
                nn.Linear(64, 64),
                nn.LeakyReLU(),
                nn.Dropout(dropout),
                nn.Linear(64, classes_count),
            )
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        return self.softmax(self.layers(x))