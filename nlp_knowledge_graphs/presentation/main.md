---
title: "Barack's Wife Hillary"
header-includes:
  - \AtBeginDocument{\title[Barack’s Wife Hillary]{Barack’s Wife Hillary:\newline Using Knowledge Graphs for Fact-Aware Language Modeling}}
subtitle:
- "Robert L. Logan IV, Nelson F. Liu, Matthew E. Peters, Matt Gardner, Sameer Singh"
author:
- Vilém Zouhar (presenter)
theme:
- Boadilla
date:
- February, 2021
aspectratio: 169

documentclass: beamer
# classoption: notes
---

# Overview

- Language modelling
- - Sentence completion using factual knowledge
- - Explicit information access
- Knowledge graph language model
- - Definition
- - Example
- - Computation
- - Training and inference
- Experiments

# Language Modelling

Next word completion:

> - `Super Mario Land is a 1989 video game developed and ____`
> - Fluency: \newline
    `Super Mario is a 1989 video game developed and published by ____`
> - Adequacy / Basic reasoning: \newline
    `Super Mario is a 1989 video game developed and published by Valve` \newline
    _Valve_ is an entity that could potentially develop and publish a video game  \newline
    Founded in 1996    
> - Factual correctness: \newline
    `Super Mario is a 1989 video game developed and published by Nintendo`

# Language Modelling

Achievements:

> - Fluency? Yes - even n-gram models
> - Adequacy? Yes - BERT derivatives
> - Factual correctness?
> - - BERT derivatives (stored in the parameters)
> - - Explicit information structure (KG)

# Explicit information access

Advantages:

> - Language model and database separate \newline
    adding information without retraining LM 
> - Performance on unseen/rare entities
> - Explainability

Control:

>   1. Prompt: `Barack is married to ___`
>   2. Reponse: `Barack is married to Michelle`
>   3. *Change the entity in the KG
>   4. Reponse: `Barack is married to Hillary`

Disadvantages:

> - Research and mass adoption missing
> - Two components to setup and maintain

\note{
  TODO

  A big advantage is being able to modify facts after the language model training. This is not possible for standard language models, because the facts are stored in the trained parameters - in their generative ability. With separate structures, it is possible to verify that changing the relevant entry will yield different generative results.
}

# Knowledge Graph Language Model

::: columns
:::: column
Components:

- Standard language model
- External knowledge graph
- Local knowledge graph (subset of ^) 
- - For mentioned entities
::::

:::: column
Actions:

- Generating new entity:
- - Access external
- - Add to local
- - Render
- Generating encountered entity
- - Access local
- - Render
::::
:::

# LM + KG

> - Standard LM: \newline
  $p(x_t|x_{< t}) = \text{softmax}(W_h h_t + b_h), h_t = \text{LSTM}(h_{t-1},x_{t-1})$
> - Knowledge graph: \newline
  $\mathcal{KG} = \{(\text{parent}, \text{relation}, \text{entity})| \text{parent, entity} \in \mathcal{E}, \text{relation} \in \mathcal{R}\}$
> - Local knowledge graph: \newline
  $\mathcal{KG}_{< t}$ entities participating in first $t$ tokens
> - LM + KG: \newline
  $p(x_t, \mathcal{KG}_t|x_{< t}, \mathcal{KG}_{< t})$
> - Decision/type of token $t: t_t \in \{\emptyset, \text{new}, \text{related}\}$

\note{
    New entity mention, new entity, related entity
} 

# LM + KG

Decision/type of token $t: t_t$

> - $t_t = \emptyset$: choose $e_t = \emptyset$
> - $t_t = \text{new}$: choose $e_t \in \mathcal{E}$
> - $t_t = \text{related}$: \newline
    choose $\text{parent}_t \in \mathcal{E}_{< t}$ \newline
    choose $\text{relation}_t \in \{r|(\text{parent}_t, r, e) \in \mathcal{KG}_{< t}\}$ \newline
    choose $\text{entity}_t \in \{e|(\text{parent}_t, \text{relation}_t, e) \in \mathcal{KG}_{< t}\}$

