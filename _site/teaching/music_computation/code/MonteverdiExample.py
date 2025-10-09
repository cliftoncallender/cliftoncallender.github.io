"""
Solution to the machine learning problem set.  
(Original code [here](MonteverdiExample.py).)
"""

from music21 import features
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import pickle

# import four different classifiers for comparison
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

# import class for Principal Component Analysis
from sklearn.decomposition import PCA

# import class for selecting the k best features
from sklearn.feature_selection import SelectKBest

# import class for cross validation and scoring
from sklearn.model_selection import cross_val_score

# === Processing madrigals ===

def process_madrigals():
    """
    Create `DataSet`, add features with `addFeatureExtractors`, and parse and
    add streams of Monteverdi madrigals 1-8 from both books three and five.

    Pickle the lists given by `getFeaturesAsList()` and `getAttributeLabels()`
    and return these lists as a tuple.
    """
    books = {}
    # Create DataSet
    ds = features.DataSet(classLabel='Book')
    
    # Create list of `ids` for feature extractors
    ids = ['m' + str(i) for i in range(2, 20) if i not in [3, 4]]
    ids.extend(['p' + str(i) for i in range(1, 17)
                if i not in [5, 6, 11, 16]])
    ids.append('r17')

    # Get feature `extractorsById` and `addFeatureExtractors`
    fes = features.extractorsById(ids)
    ds.addFeatureExtractors(fes)

    # Get paths for madrigals 1-8 in both books three and five
    for book in ['3', '5']:
        prefix = 'monteverdi/madrigal.'
        suffix = '.mxl'
        books[book] = [prefix + book + '.' + str(i) + suffix
                       for i in range(1, 9)]

    # Parse madrigals and add streams to `DataSet` using `addData`
    for book in books:
        for piece in books[book]:
            print('Parsing', piece)
            ds.addData(piece, classValue=book)

    # Process DataSet, name feature values `dataset` and attributes labels
    # `attributes`
    ds.process()
    dataset = ds.getFeaturesAsList()
    attributes = ds.getAttributeLabels()

    # Pickle `dataset` and `attributes`
    pickle.dump(dataset, open('monteverdi_dataset.pkl', 'wb'))
    pickle.dump(attributes, open('monteverdi_attributes.pkl', 'wb'))
    return (dataset, attributes)

# === Loading data ===

def load_data():
    """
    If 'monteverdi_dataset.pkl' exists, unpickle and return tuple of dataset
    and attribute labels.

    Otherwise, call `process_madrigals()` and return the tuple.
    """
    if os.path.isfile('monteverdi_dataset.pkl'):
        return (pickle.load(open('monteverdi_dataset.pkl', 'rb')),
                pickle.load(open('monteverdi_attributes.pkl', 'rb')))
    else:
        return process_madrigals()
    
# === 3D plotting ===

def plot_3D(X, y, title=None):
    """
    Perform a Principal Component Analysis with three components. Fit to and
    transform `X`. Plot the resulting transformed data in 3D with data points
    colored by their labels.
    """
    fig = plt.figure(1, figsize=(8, 6))
    ax = Axes3D(fig, elev=-150, azim=110)
    pca = PCA(n_components=3)
    pca.fit(X)
    X_reduced = pca.transform(X)
    ax.scatter(X_reduced[:, 0], X_reduced[:, 1], X_reduced[:, 2], c=y)
    ax.set_title(title)
    ax.set_xlabel("1st eigenvector")
    ax.w_xaxis.set_ticklabels([])
    ax.set_ylabel("2nd eigenvector")
    ax.w_yaxis.set_ticklabels([])
    ax.set_zlabel("3rd eigenvector")
    ax.w_zaxis.set_ticklabels([])

    plt.show()

# === Test classifiers ===

def test_classifiers(X, y):
    """
    Compare four different classifiers on data `X` and targets `y`.

    Use `cross_val_score` to perform cross validation and score each batch.
    """
    gnb = GaussianNB()
    knn = KNeighborsClassifier()
    svc = SVC()
    dtc = DecisionTreeClassifier()
    classifiers = [gnb, knn, svc, dtc]
    classifier_names = ['GaussianNB', 'KNeighbors', 'SVC', 'Decision Tree']
    for clf, name in zip(classifiers, classifier_names):
        scores = cross_val_score(clf, X, y, cv=8)
        print('Accuracy for {} is {}.'.format(name, np.mean(scores)))

# === Feature reduction ===

