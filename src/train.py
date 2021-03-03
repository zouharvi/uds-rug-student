from data.ontonotes import OntoNotesEmbd, tags_order, average_embd, tuple_embd
from zoo import ModelDense
import torch

data_dev = OntoNotesEmbd("data/embedding_").get("dev")
data_test = OntoNotesEmbd("data/embedding_").get("test")
classes_map, classes_count = tags_order(data_dev)
embd_size = data_dev[0]["embedding"].size()[1]
print("Embeddings size", embd_size)
print("Classes count", classes_count)

data_dev = tuple_embd(average_embd(data_dev), classes_map)
data_test = tuple_embd(average_embd(data_test), classes_map)
data_dev = torch.utils.data.DataLoader(data_dev, batch_size=16)

model = ModelDense([('L', embd_size, classes_count)])
model.fit(data_dev, data_test, 50)