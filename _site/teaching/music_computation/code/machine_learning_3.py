# === Cross validation in sklearn ===

"""
(See original code [here](machine_learning_3.py).)
"""

import numpy as np
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier

iris = datasets.load_iris()
X = iris.data
y = iris.target

knn = KNeighborsClassifier()

# ==== Leave-one-out validation ====

from sklearn.model_selection import LeaveOneOut
# Instatiate `LeaveOneOut` class. See [here](http://scikit-learn.org/stable/modules/cross_validation.html#leave-one-out-loo)
# and [here](http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.LeaveOneOut.html#sklearn.model_selection.LeaveOneOut)
# for more details.
loo = LeaveOneOut()
# Keep track of successful predictions
successes = []

# the `split` method generates indices to split data into training and test set.
for train_index, test_index in loo.split(X):
    # `fit` classifier on training indices
    knn.fit(X[train_index], y[train_index])
    # `score` classifier on testing indices; since there will be only one
    # test index, the score will be either 1 (for a correct prediction) or
    # 0 (for an incorrect prediction).
    successes.append(knn.score(X[test_index], y[test_index]))
# Divide `successes` by the sample size to get the percentage score.
print("Accuracy for iris dataset with Leave-One-Out validation is {}.\n".
      format(np.mean(successes)))

# ==== Random permutation cross validation ====

from sklearn.model_selection import ShuffleSplit
# Instantiate ShuffleSplit class with `n_splits` (number of repetitions) and
# `test_size` (percentage of dataset to withhold for the test data). See
# [here](http://scikit-learn.org/stable/modules/cross_validation.html#k-fold)
# and [here](http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.KFold.html#sklearn.model_selection.KFold)
# for more details.
ss = ShuffleSplit(n_splits=5, test_size=0.25)

successes = []
for train_index, test_index in ss.split(X):
    knn.fit(X[train_index], y[train_index])
    successes.append(knn.score(X[test_index], y[test_index]))
print("Accuracy for iris dataset with Random Permutation cross validation " \
      "is {}.\n".format(np.mean(successes)))

# ==== K-folds cross validation ====

from sklearn.model_selection import KFold
# Instantiate KFold class with `n_splits`  
# Provides train/test indices to split data in train/test sets. Split dataset
# into k consecutive folds (without shuffling by default).  
# Each fold is then used once as a validation while the k - 1 remaining folds
# form the training set.
# If `n_splits` equals the sample size, this is equivalent to the Leave-one-out
# Validation.  
# See [here](http://scikit-learn.org/stable/modules/cross_validation.html#random-permutations-cross-validation-a-k-a-shuffle-split)
# and [here](http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.ShuffleSplit.html#sklearn.model_selection.ShuffleSplit)
# for more details.
kf = KFold(n_splits=5)

successes = []
for train_index, test_index in ss.split(X):
    knn.fit(X[train_index], y[train_index])
    successes.append(knn.score(X[test_index], y[test_index]))
print("Accuracy for iris dataset with K-folds cross validation " \
      "is {}.\n".format(np.mean(successes)))

# ==== Evaluate a score directly by cross-validation ====

from sklearn.model_selection import cross_val_score
# `cross_val_score` takes an estimator (in this case the `knn` classifier),
# data, targets, and `cv` (in this case, the number of folds). See
# [here](http://scikit-learn.org/stable/modules/cross_validation.html#computing-cross-validated-metrics)
# and [here](http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_val_score.html#sklearn.model_selection.cross_val_score)
# for more details.
scores = cross_val_score(knn, X, y, cv=10)
print("Scores for each run of the cross validation:\n", scores)
print("Average score for all runs of the cross validation is {}."
      .format(np.mean(scores)))
