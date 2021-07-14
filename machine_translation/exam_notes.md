MT exam notes

# Meta
- nothing on rule-based MT
- bring a phone/calculator
- 50% explanatory, 50% computation (alignment, em, computation)
- bring a test/vaccination

# 1
- LM and perplexity
- what do they do & tell us
- how can we model probability
- faithful approximation and what the issue is
- - Markov assumption
- TODO: check what bigram and trigram model is, crosscheck with slides (seems to be one off)
- two ways perplexity is computed
- probability:
- - bayes rule, prior, likelihood, posterior
- - noisy channel model

# 2
- statistical machine translation
- alignments, expectation maximization
- word-based SMT
- phrase-based SMT, alignment grid, extracting phrases, consistency
- decoding algorithm, beam search
- explain IBM given the formulas

# 3
- FFNNs
- activation functions and their gradients
- logistic regression
- what is learning and what parameters does it have
- what is error and gradient descend (descent?)
- computation graph, dynamic programming, backpropagation
- Matrix multiplication and stuff
- Hyperparameters vs parameters
- Cost vs loss function (squared, cross-entropy)

# 4
- encoder-decoder (vanilla RNN, LSTM)
- bottleneck, sequence-to-sequence
- vanishing and exploding gradients
- parameters are shared, etc..
- backpropagation through time
- contextualized vs static

# 5
- word-embeddings, one-hot embedding
- CBOW, skipgram
- distributional semantics

# 6
- attention
- - weighting encoder states, etc
- transformer
- - self-attention, cross-attention, masked-attention
- - addressing mechanism (different matricies)
- - positional encoding

# 7
- evaluation, quality estimation
- f-scores, precision, recall
- word based vs. n-gram based
- BLEU
- differences between human & automatic evaluation

How much do we need to know the formulas, e.g. for IBM3.
