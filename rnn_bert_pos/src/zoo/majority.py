from collections import Counter
import torch
import wandb

class MajorityClassifier():
    def __init__(self, classes_map):
        self.most_common = None
        self.classes_map = classes_map

    def fit(self, dataTrain, dataDev, epochs, save_path):
        ys = Counter()
        for _x, y in dataTrain:
            ys.update(y.tolist())
        self.most_common = ys.most_common(1)[0][0]
        print(
            'Most common:',
            self.most_common,
            f'({self.classes_map[self.most_common]})'
        )
        log_obj = {"acc_dev": self.evaluate(dataDev), "acc_train": self.evaluate(dataTrain)}
        wandb.log(log_obj)
            
        print('Acc', f'{log_obj["acc_dev"]*100:.2f}')

    def evaluate(self, test):
        matches = 0
        total = 0
        for x, y in test:
            matches += torch.sum(self.most_common == y)
            total += y.size()[0]
        return matches/total

