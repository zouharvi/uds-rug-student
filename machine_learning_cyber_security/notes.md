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
