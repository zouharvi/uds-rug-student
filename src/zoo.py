import torch
import torch.nn as nn

class Dense(nn.Module):
    def __init__(self, params):
        super().__init__()
        params = [tok.strip().split('-') for tok in params.split(',')]
        layers = []
        for param_i, param in enumerate(params):
            if param[0] == 'L':
                layers.append(
                    nn.Linear(int(param[1]), int(param[2]), bias=True)
                )
            if param[0] == 'D':
                layers.append(nn.Dropout(float(param[1])))
            if param_i != len(params):
                layers.append(nn.LeakyReLU())

        self.layers = nn.Sequential(*layers)
        self.train(False)

    def forward(self, x):
        return self.layers(x)

    def fit(self, dataTrain, dataValid, epochs):
        self.train(True)
        loss_fn = torch.nn.MSELoss()
        opt = torch.optim.Adam(self.parameters(), lr=0.0025)
        for epoch in range(epochs):
            self.train(True)

            pred = self(dataTrain[0]).reshape(-1)
            lossTrain = loss_fn(pred, dataTrain[1])
            lossTrain.backward()
            opt.step()
            opt.zero_grad()

            if epoch % 100 == 0:
                self.eval()
                pred = self(dataValid[0]).reshape(-1)
                lossValid = loss_fn(pred, dataValid[1])
                print(f'e{epoch:<9}:', end='')
                print(f'{math.sqrt(lossTrain.item()):>6.3f} | {math.sqrt(lossValid.item()):>6.3f}')
        self.train(False)
