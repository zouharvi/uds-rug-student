import torch
import torch.nn as nn

class Evaluatable():
    def evaluate(self, test):
        self.eval()
        matches = 0
        for x, y in test:
            matches += 1*(int(self(x).argmax())==y)
        return matches/len(test)

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

    def forward(self, x):
        return self.layers(x)

    def fit(self, dataTrain, dataDev, epochs):
        print(f'    x  acc {self.evaluate(dataDev)*100:>6.3f}%')

        loss_fn = torch.nn.CrossEntropyLoss()
        opt = torch.optim.Adam(self.parameters(), lr=0.1)
        for epoch in range(epochs):
            self.train(True)

            for batch in dataTrain:
                x, y = batch
                pred = self(x)

                lossTrain = loss_fn(pred, y)
                lossTrain.backward(retain_graph=True)
                opt.step()
                opt.zero_grad()

            print(f'{epoch:>5} loss {lossTrain.item():>6.3f}')
            print(f'{epoch:>5}  acc {self.evaluate(dataDev)*100:>6.3f}%')
        self.train(False)
