import torch
import torch.nn as nn
from utils import DEVICE
from zoo.evaluatable import Evaluatable

class ModelCNN(Evaluatable):
    def __init__(self, params):
        super().__init__(lr=0.0005)

        layers = []
        for param_i, param in enumerate(params):
            if param[0] == 'C1':
                layers.append(nn.Conv1d(param[1], param[2], param[3]))
            elif param[0] == 'M':
                layers.append(nn.MaxPool1d(param[1]))
            elif param[0] == 'F':
                layers.append(nn.Flatten(start_dim=param[1]))
            elif param[0] == 'L':
                layers.append(
                    nn.Linear(param[1], param[2], bias=True)
                )

        self.softmax = nn.Softmax(dim=1)
        self.layers = nn.Sequential(*layers)

    def forward(self, x):
        y = self.layers(x.reshape((x.shape[0], 1, -1)))
        return self.softmax(y)
