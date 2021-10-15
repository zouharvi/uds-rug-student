import numpy as np
import torch
import random

from misc.utils import DEVICE, binarize_labels
from sklearn.dummy import DummyClassifier
from transformers import BertTokenizer, BertModel, RobertaTokenizer, RobertaModel

def mccc_report(data):
    model = DummyClassifier(strategy="most_frequent")
    model.fit([x[0] for x in data], [x[1] for x in data])
    acc = model.score([x[0] for x in data], [x[1] for x in data])
    print(f"Dummy ACC {acc:.2%}")

class CustomBert(torch.nn.Module):
    def __init__(self, model_name, dropout):
        super().__init__()

        if model_name == "bert":
            model_name = 'bert-base-uncased'
            self.tokenizer = BertTokenizer.from_pretrained(model_name)
            self.model = BertModel.from_pretrained(model_name).to(DEVICE)
        elif model_name == "roberta":
            model_name = 'roberta-base'
            self.tokenizer = RobertaTokenizer.from_pretrained(model_name)
            self.model = RobertaModel.from_pretrained(model_name).to(DEVICE)
        elif model_name == "bertje":
            model_name = 'GroNLP/bert-base-dutch-cased'
            self.tokenizer = BertTokenizer.from_pretrained(model_name)
            self.model = BertModel.from_pretrained(model_name).to(DEVICE)
        else:
            raise Exception("Unknown model name")

        self.class_nn = torch.nn.Sequential(
            torch.nn.Dropout(p=dropout),
            torch.nn.Linear(768, 1),
            torch.nn.Sigmoid(),
        ).to(DEVICE)

    def preprocess(self, sentences):
        binarizer, sent_labels_bin = binarize_labels(sentences)
        return [
            (
                # TODO: we are truncating quite a lot of content away!
                self.tokenizer(
                    sent_txt, return_tensors="pt",
                    truncation=True
                ).to(DEVICE),
                torch.FloatTensor(sent_label_bin).to(DEVICE)
            )
            for (sent_txt, _sent_label), sent_label_bin in zip(sentences, sent_labels_bin)
        ]

    def forward(self, sent_txt):
        # TODO: check that CLS is indeed retrieved on the 0th position
        sent_embd = self.model(
            input_ids=sent_txt['input_ids'],
            attention_mask=sent_txt['attention_mask'],
        ).last_hidden_state[:, 0]
        return self.class_nn(sent_embd)

    def train_data(self, data_train, data_dev=None, batch_size=5, epochs=50):
        # self.zero_grad()
        optimizer = torch.optim.AdamW(
            self.parameters(),
            lr=2e-5,
            # eps=1e-8
        )
        loss_fun = torch.nn.BCELoss()

        for epoch in range(epochs):
            self.train()
            print(f"Epoch {epoch}")
            random.shuffle(data_train)
            for i in range(len(data_train) // batch_size):
                optimizer.zero_grad()
                batch = data_train[i * batch_size:(i + 1) * batch_size]
                loss = 0
                for sent_txt, sent_label in batch:
                    output = self(sent_txt)
                    # loss += loss_fun(output, sent_label.argmax(axis=1))
                    # print(output[0], sent_label[0])
                    loss += loss_fun(output[0], sent_label)
                # print(loss.item())
                loss.backward()
                optimizer.step()

            self.eval()
            print(f"Train ACC: {self.eval_data(data_train):.2%}")
            print(f"Dev   ACC: {self.eval_data(data_dev):.2%}")

    def eval_data(self, data):
        hits = []
        for sent_txt, sent_label in data:
            with torch.no_grad():
                output = self(sent_txt)
                # hits.append(output[0].argmax().item() == sent_label[0].argmax().item())
                # print(output[0,0].item(), sent_label[0,0].item())
                hits.append((output[0,0].item() >= 0.5)*1 == sent_label[0].item())
        return np.average(hits)