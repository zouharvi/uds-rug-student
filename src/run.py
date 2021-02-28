import datasets
import torch
from transformers import AutoTokenizer, BertModel

print("* Loading data")
data = datasets.load_dataset(
    "./src/data/ontonotes.py",
    data_files="data/all.tsv",
)

print("* Tokenizing data")
tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
data = {
    split: [
        {**sentence, **tokenizer(sentence["raw"])}
        for sentence in data[split]
    ]
    for split in data
}

print("* Computing embeddings")
model = BertModel.from_pretrained("bert-base-cased")
model.eval()

data_embd = {}
for split in data:
    data_embd[split] = []
    for sentence in data[split]:
        # data_embd[split].append()
        output = model(torch.LongTensor([sentence["input_ids"]]), output_hidden_states=True)
        data_embd[split].append(
            torch.reshape(
                output.hidden_states[0],
                (len(sentence["input_ids"]), -1)
            )
        )

# dataset = datasets.load_dataset('csv', delimiter="\t", data_files=['data/all.tsv'])
