import torch
import random
from utils import DEVICE, binarize_label
from transformers import BertTokenizer, BertModel


class CustomBert(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained('bert-base-uncased').to(DEVICE)
        self.class_nn = torch.nn.Sequential(
            torch.nn.Linear(768, 6),
            # torch.nn.Sigmoid(),
            torch.nn.Softmax(),
        ).to(DEVICE)

    def preprocess(self, sentences):
        return [
            (
                # TODO: we are truncating quite a lot of content away!
                self.tokenizer(
                    sent_txt, return_tensors="pt",
                    truncation=True
                ).to(DEVICE),
                torch.LongTensor(
                    binarize_label(sent_label)
                ).to(DEVICE).reshape(1,-1)
            )
            for sent_txt, sent_label in sentences
        ]

    def forward(self, sent_txt):
        # TODO: check that CLS is indeed retrieved on the 0th position
        sent_embd = self.model(
            input_ids=sent_txt['input_ids'],
            attention_mask=sent_txt['attention_mask'],
        ).last_hidden_state[:,0]
        return self.class_nn(sent_embd)

    def train_epochs(self, sentences, batch_size=5, epochs=5):
        self.train()
        self.zero_grad()
        optimizer = torch.optim.AdamW(
            self.parameters(),
            lr=2e-5,
            eps=1e-8
        )
        loss_fun = torch.nn.CrossEntropyLoss()

        for epoch in range(epochs):
            random.shuffle(sentences)
            for i in range(len(sentences)//batch_size):
                optimizer.zero_grad()
                batch = sentences[i*batch_size:(i+1)*batch_size]
                loss = 0
                for sent_txt, sent_label in batch:
                    output = self(sent_txt)
                    loss += loss_fun(output, sent_label.argmax(axis=1))
                # print last loss
                # print(loss.item())
                loss.backward()
                optimizer.step()

            self.eval()
            hits = 0
            for sent_txt, sent_label in sentences:
                with torch.no_grad():
                    output = self(sent_txt)
                    # print(output, sent_label)
                    # print(output.shape, sent_label.shape)
                    # print(sent_label.argmax(axis=0).shape, sent_label.argmax(axis=1).shape)
                    # print(output[0].argmax().item(), sent_label[0].argmax().item())
                    if output[0].argmax().item() == sent_label[0].argmax().item():
                        hits += 1

            print(f"Train ACC: {hits/len(sentences):.2%}")
