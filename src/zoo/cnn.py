import torch
import torch.nn as nn
from utils import DEVICE
from zoo.evaluatable import Evaluatable

class ModelCNN(nn.Module, Evaluatable):
    def __init__(self, params):
        nn.Module.__init__(self)
        Evaluatable.__init__(self, lr=0.01)

        layers = []
        for param_i, param in enumerate(params):
            if param[0] == 'C1':
                layers.append(nn.Conv1d(param[1], param[2], param[3]))
            elif param[0] == 'M':
                layers.append(torch.nn.MaxPool1d(param[1]))
            elif param[0] == 'F':
                layers.append(torch.nn.Flatten(start_dim=param[1]))
            elif param[0] == 'L':
                layers.append(
                    nn.Linear(param[1], param[2], bias=True)
                )

        self.f = nn.Softmax(dim=1)
        self.layers = nn.Sequential(*layers)
        self.to(DEVICE)

    def forward(self, x):
        return self.f(self.layers(x.reshape((x.size()[0], 1, -1))))
