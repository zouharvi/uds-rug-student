# ML Overview

## Types of learning
- supervised learning: training data T = {(Xi, Yi) | i}
- - Y discrete: classification
- - Y real/power of real: regression
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


## Issues
- curse of dimensoinality
- underfitting/overfitting, bias/variance tradeoff

## Loss function
- Y \times Y -> [0, \inf)
- - classification is either 1 or 0
- - regression e.g. squared loss L(f(x), y) = (y-f(x))^2


### Expected loss, risk
- E[L(f(X), Y)] = E[E[L(f(X), Y)|X]]
- \int [ \int L(f(x), y) p(y|x) dy] p(x) dx
- minimising the risk makes sense, because we don't care about high loss in improbable cases
- empirical loss is the average of loss across the data

## IID
- independently and identically distributed data
- independet: p((x1,y1), (x2, y2), ..) = p(x1,y1)\*p(x2,y2)\*...
- identically distributed: p\_i(x,y) = p\_j(x,y) (between train and test)


## Validation
- in-time validation
- out-of-time validation (network traffic)
