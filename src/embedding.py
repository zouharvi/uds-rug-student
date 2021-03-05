import datasets
from transformers import AutoTokenizer, BertModel
import torch
import pickle
from utils import DEVICE
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--data', default="data/all.tsv", help='Path to parsed tsv')
parser.add_argument('--out', default="data/embedding_x.pkl", help='Where to store pickled embeddings')
args = parser.parse_args()


print("* Loading data")
data = datasets.load_dataset(
    "./src/data/ontonotes.py",
    data_files=args.data,
)

print("* Tokenizing data")
tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
data = {
    split: [
        {
            "sid": sentence["sid"],
            "sequence": sentence["sequence"],
            "input_ids": tokenizer(sentence["raw"])["input_ids"]
        }
        for sentence in data[split]
    ]
    for split in data
}


print("* Computing embeddings")
model = BertModel.from_pretrained("bert-base-cased")
model.to(DEVICE)
model.eval()

data_embd = {}

for split in ["test"]:
    data_embd[split] = []
    for i, sentence in enumerate(data[split]):
        print(f"{i/len(data[split])*100:.5}%")

        # This could be done faster by padding the sentences and increasing the batch size,
        # on the other hand, the cost of this is just leaving the computer to run overnight
        # for an hour.
        output = model(
            torch.LongTensor([sentence["input_ids"]], device=DEVICE),
            output_hidden_states=True
        )
        data_embd[split].append({
            **sentence,
            "embedding": torch.reshape(
                output.hidden_states[0],
                (len(sentence["input_ids"]), -1)
            )
        })

with open(args.out, "wb") as f:
    pickle.dump(data_embd, f)
