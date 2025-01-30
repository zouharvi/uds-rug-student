import torch.nn as nn
from utils import DEVICE
from zoo.evaluatable import Evaluatable

class ModelDense(Evaluatable):
    def __init__(self, dense_model, dropout, embd_size, classes_count):
        super().__init__(lr=0.001)

        assert(dropout in {0, 0.1})

        if dense_model == 1:
            self.layers = nn.Sequential(
                nn.Linear(embd_size, classes_count)
            )
        elif dense_model == 2:
            self.layers = nn.Sequential(
                nn.Linear(embd_size, 128),
                nn.Tanh(),
                nn.Dropout(dropout),
                nn.Linear(128, classes_count),
            )
        elif dense_model == 3:
            self.layers = nn.Sequential(
                nn.Linear(embd_size, 256),
                nn.Tanh(),
                nn.Dropout(dropout),
                nn.Linear(256, 256),
                nn.Tanh(),
                nn.Dropout(dropout),
                nn.Linear(256, classes_count),
            )
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        return self.softmax(self.layers(x))