def feature_reduction(num_features, X, y, attributes, verbose=True):
    """
    Find the best `num_features` of features for data `X` and targets `y`.
    If `verbose=True`, print features in order from highest to lowest scores.

    Return the reduced feature values.
    """
    select = SelectKBest(k=num_features)
    select.fit(X, y)
    indices = np.argsort(select.scores_)
    if verbose:
        print('\nBest features:')
        for index in indices[::-1]:
            print('feature: {}, score: {}'.format(attributes[index+1],
                                                  select.scores_[index]))
    return X[:, indices[-1:-num_features -1:-1]]

# === Process or load madrigal data ===

def initialize(reload):
    if reload:
        process_madrigals()
    dataset, attributes = load_data()
    data = []
    targets = []
    for obs in dataset:
        data.append(obs[1:-1])
        targets.append(obs[-1])
    return (np.array(data), np.array(targets), attributes)

# === Pulling it all together ====

# Flag whether or not to force reloading and parsing of the madrigals.
reload = False

# Assign `X`, `y`, and `attributes` to data, targets, and attribute labels.
X, y, attributes = initialize(reload)

# 3D plot of data with all features  
# (Image [here](monteverdi1.png).)
plot_3D(X, y, title='PCA, all features')

# Score for classifiers trained on data with all features.  
# `Accuracies based on all features:`  
# `Accuracy for GaussianNB is 0.75.`  
# `Accuracy for KNeighbors is 0.5625.`  
# `Accuracy for SVC is 0.625.`  
# `Accuracy for Decision Tree is 0.5625.`
print('Accuracies based on all features:')
test_classifiers(X, y)

# Determine best features and assign data with only these features to `X_new`.
num_features = 6
X_new = feature_reduction(num_features, X, y, attributes)
#`Best features:`  
#`feature: Relative_Strength_of_Top_Pitch_Classes, score: 9.115085492894748`  
#`feature: Stepwise_Motion, score: 8.90606828647132`  
#`feature: Chromatic_Motion, score: 7.922172419095363`  
#`feature: Amount_of_Arpeggiation, score: 7.74151861513606`  
#`feature: Repeated_Notes, score: 6.978814103596693`  
#`feature: Direction_of_Motion, score: 5.053424575750202`  
#`feature: Melodic_Fifths, score: 3.4287923964333364`  
#`feature: Most_Common_Pitch_Class_Prevalence, score: 3.4206375187543414`  
#`feature: Pitch_Class_Variety, score: 2.7777777777777777`  
#`feature: Primary_Register, score: 2.6155071146418294`  
#`feature: Pitch_Variety, score: 2.5444264943457187`  
#`feature: Most_Common_Pitch_Prevalence, score: 2.287553543524226`  
#`feature: Relative_Strength_of_Top_Pitches, score: 1.5412578570414568`  
#`feature: Number_of_Common_Pitches, score: 1.3358778625954197`  
#`feature: Average_Melodic_Interval, score: 1.1026124301184528`  
#`feature: Melodic_Thirds, score: 1.0747339356403958`  
#`feature: Most_Common_Melodic_Interval_Prevalence, score: 1.0222533224729131`  
#`feature: Number_of_Common_Melodic_Intervals, score: 1.0`  
#`feature: Importance_of_Bass_Register, score: 0.8003018580068948`  
#`feature: Importance_of_High_Register, score: 0.6444487928561894`  
#`feature: Range, score: 0.42748091603053434`  
#`feature: Relative_Strength_of_Most_Common_Intervals, score: 0.41668508666123516`  
#`feature: Average_Note_Duration, score: 0.18684910135877145`  
#`feature: Melodic_Tritones, score: 0.16621202611352615`  
#`feature: Importance_of_Middle_Register, score: 0.009758707453006818`  
#`feature: Size_of_Melodic_Arcs, score: 0.006591088847781841`  
#`feature: Melodic_Octaves, score: 0.0019111831441988583`  
#`feature: Duration_of_Melodic_Arcs, score: 0.0008730810676606502`  

# 3D plot of data with only best features.  
# (Image [here](monteverdi2.png).)
plot_3D(X_new, y, title='PCA, best {} features'.format(num_features))

# Score for classifiers trained on data with only best features.  
#`Accuracies based on best 6 features:`  
#`Accuracy for GaussianNB is 0.8125.`  
#`Accuracy for KNeighbors is 0.75.`  
#`Accuracy for SVC is 0.875.`  
#`Accuracy for Decision Tree is 0.625.`
print('\nAccuracies based on best', num_features, 'features:')
test_classifiers(X_new, y)