> - Update local KG: $\mathcal{E}_{< t+1} = \mathcal{E}_{< t+1} \cup \{e_t\}$ 

# Computation

- $h_t = [h_{t,x};h_{t,p};h_{t,r}]$
- $t_t = \text{softmax}(W_t h_{t,x} + b_t)$ 

- $t_t = \text{new}$
- - $e_t = \text{softmax}(v_e\cdot (h_{t,p}+h_{t,r}))$
- $t_t = \text{related}$
- - $p_t = \text{softmax}(v_p\cdot h_{t,p})$
- - $r_t = \text{softmax}(v_r\cdot h_{t,r})$ (restricted by $p_t$)

# Rendering Entity

> - $t_t = \emptyset$ standard LM (condition on $h_{t,x}$)
> - $t_t = \text{new}$: choose $e_t \in \mathcal{E}$
> - $t_t = \text{related}$: \newline
    choose $\text{parent}_t \in \mathcal{E}_{< t}$ \newline
    choose $\text{relation}_t \in \{r|(\text{parent}_t, r, e) \in \mathcal{KG}_{< t}\}$ \newline
    choose $\text{entity}_t \in \{e|(\text{parent}_t, \text{relation}_t, e) \in \mathcal{KG}_{< t}\}$

TODO

We care still about the produced token, therefore: $p(x_t) = \sum_{\mathcal{E}_t} p(x_t, \mathcal{E}_t)$

\note{
    Split hidden state to word, parent and relation
}

# Linked WikiText-2

1. Entity recognition
2. Coreference using Stanford CoreNLP
3. Wikipedia links + neural-el entity linker
4. Sequentially parse tokens and create local KGs
5. Rule-based post-processing (dates, quantities, entities)


TODO

\note{
  - Data hard to come by
  - Derivative of WikiText-2
}

# Annotation

![](img/annotation_example.png){width=100%}

\centering

Figure 2: Annotation example

\note{
  - TODO: pick a few examples
  - TODO: perhaps move this before the computation
}

# Training, Inference

Training:

- Loss function: $\sum \log p(x_t, \mathcal{E}_t | x_{< t}, \mathcal{E}_{< t}, \Theta)$

Inference

- $p(x) = \sum_\mathcal{E} p(x, \mathcal{E})$ hard to compute
- $p(x) = \sum_{\mathcal{E}} \frac{p(x_t, \mathcal{E}_t)}{q(\mathcal{E}_t|x_t)}\cdot q(\mathcal{E}_t|x_t) \approx \frac{1}{N} \sum_{\mathcal{E} \sim q} \frac{p(x_t, \mathcal{E}_t)}{q(\mathcal{E}_t|x_t)}$ 

\note{
  - TODO: approximation
  - TODO: what is $q$
}

# Metrics

Perplexity

- geometric average probability of the all data: \newline
  $p(x_1, x_2, x_3, \ldots)^{1/T} = exp(\frac{1}{T} \sum_1^T log p(x_t))$

Unknown penalized perplexity

> - What about `<UNK> <UNK>'s wife is <UNK> <UNK>`?
> - $\mathcal{U} = \{t|f(t) =\texttt{<UNK>}\}$
> - $p'(\texttt{<UNK>}) = \frac{1}{|\mathcal{U}|} p(\texttt{<UNK>})$
> - Compute perplexity on $p'$

\note{
  - Standard perplexity is not the best metrics for texts containing named entities: predicting unknown/unseen words as `<UNK>` yields good results, even though no information is transferred.
  - Solution would be to penalize predicting `<UNK>` more than other tokens.
  - Distribute the predicted probability among all tokens that map to `<UNK>`
  TODO
}

# Fact completion

TODO

# Future Work

TODO

# References

Research content and all figures:

```
@article{logan2019barack,
  title={Barack's Wife Hillary: Using Knowledge-Graphs for
    Fact-Aware Language Modeling},
  author={Logan IV, Robert L and Liu, Nelson F and Peters, Matthew E
    and Gardner, Matt and Singh, Sameer},
  journal={arXiv preprint arXiv:1906.07241},
  year={2019}
}
```