#!/usr/bin/env python3
import datasets
from transformers import AutoTokenizer, BertModel
from data.ontonotes import average_embd, tags_order
import torch
import pickle
from utils import DEVICE
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--data', default="data/all.tsv",
                    help='Path to parsed tsv')
parser.add_argument('--data-out', default="data/embedding_x.pkl",
                    help='Where to store pickled embeddings')
parser.add_argument('--name', default="test",
                    help='Section of the data to use (train, validation/dev, test)')
parser.add_argument('--no-hotswap', action="store_true",
                    help='Hotswap to CPU when GPU is out of memory')
parser.add_argument('--no-half', action="store_true",
                    help='Disable halving the precision')
parser.add_argument('--hotswap-threshold', default=3072, type=int,
                    help='Threshold (in MB) from which to store data on CPU')
parser.add_argument('--seed', type=int, default=0,
                    help='Seed to use for shuffling')
args = parser.parse_args()

if args.name == "dev":
    args.name = "validation"

print("* Loading data")
data = datasets.load_dataset(
    "./src/data/ontonotes.py",
    data_files=args.data,
    config={"seed": args.seed}
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

if not args.no_hotswap:
    hotswap_ptr = 0
    gpu_total = torch.cuda.get_device_properties(device=DEVICE).total_memory
data_embd = []

classes_map, classes_count = tags_order(
    data["train"]+data["validation"]+data["test"]
)
with torch.no_grad():
    for i, sentence in enumerate(data[args.name]):
        if not args.no_hotswap:
            gpu_used = torch.cuda.memory_allocated(device=DEVICE)
            if (gpu_total - gpu_used) <= args.hotswap_threshold*1024*1024:
                if hotswap_ptr >= len(data_embd):
                    raise Exception(
                        "Attempted to hotswap out of GPU, but not enough computed.")
                tmp = data_embd[hotswap_ptr]["embedding"].detach().cpu()
                del data_embd[hotswap_ptr]["embedding"]
                data_embd[hotswap_ptr]["embedding"] = tmp
                torch.cuda.empty_cache()
                hotswap_ptr += 1

        if i % 200 == 0:
            print(f"{i/len(data[args.name])*100:5.3}%",
                  f"Free mem: {(gpu_total - gpu_used)/1024/1024:4.0f}MB" if not args.no_hotswap else "")

        # This could be done faster by padding the sentences and increasing the batch size,
        # on the other hand, the cost of this is just extra an extra few minutes.
        output = model(
            torch.LongTensor([sentence["input_ids"]]).to(DEVICE),
            output_hidden_states=True
        )
        final_tensor = torch.reshape(
                output.hidden_states[0],
                (len(sentence["input_ids"]), -1),
            )
        if not args.no_half:
            final_tensor = final_tensor.half()
        data_embd.append({
            **sentence,
            "embedding": final_tensor
        })

with open(args.data_out, "wb") as f:
    pickle.dump({
        "data": average_embd(data_embd, "cpu"),
        "classes_map": classes_map,
        "classes_count": classes_count
    }, f)
