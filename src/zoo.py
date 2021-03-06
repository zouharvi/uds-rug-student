import torch
import torch.nn as nn
from collections import Counter
from utils import DEVICE

FACTORY = {
    "mcc": lambda params: MostCommonClass(params["classes_map"]),
    "d0": lambda params: ModelDense([('L', params["embd_size"], params["classes_count"])]),
    "d1": lambda params: ModelDense([('L', params["embd_size"], 20), ('L', 20, params["classes_count"])]),
    "d2": lambda params: ModelDense([('L', params["embd_size"], 100), ('D', 0.2), ('L', 100, params["classes_count"])]),
    "c0": lambda params: ModelCNN([('C1', 1, 64, 4), ('M', 765), ('F', 1), ('L', 64, params["classes_count"])]),
    "c1": lambda params: ModelCNN([('C1', 1, 64, 4), ('C1', 64, 64, 4), ('C1', 64, 64, 4), ('M', 759), ('F', 1), ('L', 64, params["classes_count"])]),
}


class Evaluatable():
    def __init__(self, lr):
        self.lr = lr

    def evaluate(self, test):
        self.eval()
        matches = 0
        total = 0
        for x, y in test:
            x = x.to(DEVICE)
            y = y.to(DEVICE)
            matches += torch.sum(self(x).argmax(dim=1) == y)
            total += y.size()[0]
        return matches/total

    def fit(self, dataTrain, dataDev, epochs):
        print("epoch\tloss\tacc")
        print(f'   -1\tNaN\t{self.evaluate(dataDev)*100:>5.3f}%')

        loss_fn = torch.nn.CrossEntropyLoss()
        opt = torch.optim.Adam(self.parameters(), lr=self.lr)
        for epoch in range(epochs):
            self.train(True)

            for i, batch in enumerate(dataTrain):
                x, y = batch
                x = x.to(DEVICE)
                y = y.to(DEVICE)
                pred = self(x)
                lossTrain = loss_fn(pred, y)
                lossTrain.backward(retain_graph=True)
                opt.step()
                opt.zero_grad()

            print(
                f'{epoch:>5}',
                f'{lossTrain.to("cpu").item():>5.3f}',
                f'{self.evaluate(dataDev)*100:>5.2f}%',
                sep="\t"
            )


class MostCommonClass():
    def __init__(self, classes_map):
        self.most_common = None
        self.classes_map = classes_map

    def fit(self, dataTrain, dataDev, epochs):
        ys = Counter()
        for _x, y in dataTrain:
            ys.update(y.tolist())
        self.most_common = ys.most_common(1)[0][0]
        print(
            'Most common:',
            self.most_common,
            f'({self.classes_map[self.most_common]})'
        )

        print('Acc', f'{self.evaluate(dataDev)*100:.2f}')

    def evaluate(self, test):
        matches = 0
        total = 0
        for x, y in test:
            matches += torch.sum(self.most_common == y)
            total += y.size()[0]
        return matches/total


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

        self.layers = nn.Sequential(*layers)
        self.train(False)
        self.to(DEVICE)

    def forward(self, x):
        return self.layers(x)


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

        self.layers = nn.Sequential(*layers)
        self.train(False)
        self.to(DEVICE)

    def forward(self, x):
        return self.layers(x.reshape((x.size()[0], 1, -1)))
