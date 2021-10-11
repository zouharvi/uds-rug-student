import torch

if torch.cuda.is_available():
    DEVICE = torch.device("cuda")
else:
    DEVICE = torch.device("cpu")
DEVICE_CPU = torch.device("cpu")

def binarize_label(sent_label):
    return (
        1 if sent_label == "music" else 0,
        1 if sent_label == "books" else 0,
        1 if sent_label == "health" else 0,
        1 if sent_label == "dvd" else 0,
        1 if sent_label == "software" else 0,
        1 if sent_label == "camera" else 0,
    )