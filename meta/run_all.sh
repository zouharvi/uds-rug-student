#/bin/bash

function run_single {
    echo "Running > python3 src/train.py $@";
    python3 src/train.py "$@"
}

function run_rnn {
    run_single "$@" --batch 16;
}

# baselines
run_single majority
for DROPOUT in 0 0.1; do
    for DENSE_MODEL in 1 2 3; do
        run_single dense --dense-model $DENSE_MODEL --dropout $DROPOUT --batch 2048
    done
done

# rnn
for UNIT in lstm gru "rnn+tanh" "rnn+relu"; do
    run_rnn $UNIT
done
for HIDDEN_SIZE in 64 256 512 1024; do
    run_rnn lstm --rnn-hidden-size $HIDDEN_SIZE
done
for RNN_LAYERS in 2 3; do
    run_rnn lstm --rnn-layers $RNN_LAYERS
    run_rnn lstm --rnn-layers $RNN_LAYERS --dropout 0.1
done
run_rnn lstm --rnn-bidir
for RNN_DENSE_MODEL in 2 3; do
    run_rnn lstm --rnn-dense-model $RNN_DENSE_MODEL
done
