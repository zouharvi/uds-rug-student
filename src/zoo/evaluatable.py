import torch
import torch.nn as nn
from utils import DEVICE
import numpy as np
import wandb

class Fittable():
    def __init__(self, lr):
        self.lr = lr
        wandb.config.learning_rate = lr
        self.loss_fn = nn.CrossEntropyLoss()

    def fit(self, dataTrain, dataDev, epochs, save_path):
        print("epoch\tloss\tacc")
        log_obj = {"epoch": -1, "loss_train": np.nan, "acc_dev": self.evaluate(dataDev)}
        wandb.log(log_obj)
        print(
            f'{log_obj["epoch"]:>5}',
            f'{log_obj["loss_train"]:>5.3f}',
            f'{log_obj["acc_dev"]*100:>5.2f}%',
            sep="\t"
        )
        self.opt = torch.optim.Adam(self.parameters(), lr=self.lr)

        wandb.watch(self)
        for epoch in range(epochs):
            epoch += 1
            lossTrain = self.train_epoch(dataTrain)
            log_obj = {"epoch": epoch, "loss_train": lossTrain, "acc_dev": self.evaluate(dataDev)}
            torch.save(self.state_dict(), f"{save_path}/{self.name}/e{epoch:0>3}.pt")
            wandb.log(log_obj)
            print(
                f'{log_obj["epoch"]:>5}',
                f'{log_obj["loss_train"]:>5.3f}',
                f'{log_obj["acc_dev"]*100:>5.2f}%',
                sep="\t"
            )

class Evaluatable(Fittable):
    def train_epoch(self, data):
        self.train(True)
        losses = []
        for x, y in data:
            x = x.float().to(DEVICE)
            y = y.to(DEVICE)
            pred = self(x)
            lossTrain = self.loss_fn(pred, y)
            losses.append(lossTrain.detach().cpu())
            lossTrain.backward(retain_graph=True)
            self.opt.step()
            self.opt.zero_grad()
        return np.average(losses)

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