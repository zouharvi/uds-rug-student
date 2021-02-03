# ML Basics

## Types of learning
- supervised learning: training data T = {(Xi, Yi) | i}
- - Y discrete: classification
- - Y real/power of real: (multivariate) regression
- - Y other: structured output
- unsupervised learning: trainig data T = {Xi| i}
- - clustering, density estimation, dimensionality reduction

## Data accessibility
- batch: all training data given at once, classifier is trained only once
- online: trainig data arrives sequentially, classifier is updated sequentially
- active learning: variant of semi-supervised learning, algorithm can actively query some input points to be labeled

## Learning 
- generative: estimate p(x,y) and mostly p(x|y) to get p(y|x)
- discriminative: predict directly p(y|x)
- - SVM, NNs, k-nearest neighbors

## Issues
- curse of dimensoinality
- underfitting/overfitting
- - depends on the complexity of F and the number of parameters
- - regularization may help, as it restricts the landscape
- bias/variance tradeoff
- - hard to know where to stop

## Loss function
- Y \times Y -> [0, \inf)
- - classification is either 1 or 0
- - regression e.g. squared loss L(f(x), y) = (y-f(x))^2

### Expected loss, risk
- E[L(f(X), Y)] = E[E[L(f(X), Y)|X]]
- \int [ \int L(f(x), y) p(y|x) dy] p(x) dx
- minimising the risk makes sense, because we don't care about high loss in improbable cases
- empirical loss is the average of loss across the data
- - we minimize empirical loss in lieau of expecter loss 

## IID
- independently and identically distributed data
- independet: p((x1,y1), (x2, y2), ..) = p(x1,y1)\*p(x2,y2)\*...
- identically distributed: p\_i(x,y) = p\_j(x,y) (between train and test)

## Validation
- in-time validation
- out-of-time validation (network traffic)

## Naive Bayes
- we want to model P(x|class) (maximum posterior decision)
- P(x|class) = argmax(class) p(x|class) * p(class)
- make a strong assumption  P(x|class) = \product P(x\_i|C)
- generative

## Linear Classifier
- w\*x + b <> 0
- discriminative
- leads to maximum/large margin classifier
- SVM
- - biggest margin
- - minimize ||w||^2
- - added penalization in case it can't be linearly separated
- - - dependent on the distance behind the margin
- - kernel functions may be introduced (kernel trick)
- - - gaussian, polynomial kernel

## Classification
- 1 vs rest
- 1 vs 1

## K-means clustering
- iterative method
- normalization important
- many tricks

## Training/model consideration
- cross-validation
- train-dev-test split
- missing features
- - samples left out, replaced with NaNs, replaced with means, replaced with most likely feature

# DL Overview
- model a function as a computational graph, which can be optimized with gradient descent
- first order approximation: do one step
- second order approximation: step into minimum
- - better but much more expensive (inverse of hessian)

## Gates
- add - distributes
- max - routes
- mul - switches

## Data preprocessing
- zero-centering (mean), normalizing (variance)
- decorelation (covariance matrix is diagonal), whitening (covariance matrix is I)
- batch normalization (z-normalization)

## Regularization
- dropout, explicit term

# Evasion
- causative (train time (offline + online)) = poisoning vs. exploratory (test time) = evasion
- specificity
- - direct/targeted (misclassify A as B) vs. indiscriminant (misclassify) attack
- security
- - avoid detection by decreasing TPR vs. degrade usability by increasing FPR

## Attacks
- membership inference attack
- - infer information about the training data
- - observing only input and output
- - privacy issue because large models memorize data
- model inference data
- - infer data about the model
- - observing only input and output

## Manifold
- adversial examples can be either on or off manifold
- on manifold - still in the expected input space, harder
- off manifold - arbitrary noise can be added

## Binary Classifier
- find which direction (feature) influences the output probability the most + move in that direction
- sigmoid(w,x) = 1/(1+e^{-wx})

## Adversial Condition
- empirical riski minimization
- - min E [ L(x,y,theta) ]
- empirical risk minimization in adversial conditions
- - given some wiggle room for the adversary
- - min E [ max L(x+delta, y, theta) ]
- - for a targeted case
- - - min E [ max_{over class Y} L(x+delta, y, theta) ]

## Fast Signed Gradient Method
- method to find adverarial examples
- x + epsilon * sgn(gradient of L(x,y, theta) w.r.t. the input x (not theta))
- multi-step: TODO
- requires white-box access

