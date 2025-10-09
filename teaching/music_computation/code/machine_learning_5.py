# == k-means clustering of Bach chorales ==

"""
k-means clustering of Bach chorales into modes based on pitch-class
distributions. Original code [here](machine_learning_5.py).
"""

from music21 import corpus
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import os

# ==== Process the chorales ====

def process_chorales():
    """
    Iterates through all Bach chorales, discarding those where the number
    of parts is not 4.

    Collect the pc histogram for each remaining chorale and saves the data
    as 'chorales_pc_counts.npy' using `np.save`.
    """
    chorales_pc_counts = []

    for chorale in corpus.chorales.Iterator():
        # Discard if number of parts is not 4
        if len(chorale.parts) != 4:
            continue
        pcs = get_pcs(chorale)
        tonic_pc = get_tonic_pc(chorale)
        # transpose pcs so that tonic_pc is 0
        pcs = [(pc - tonic_pc) % 12 for pc in pcs]

        # counter for pcs
        counts = np.zeros(12)
        for pc in pcs:
            counts[pc] += 1
        chorales_pc_counts.append(counts)

        # Print progress
        length = len(chorales_pc_counts)
        if length % 10 == 0:
            print(length, 'chorales processed')

    chorales_pc_counts = np.array(chorales_pc_counts)
    # Save the pc counts
    np.save('chorales_pc_counts.npy', chorales_pc_counts)
    return chorales_pc_counts

def get_pcs(s):
    """
    Helper function to get all pcs from a stream. Returns a list of pcs
    (integers mod 12).
    """
    pcs = []
    for n in s.flat.notes:
        if n.isChord:
            for p in n.sortAscending():
                pcs.append(p.pitch.pitchClass)
        else:
            pcs.append(n.pitch.pitchClass)
    return pcs

def get_tonic_pc(s):
    """
    Helper function that returns the pitch class of the last bass note of the
    choral.
    """
    bass = s.parts[-1]
    tonic_note = bass.flat.notes[-1]
    if tonic_note.isChord:
        tonic_note = tonic_note.sortAscending()[0]
    return tonic_note.pitch.pitchClass

# ==== Load the data ====

def load_data():
    """
    Loads 'chorales_pc_counts.npy', which is a list of Bach chorale pitch-
    class counts, using `np.load`. If 'chorales_pc_counts.npy' does not exist,
    calls `process_chorales()` to generate this list.

    Returns a list of Bach chorale pitch-class counts.
    """
    if os.path.isfile('chorales_pc_counts.npy'):       
        return np.load('chorales_pc_counts.npy')
    else:
        return process_chorales()

# ==== Reduce the data to two principal components (dimensions) ====

def reduce_data(data):
    """
    Reduce 12D pc histograms to two principal components.

    Returns the reduced data.
    """
    normalized_data = normalize(data)
    reduced_data = PCA(n_components=2).fit_transform(normalized_data)
    return reduced_data

# ==== Normalize the data ====

def normalize(data):
    """
    Normalize the features in each sample.

    Returns the normalized data.
    """
    rows = []
    for row in data:
        rows.append(row / row.sum())
    return np.array(rows)

# ==== Fit the data ====

def fit_data(data, k=2):
    """
    Fit the data using a kmeans clustering, where k is the number of clusters.

    Returns the fitted kmeans model.
    """
    kmeans = KMeans(init='k-means++', n_clusters=k, n_init=10)
    kmeans.fit(data)

    return kmeans

# ==== Silhouette scores ====

def silhouette(data):
    """
    Plot the silhouette scores for number of clusters ranging from 2 to 6.

    Returns the number of clusters with the max silhouette score.
    """
    scores = []
    for n in range(2, 7):
        kmeans = fit_data(data, k=n)
        pred = kmeans.predict(data)
        scores.append(silhouette_score(data, pred))
    xs = range(2, 7)
    plt.plot(xs, scores)
    plt.xticks(range(2, 7))
    plt.xlabel('number of clusters')
    plt.ylabel('silhouette score')
    plt.show()

    return np.argmax(scores) + 2

# ==== Visualize the data as a Voronoi diagram ====

def visualize_data(data, kmeans):
    """
    Visualization code taken from [here](http://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_digits.html#sphx-glr-auto-examples-cluster-plot-kmeans-digits-py)
    """
    # Step size of the mesh. Decrease to increase the quality of the VQ.
    h = .0002     # point in the mesh [x_min, x_max]x[y_min, y_max].

    # Plot the decision boundary. For that, we will assign a color to each
    excess = 0.1
    x_min, x_max = data[:, 0].min() - excess, data[:, 0].max() + excess
    y_min, y_max = data[:, 1].min() - excess, data[:, 1].max() + excess
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    # Obtain labels for each point in mesh. Use last trained model.
    Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure(1)
    plt.clf()
    plt.imshow(Z, interpolation='nearest',
               extent=(xx.min(), xx.max(), yy.min(), yy.max()),
               cmap=plt.cm.Paired,
               aspect='auto', origin='lower')

    plt.plot(data[:, 0], data[:, 1], 'k.', markersize=2)
    
    # Plot the centroids as a white X
    centroids = kmeans.cluster_centers_
    plt.scatter(centroids[:, 0], centroids[:, 1],
                marker='x', s=169, linewidths=3,
                color='w', zorder=10)
    plt.title('K-means clustering on the pc_distribution of Bach Chorales:\n'
              '(PCA-reduced data) Centroids are marked with white cross')
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.xticks(())
    plt.yticks(())
    plt.show()

# ==== Putting it all together ====

# Load the data
data = load_data()
# Reduce the data
reduced_data = reduce_data(data)
# Find the best number of clusters
best = silhouette(reduced_data)
# Fit the data
kmeans = fit_data(reduced_data, k=best)
# Visualize the data
pred = visualize_data(reduced_data, kmeans)
