import torch.nn as nn
from utils import DEVICE
from zoo.evaluatable import Evaluatable

class ModelDense(nn.Module, Evaluatable):
    def __init__(self, params):
        nn.Module.__init__(self)
        Evaluatable.__init__(self, lr=0.01)

        layers = []
        for param_i, param in enumerate(params):
            if param[0] == 'L':
                layers.append(
                    nn.Linear(param[1], param[2], bias=True)
                )
            if param[0] == 'D':
                layers.append(nn.Dropout(param[1]))
            if param_i != len(params):
                layers.append(nn.LeakyReLU())

        self.softmax = nn.Softmax(dim=1)
        self.layers = nn.Sequential(*layers)

    def forward(self, x):
        return self.softmax(self.layers(x))