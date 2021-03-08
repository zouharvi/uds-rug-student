import torch
import torch.nn as nn
from utils import DEVICE

class Evaluatable():
    def __init__(self, lr):
        self.lr = lr

    def evaluate(self, test):
        self.eval()
        matches = 0
        total = 0
        for x, y in test:
            x = x.float().to(DEVICE)
            y = y.to(DEVICE)
            matches += torch.sum(self(x).argmax(dim=1) == y)
            total += y.size()[0]
        return matches/total

    def fit(self, dataTrain, dataDev, epochs):
        print("epoch\tloss\tacc")
        print(f'   -1\tNaN\t{self.evaluate(dataDev)*100:>5.3f}%')

        loss_fn = nn.CrossEntropyLoss()
        opt = torch.optim.Adam(self.parameters(), lr=self.lr)
        for epoch in range(epochs):
            epoch += 1
            self.train(True)

            for x, y in dataTrain:
                x = x.float().to(DEVICE)
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