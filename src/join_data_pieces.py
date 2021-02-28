import pickle

with open("data/embedding_train1.pkl", "rb") as f:
    data1 = pickle.load(f)
with open("data/embedding_train2.pkl", "rb") as f:
    data2 = pickle.load(f)

data = {"train": data1["train"]+data2["train"]}
with open("data/embedding_train.pkl", "wb") as f:
    pickle.dump(data, f)