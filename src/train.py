from data.ontonotes import OntoNotesEmbd, tags_order, average_embd, tuple_embd
from zoo import FACTORY
import torch
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('model', help='Model to use')
parser.add_argument('--epochs', type=int, default=50,
                    help='Number of epochs to use')
parser.add_argument('--batch', type=int, default=4096,
                    help='Batch size to use')
parser.add_argument('--data', default="data/embedding_",
                    help='Prefix of path to embedding_{train,dev,test}.pkl')
parser.add_argument('--train-size', type=int, default=10000,
                    help='Number of training examples to use')
parser.add_argument('--dev-size', type=int, default=7000,
                    help='Number of dev examples to use')
args = parser.parse_args()

data_train, classes_map, classes_count = OntoNotesEmbd(args.data).get("train", args.train_size)
data_dev, _, _ = OntoNotesEmbd(args.data).get("dev", args.dev_size)
embd_size = data_train[0]["embedding"].size()[1]
print("Embeddings size", embd_size)
print("Classes count", classes_count)

data_train = torch.utils.data.DataLoader(data_train, batch_size=args.batch)
data_dev = torch.utils.data.DataLoader(data_dev, batch_size=args.batch)

params = {"embd_size": embd_size, "classes_count": classes_count, "classes_map": classes_map}
model = FACTORY[args.model](params)
model.fit(data_train, data_dev, args.epochs)
