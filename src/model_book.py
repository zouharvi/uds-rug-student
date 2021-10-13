import numpy as np
import torch
import random
from misc.utils import DEVICE, binarize_labels
from transformers import BertTokenizer, BertModel


class CustomBert(torch.nn.Module):
    def __init__(self, model_name):
        super().__init__()

        if model_name == "bert":
            model_name = 'bert-base-uncased'
        elif model_name == "bertje":
            model_name = 'GroNLP/bert-base-dutch-cased'

        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertModel.from_pretrained(model_name).to(DEVICE)
        self.class_nn = torch.nn.Sequential(
            torch.nn.Linear(768, 6),
            # torch.nn.Sigmoid(),
            torch.nn.Softmax(dim=1),
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
                torch.LongTensor(sent_label_bin).to(DEVICE).reshape(1, -1)
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

    def train_data(self, data_train, data_dev=None, batch_size=5, epochs=5):
        self.train()
        self.zero_grad()
        optimizer = torch.optim.AdamW(
            self.parameters(),
            lr=2e-5,
            eps=1e-8
        )
        loss_fun = torch.nn.CrossEntropyLoss()

        for epoch in range(epochs):
            print(f"Epoch {epoch}")
            random.shuffle(data_train)
            for i in range(len(data_train) // batch_size):
                optimizer.zero_grad()
                batch = data_train[i * batch_size:(i + 1) * batch_size]
                loss = 0
                for sent_txt, sent_label in batch:
                    output = self(sent_txt)
                    loss += loss_fun(output, sent_label.argmax(axis=1))
                # print(loss.item())
                loss.backward()
                optimizer.step()

            self.eval()
            print(f"Dev   ACC: {self.eval_data(data_dev):.2%}")
            print(f"Train ACC: {self.eval_data(data_train):.2%}")

    def eval_data(self, data):
        hits = []
        for sent_txt, sent_label in data:
            with torch.no_grad():
                output = self(sent_txt)
                hits.append(output[0].argmax().item() == sent_label[0].argmax().item())
        return np.average(hits)