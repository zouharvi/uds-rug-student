#/bin/bash

function run_single {
    echo "> python3 src/train.py $@";
    sleep 1;
    # python3 src/train.py "$@"
}

function run_rnns {
    run_single "rnn+tanh" "$@";
    run_single "rnn+relu" "$@";
    run_single "gru" "$@";
    run_single "lstm" "$@";
}

# baselines
run_single majority
for DROPOUT in 0 0.1; do
    for DENSE_MODEL in 1 2 3; do
        run_single dense --dense-model $DENSE_MODEL --dropout $DROPOUT
    done
done

# rnn
for DROPOUT in 0 0.1 0.2 0.3 0.4; do
    run_rnns --dropout $DROPOUT
done
for HIDDEN_SIZE in 16 32 64 128 256 512 1024; do
    run_rnns --rnn-hidden-size $HIDDEN_SIZE
done
for RNN_LAYERS in 1 2 3; do
    run_rnns --rnn-layers $RNN_LAYERS
done
for RNN_BIDIR in false true; do
    run_rnns --rnn-bidir $RNN_BIDIR
done
for RNN_DENSE_MODEL in 1 2 3; do
    run_rnns --rnn-dense-model $RNN_DENSE_MODEL
done
