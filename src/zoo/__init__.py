from utils import DEVICE
from zoo.cnnsent import ModelCNNSent
from zoo.dense import ModelDense
from zoo.majority import MajorityClassifier
from zoo.cnn import ModelCNN
from zoo.rnn import ModelRNN
from pathlib import Path

_FACTORY = {
    "majority": lambda params: MajorityClassifier(params["classes_map"]),
    "rnn1b": lambda params: ModelRNN('rnn', True, 1, params["embd_size"], params["classes_count"], hidden_dim=100),
    "rnn2b": lambda params: ModelRNN('rnn', True, 2, params["embd_size"], params["classes_count"], hidden_dim=100),
    "rnn1": lambda params: ModelRNN('rnn', False, 1, params["embd_size"], params["classes_count"], hidden_dim=100),
    "rnn2": lambda params: ModelRNN('rnn', False, 2, params["embd_size"], params["classes_count"], hidden_dim=100),
    "lstm1b": lambda params: ModelRNN('lstm', True, 1, params["embd_size"], params["classes_count"], hidden_dim=100),
    "lstm2b": lambda params: ModelRNN('lstm', True, 2, params["embd_size"], params["classes_count"], hidden_dim=100),
    "lstm1": lambda params: ModelRNN('lstm', False, 1, params["embd_size"], params["classes_count"], hidden_dim=100),
    "lstm2": lambda params: ModelRNN('lstm', False, 2, params["embd_size"], params["classes_count"], hidden_dim=100),
    "gru1b": lambda params: ModelRNN('gru', True, 1, params["embd_size"], params["classes_count"], hidden_dim=100),
    "gru2b": lambda params: ModelRNN('gru', True, 2, params["embd_size"], params["classes_count"], hidden_dim=100),
    "gru1": lambda params: ModelRNN('gru', False, 1, params["embd_size"], params["classes_count"], hidden_dim=100),
    "gru2": lambda params: ModelRNN('gru', False, 2, params["embd_size"], params["classes_count"], hidden_dim=100),
    "dense1": lambda params: ModelDense([('L', params["embd_size"], params["classes_count"])]),
    "dense2": lambda params: ModelDense([('L', params["embd_size"], 20), ('L', 20, params["classes_count"])]),
    "dense3": lambda params: ModelDense([('L', params["embd_size"], 60), ('L', 60, params["classes_count"])]),
    "dense3d": lambda params: ModelDense([('L', params["embd_size"], 60), ('D', 0.1), ('L', 60, params["classes_count"])]),
    "dense4": lambda params: ModelDense([('L', params["embd_size"], 64), ('L', 64, 64), ('L', 64, params["classes_count"])]),
    "dense4d": lambda params: ModelDense([('L', params["embd_size"], 64), ('D', 0.1), ('L', 64, 64), ('D', 0.1), ('L', 64, params["classes_count"])]),
    "cnnsent1": lambda params: ModelCNNSent(params["embd_size"], params["classes_count"]),
    "cnn1": lambda params: ModelCNN([('C1', 1, 64, 16), ('M', 50), ('F', 1), ('L', 960, params["classes_count"])]),
    "cnn2": lambda params: ModelCNN([('C1', 1, 64, 128), ('M', 641), ('F', 1), ('L', 64, params["classes_count"])]),
    # TODO
    "cnn3": lambda params: ModelCNN([('C1', 1, 64, 4), ('C1', 64, 64, 4), ('C1', 64, 64, 4), ('M', 759), ('F', 1), ('L', 64, params["classes_count"])]),
}


def factory(name, params, save_path):
    model = _FACTORY[name](params)
    if name != "majority":
        model.to(DEVICE)
    model.name = name
    Path(save_path+"/"+name).mkdir(parents=True, exist_ok=True)
    return model