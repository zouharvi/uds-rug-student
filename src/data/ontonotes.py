from transformers import AutoTokenizer, BertModel
import datasets


class OntoNotes(datasets.GeneratorBasedBuilder):
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
        tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
        model = BertModel.from_pretrained("bert-base-cased")
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
                    "data": data[int(0.0*len(data)):int(0.9*len(data))],
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
