import torch
import datasets
from transformers import AutoTokenizer
import pickle
import random
from os.path import isfile


class OntoNotes(datasets.GeneratorBasedBuilder):
    """
    Huggingface-like loader for pre-processed .tsv files with POS tags
    Train/Dev/Test split is 80/10/10
    """

    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.seed = config["seed"]

    def _info(self):
        return datasets.DatasetInfo(
            features=datasets.Features(
                {
                    "sid": datasets.Value("uint32"),
                    "sequence": datasets.features.Sequence(
                        {
                            "token": datasets.Value("string"),
                            "POS": datasets.Value("string"),
                        }
                    ),
                    "raw": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
        )

    def _split_generators(self, _dl_manager):
        data = []
        with open(self.config.data_files) as f:
            buffer = []
            for id_, row in enumerate(f):
                row = row.rstrip("\n")
                if row == "*":
                    data.append((id_, {
                        "sid": id_,
                        "sequence": buffer,
                        "raw": " ".join([x["token"] for x in buffer]),
                    }))
                    buffer = []
                else:
                    x = row.split("\t")
                    buffer.append({
                        "token": x[1],
                        "POS": x[2],
                    })
        random.seed(self.seed)
        random.shuffle(data)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "data": data[int(0.0*len(data)):int(0.8*len(data))],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "data": data[int(0.8*len(data)):int(0.9*len(data))],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "data": data[int(0.9*len(data)):int(1.0*len(data))],
                },
            ),
        ]

    def _generate_examples(self, data):
        for x in data:
            yield x

def tags_order(data):
    """
    Creates a joint dictionary of TAGSTR -> TAGID and TAGID -> TAGSTR
    It can be joint in one structure, because of the assumption that TAGSTR is always a string
    and TAGID is always an integer
    """
    tags = set()
    for sent in data:
        tags = tags.union(sent["sequence"]["POS"])

    tags = sorted(list(tags), key=lambda x: x)
    tagsFW = {tstr: tid for tstr, tid in enumerate(tags)}
    tagsBW = {tid: tstr for tstr, tid in enumerate(tags)}

    return {**tagsFW, **tagsBW}, len(tagsFW)


def average_embd(data, device="cuda:0"):
    """
    Averages embeddings of subwords in one token
    """
    tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
    data_new = []
    unparsable_sents = 0
    for sent in data:
        buffer = []
        embeddings_new = []
        buffer_str = ""
        token_list = list(sent["sequence"]["token"])
        cur_token = token_list.pop(0)

        for i, sub_token in enumerate(tokenizer.convert_ids_to_tokens(sent["input_ids"])):
            if sub_token == "[CLS]":
                continue
            if (buffer_str == "[UNK]" or len(buffer_str) == len(cur_token)) and len(buffer) != 0:
                # can also be [SEP]
                embeddings_new.append(
                    torch.mean(torch.stack(buffer, dim=0), dim=0).to(device)
                )
                if len(token_list) == 0:
                    break
                if buffer_str != cur_token and buffer_str != "[UNK]":
                    unparsable_sents += 1
                    break

                cur_token = token_list.pop(0)
                buffer = []
                buffer_str = ""

            if sub_token.startswith("##"):
                buffer_str += sub_token[2:]
            else:
                buffer_str += sub_token
            buffer.append(sent["embedding"][i])

        if len(embeddings_new) != len(sent["sequence"]["POS"]):
            unparsable_sents += 1
        else:
            data_new.append((embeddings_new, sent["sequence"]["POS"]))
    print(f"Unparsed sents: {unparsable_sents}/{len(data)}")

    return data_new


class OntoNotesEmbd():
    """
    Custom loader for computed embeddings
    """

    def __init__(self, prefix, suffix=".pkl"):
        self.prefix = prefix
        self.suffix = suffix
        if all([not isfile(prefix + name + suffix) for name in {"train", "dev", "test"}]):
            raise Exception(
                "None of the embedding pickle files exist (train, dev, test). " +
                "All `get` calls will fail"
            )

    def get(self, name, size=None, keep_sent=False):
        with open(f"{self.prefix}{name}{self.suffix}", "rb") as f:
            data = pickle.load(f)
            print("loaded", name)
            return (tuple_embd(data["data"][:size], data["classes_map"], keep_sent), data["classes_map"], data["classes_count"])


def tuple_embd(data, pos_mapper, keep_sent):
    """
    TODO
    """
    if keep_sent:
        return [
            (
                sent[0],
                [pos_mapper[pos] for pos in sent[1]]
            )
            for sent in data
        ]
    else:
        return [
            (embd, pos_mapper[pos])
            for sent in data for embd, pos in zip(sent[0], sent[1])
        ]