## Ensembles
- commonly we don't have access to the model/know only roughly the family
- we may train a single model and hope the adversial examples transfer
- it works more if we train an ensemble and create adversial examples there
- min E [ max t1*L1(x+delta, y, theta) + t2*L2(x+delta, y, theta) + .. ]
- - t1, t2, .. are weights for every model
- - L1, L2, .. are respecive loss functions/computations for every model

## Selective Attack
- adversial examples that break model 1, but leave model 2
- min E [ max t1*L1(x+delta, y, theta) - t2*L2(x+delta, y, theta) + .. ]
- (note the minus)

## Defense
- ensembles, denoising, detection, smoothing, dimensionality reduction - none really work
- distillation
- - gradient is used for attack
- - make score surface smoother so that the gradient is less informative
- - model-teacher does this
- adversarial training
- - minimize loss, maximize attack, minimize loss, .. iterate
- - (within the empirical risk formula)
- - at some point sematnic shift (as a human would rate it)

# Poisioning
- poisioning vs. clean data poisoning
- esp. problematic where there is already low data and high model capacity
- generally aim to collide with the target in the feature embedding
- creates a backdoor

## Defense
- commonly data sanatization
- must be automated (can't be checked by humans and they are not good anyway)
- attacker has limited control over the dataset
- attacker goal is to maximize test error rate given training data |Dp| = epsilon|Dc|
- defender goal is to filter out poisonous examples from Dp union Dc

## L2 centroid
- find class centroids and remove outliers
- formally
- - rate "anomality" of every example B: X times Y -> R
- - for this case, parameters of the anomaly detector are centroids (positive, negative)
- - - SB = ||x-correct_centroid||^2
- - remove "bad" points using a threshold
- quite robust

## Slab Defense
- SB = |(Cp-Cn)(x-C)| (projection on the line between centroids)
- quite robust

## Loss Defense
- SB = loss(x, y)
- removes points which can't be fitted well
- high concentration will lead to better fit on poison data

## SVD Defense
- SB = ||(I-DD)x||^2
- usually train data lie in a lower-dimensional space
- poisoned data have higher residual
- D - top k singular vectors of X
- attacker can create similar points, which will included them in lower rank representation

## KNN Defense
- SB = distance to the nearest neighbour
- attacker can however provide their own nearest neighbours

## Iterative Attack
- update feasible set and optimize for a new set of poisoned data

## Constraint Optimization
- assume no clean data removed
1. Dp = argmax loss, Dp filtered by anomaly detector B
2. update anomaly detector B by Dp
3. stop on Dp convergence

## Clean Label Poisioning
- sample an instance from the base class
- labeled by a third party
- goal: target (other sample) is then misclassified as base class
- argmin ||f(x) - f(t)||^2 + beta ||x-b||^2
- - x = sample chosen by the attacker, benign
- - t = target
- - b = base class
1. L(x) = ||f(x)-f(t)||^2, x0 = b
2. xi* = x(i-1) - lambda L(x(i-1)) # minimize predictive distance between target and sample
3. xi = (xi* + lambda beta b)(1+lambda beta)
4. goto 2

## Watermarking
- sneaky way to confuse the model, but still get original labels

# Model Stealing
- interest: architecture, training procedure, data, functionality

## Explicit Classifier Training
- train a single layer (?) classifier on top of the input and model predictions
- - predicts e.g. max pooling
- - requires that we have a local copy of a white-box model with and without max pooling
- or craft an adversarial input that looks like 1 with max pooling and like 2 without
- - then we can just read the output

## Functionality Stealing / Knock-Off Nets
- use victim querying instead of manual labeling
- victim samples inputs from PV, attacker from PA
- for student-teacher, PA = PV
- it works even if we have completely differnt inputs
- - hypothesis: just by observing the output probabilities, the new network learns the inner workings of the victim
- works even if we have different architectures
- works even if we provide only top-k or argmax (top-1)

## Defense
- output truncation does not really work and can negatively affect benign users
- idea: pertrube the output ( f(x) + delta ), so that gradient L(fAdv(x, w), y + delta) is wrong
- - limit ||delta|| <= epsilon

## Watermarking
- proof that a model was stolen
- embedding of carrier data C with watermarks W: e = E(C,W)
- we then extract the watermarks from stolen model and compare it to what we embedded
- e.g. by adding the watermark the class systematically changes
- - we query the stolen model on the original and watermarked examples
- - if the output class changes as predicted, it was stolen
- either meaningful content, independent data or pre-specified noise

# Membership Inference
- pertrubations (Adversial Image Pertrubation)
- - work, but can be countermeasured
- - decrease the quality
- - upper bound on recognizion rate

## Zero-Sum Game
- good theoretical model for this situation
- user (provider) vs attacker (recognizer)
- attacker gets reward p(i,j) for user playing strategy i and attacker strategy j
- user gets reward 1-p(i,j) (does not sum to zero :shrug:)
- if strategies are played with a distribution, then expected reward can be computed
- sum prob(i) * prob(j) * p(i, j)
- optimal strategy can be computed for the user, attackers game is then bounded by this
- - argmin\_i max\_j prob(i) prob(j) p(i, j)

## Progression
- attack: adversial petrubations make the recognizer fail
- defense: train with pertrubed examples
- attack against defense: adversial pertrubations against the new classifier

## Membership
- by training a shadow model we can still infer the membership
- TODO: watch lecture, slides are bad here
- we can observe overfitting on training examples (higher confidence)
- defense: regularization (dropout), combination
- training data can be reconstructed from posteriors

### Differential Privacy
- an algorithm that satisfies the following
- D and D' differ in one example, t is a possibly learned parameter
- sup\_t | log ( p(A(D) = t)/p(A(D') = t) ) <= epsilon
- - means that one member changes the parameters/result only a bit

# GAN and Deep Fakes
- even for pixels we can define mathematically sound sequential generation of pixels prod p(x|all previous pixels)

## Autoencoders
- denoising
- loss function simply distance to the original
- evolution to Variational Autoencoder

## GANs
- discriminator and generator networks
- very hard to train (balancing)
- can be reused for evasion attack defense
- training very unstable, every GAN is different
- - every GAN has patterns shared among generated images, which is different from others
- - these fingerprints can be visualized
- task: atribute generated output to the correct GAN model
- - architecture, training data, seed give away attribution (?)
- - frequency bands, patch sizes contain fingerprints
- attack (to make models indistinguishable)
- - add noise, blur, compress, relight, combination
- compared to real images, generated ones have power in the high spatial frequencies

## Injecting Fingerprints
- approach 1: fingerprint the dataset
- - easy to do, but does not scale (needs to be repeated for every new fingerprint)
- approach 2: train GAN with a fingerprint autoencoder
- - fingerprint is a 128bit key that can be extracted/detected
- - 2^128 unique fingerprints

# Malware Detection
- multiple layers: binary/source code/intermediate representation
- source code can be represented as a binary, n-grams (AST traversal), path context, API calls
- other static analyses

## Android Example
- opcodes for application calls (?)
- serialized into one sequence, embedded as one hot, then embedding, then CNN layer, dynamic max pooling to get a fixed vector representation, hidden layer, softmax

## JavaScript Example
- convert every character into binary vector (ASCII), project to lower dimensionality
- denoising autoencoder

## Evasion
- malware + non-interfering noise = adversial malware
- given whitebox access and the feature list, we can see what features influence the decision the most and add this feature
- can be crafted also with GAN, where we substitute the detector by our own
- works very well even if the detector is of completely different model family

# Anomaly Detection
- supervised: (cat vs dog), anomaly: (not cat)
- novelty detection: training time only regular data
- outlier detection: training time regular + outlier data
- prototypically anomaly detection
- supervised learning can't be employed, since the anomalies are usually rare and novel
- examples
- - host intrusion detection
- - network intrusion detection
- - web app intrusion detection

## Approaches
- was done by threshold/dynamic threshold, but this quickly gets out of hand
- data-driven approach as to accomodate seasonality and trends
- elliptic envelope (covariance estimation, gauss), one class SVM, isolation forests, k-means cluster distance (similar to gaussian mixture)

## Forecasting
- has to deal with trends
- auto-regressive, moving-average model, combination
- - simple but does not scale well for higher dimensional input
- RNNs (vanilla, GRU, LSTM)
- - works well with all shapes, but hard to inspect, perhaps computationaly expensive

# Privacy
- simply anonymization of data is not enough, small data as well
- privacy barier
- privacy loss is the sum of privacy losses

## Differential Privacy (continued)
- A(D+z) has similar distribution as A(D)
- (epsilon, delta) relaxation: max |log( (p(A(D) in S) - delta)/( p(A(D') in S) ) )| <= epsilon
- - can be restated as p(A(D) in S) <= e^epsilon p(A(D') in S) + delta
- - basically delta slack is added

## SGD
- can be made private by adding noise to the gradient
- also clipping, so no big updates on individual samples (bound sensitivity)
- privacy loss is accumulated every iteration)
- random subsampling improves this further

## Private Aggregation of Teacher Ensembles (PATE)
- we can split the data into subsets and train teachers individually
- query teachers on public but unannotated data
- get blackbox teacher responses, but still add noise to the votes
- take maximum for the student
- publish only the student
