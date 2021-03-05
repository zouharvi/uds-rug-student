import torch
import torch.nn as nn
from utils import DEVICE

FACTORY = {
    "d0": lambda embd, classes: ModelDense([('L', embd, classes)]), 
    "d1": lambda embd, classes: ModelDense([('L', embd, 20), ('L', 20, classes)]),
    "d2": lambda embd, classes: ModelDense([('L', embd, 100), ('D', 0.2), ('L', 100, classes)]),
    "c0": lambda embd, classes: ModelCNN([('C1', 1, 64, 4), ('C1', 64, 64, 4), ('C1', 64, 64, 4), ('M', 759), ('F', 1), ('L', 64, classes)]), 
}

class Evaluatable():
    def evaluate(self, test):
        self.eval()
        matches = 0
        total = 0
        for x, y in test:
            x = x.to(DEVICE)
            y = y.to(DEVICE)
            matches += torch.sum(self(x).argmax(dim=1)==y)
            total += y.size()[0]
        return matches/total

    def fit(self, dataTrain, dataDev, epochs):
        print("epoch\tloss\tacc")
        # print(f'   -1\tNaN\t{self.evaluate(dataDev)*100:>5.3f}%')

        loss_fn = torch.nn.CrossEntropyLoss()
        opt = torch.optim.Adam(self.parameters(), lr=0.01)
        for epoch in range(epochs):
            self.train(True)

            for i,batch in enumerate(dataTrain):
                x, y = batch
                x = x.to(DEVICE)
                y = y.to(DEVICE)
                pred = self(x)
                lossTrain = loss_fn(pred, y)
                lossTrain.backward(retain_graph=True)
                opt.step()
                opt.zero_grad()

            print(f'{epoch:>5}\t{lossTrain.to("cpu").item():>5.3f}\t{self.evaluate(dataDev)*100:>5.2f}%')

class ModelDense(nn.Module, Evaluatable):
    def __init__(self, params):
        super().__init__()
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

        self.layers = nn.Sequential(*layers)
        self.train(False)
        self.to(DEVICE)

    def forward(self, x):
        return self.layers(x)

class ModelCNN(nn.Module, Evaluatable):
    def __init__(self, params):
        super().__init__()

        layers = []
        for param_i, param in enumerate(params):
            if param[0] == 'C1':
                layers.append(nn.Conv1d(param[1], param[2], param[3]))
            elif param[0] == 'M':
                # 756
                layers.append(torch.nn.MaxPool1d(param[1]))
            elif param[0] == 'F':
                layers.append(torch.nn.Flatten(start_dim=param[1]))
            elif param[0] == 'L':
                layers.append(
                    nn.Linear(param[1], param[2], bias=True)
                )

        self.layers = nn.Sequential(*layers)
        self.train(False)
        self.to(DEVICE)

    def forward(self, x):
        return self.layers(x.reshape((x.size()[0], 1,-1)))

