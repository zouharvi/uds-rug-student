from zoo.dense import ModelDense
from zoo.most_common import MostCommonClass
from zoo.cnn import ModelCNN
from zoo.rnn import ModelRNN

FACTORY = {
    "common": lambda params: MostCommonClass(params["classes_map"]),
    "rnn1b": lambda params: ModelRNN('rnn', True, 1, params["embd_size"], params["classes_count"]),
    "rnn2b": lambda params: ModelRNN('rnn', True, 2, params["embd_size"], params["classes_count"]),
    "rnn1": lambda params: ModelRNN('rnn', False, 1, params["embd_size"], params["classes_count"]),
    "rnn2": lambda params: ModelRNN('rnn', False, 2, params["embd_size"], params["classes_count"]),
    "lstm1b": lambda params: ModelRNN('lstm', True, 1, params["embd_size"], params["classes_count"]),
    "lstm2b": lambda params: ModelRNN('lstm', True, 2, params["embd_size"], params["classes_count"]),
    "lstm1": lambda params: ModelRNN('lstm', False, 1, params["embd_size"], params["classes_count"]),
    "lstm2": lambda params: ModelRNN('lstm', False, 2, params["embd_size"], params["classes_count"]),
    "gru1b": lambda params: ModelRNN('gru', True, 1, params["embd_size"], params["classes_count"]),
    "gru2b": lambda params: ModelRNN('gru', True, 2, params["embd_size"], params["classes_count"]),
    "gru1": lambda params: ModelRNN('gru', False, 1, params["embd_size"], params["classes_count"]),
    "gru2": lambda params: ModelRNN('gru', False, 2, params["embd_size"], params["classes_count"]),
    "dense1": lambda params: ModelDense([('L', params["embd_size"], params["classes_count"])]),
    "dense2": lambda params: ModelDense([('L', params["embd_size"], 20), ('L', 20, params["classes_count"])]),
    "dense3d": lambda params: ModelDense([('L', params["embd_size"], 100), ('D', 0.2), ('L', 100, params["classes_count"])]),
    "cnn0": lambda params: ModelCNN([('C1', 1, 64, 4), ('M', 765), ('F', 1), ('L', 64, params["classes_count"])]),
    "cnn1": lambda params: ModelCNN([('C1', 1, 64, 4), ('C1', 64, 64, 4), ('C1', 64, 64, 4), ('M', 759), ('F', 1), ('L', 64, params["classes_count"])]),
}

