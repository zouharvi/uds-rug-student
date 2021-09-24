from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import sklearn.svm
from sklearn.metrics import accuracy_score
import pickle
import numpy as np

def experiment_features(X_full, Y_full, tf_idf, use_ngrams, max_features, data_out=None):
    ngram_range = (2, 3) if use_ngrams else (1, 1)

    model = Pipeline([
        ("vec",
         TfidfVectorizer(
             preprocessor=lambda x: x,
             tokenizer=lambda x:x, max_features=max_features,
             ngram_range=ngram_range,
         )
         if tf_idf else
         CountVectorizer(
             preprocessor=lambda x: x,
             tokenizer=lambda x:x, max_features=max_features,
             ngram_range=ngram_range,
         ),
         ),
        ("svm", sklearn.svm.SVC(kernel="linear")),
    ])
    model.fit(X_full, Y_full)
    Y_pred = model.predict(X_full)
    score = accuracy_score(Y_full, Y_pred)
    print(f"train acc: {score:.2%}")

    coefs_original = model.get_params()["svm"].coef_.toarray().reshape(-1)
    coefs = sorted(enumerate(coefs_original), key=lambda x: x[1])

    vocab = model.get_params()["vec"].vocabulary_
    vec = {v: k for k, v in vocab.items()}

    # Print
    pivot = (len(coefs) - 8) // 2
    print("positive:\n", "\n".join(
        [f" {vec[ind]} ({v:.2f})" for ind, v in coefs[-8:]]), sep="")
    print("neutral:\n", "\n".join(
        [f" {vec[ind]} ({v:.2f})" for ind, v in coefs[pivot:pivot + 8]]), sep="")
    print("negative:\n", "\n".join(
        [f" {vec[ind]} ({v:.2f})" for ind, v in coefs[:8]]), sep="")

    # Store coefficients if argument is passed
    if data_out is not None:
        with open(data_out, "wb") as f:
            pickle.dump([(vec[ind], v) for ind, v in coefs], f)

    # Compute norms
    X_vec = model["vec"].transform(X_full).toarray()
    print(
        "avg data norm",
        np.average(np.linalg.norm(X_vec, axis=1))
    )
    print(
        "coefs norm",
        np.average(
            np.absolute(
                model.get_params()["svm"].coef_.toarray().reshape(-1)
            )
        )
    )
