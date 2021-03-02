import datasets
import pickle
from os.path import isfile


class OntoNotes(datasets.GeneratorBasedBuilder):
    """
    Huggingface-like loader for pre-processed .tsv files with POS tags
    Train/Dev/Test split is 80/10/10 
    """
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

    def get(self, name):
        with open(f"{self.prefix}{name}{self.suffix}", "rb") as f:
            return pickle.load(f)[name]


def tags_order(data):
    """
    Creates a joint dictionary of TAGSTR -> TAGID and TAGID -> TAGSTR
    It can be joint in one structure, because of the assumption that TAGSTR is always a string
    and TAGID is always an integer 
    """
    tags = set()
    for sent in data:
        tags = tags.union(sent["sequence"]["POS"])

    tags = list(tags)
    tagsFW = {tstr: tid for tstr, tid in enumerate(tags)}
    tagsBW = {tid: tstr for tstr, tid in enumerate(tags)}

    return {**tagsFW, **tagsBW}, len(tagsFW)