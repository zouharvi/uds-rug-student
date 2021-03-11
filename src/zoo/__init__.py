from utils import DEVICE
from zoo.cnnsent import ModelCNNSent
from zoo.dense import ModelDense
from zoo.majority import MajorityClassifier
from zoo.cnn import ModelCNN
from zoo.rnn import ModelRNN
from pathlib import Path

_FACTORY = {
    "majority": lambda params, _: MajorityClassifier(params["classes_map"]),
    "dense": lambda params, args: ModelDense(args.dense_model, args.dropout, params["embd_size"], params["classes_count"]),
    "rnn": lambda params, args: ModelRNN('rnn', args.rnn_bidir, args.rnn_layers, params["embd_size"], params["classes_count"], args.rnn_hidden_size, args.dense_model),
    "gru": lambda params, args: ModelRNN('gru', args.rnn_bidir, args.rnn_layers, params["embd_size"], params["classes_count"], args.rnn_hidden_size, args.dense_model),
    "lstm": lambda params, args: ModelRNN('lstm', args.rnn_bidir, args.rnn_layers, params["embd_size"], params["classes_count"], args.rnn_hidden_size, args.dense_model),

    # Broken, deprecated
    "cnnsent1": lambda params, _: ModelCNNSent(params["embd_size"], params["classes_count"]),
    "cnn1": lambda params, _: ModelCNN([('C1', 1, 64, 16), ('M', 50), ('F', 1), ('L', 960, params["classes_count"])]),
    "cnn2": lambda params, _: ModelCNN([('C1', 1, 64, 128), ('M', 641), ('F', 1), ('L', 64, params["classes_count"])]),
    "cnn3": lambda params, _: ModelCNN([('C1', 1, 64, 4), ('C1', 64, 64, 4), ('C1', 64, 64, 4), ('M', 759), ('F', 1), ('L', 64, params["classes_count"])]),
}


def factory(name, params, args):
    model = _FACTORY[name](params, args)
    if name != "majority":
        model.to(DEVICE)
    model.name = name
    Path(args.save_path+"/"+name).mkdir(parents=True, exist_ok=True)
    return model
