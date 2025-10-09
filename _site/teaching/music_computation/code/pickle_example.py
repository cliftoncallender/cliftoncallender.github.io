## Using `pickle`

"""
“Pickling” is the process whereby a Python object hierarchy is converted into
a byte stream, and “unpickling” is the inverse operation, whereby a byte
stream (from a binary file or bytes-like object) is converted back into an
object hierarchy. See the
[documentation ](https://docs.python.org/3/library/pickle.html) for more
details. (Original code [here](pickle_example.py).)
"""

from music21 import *
import time
import pickle

# === Simple example ===

favorite_works = {'Parker':'Anthropology',
                  'Saariaho':'Amers',
                  'Bach':'Musical Offering'}

# Use the `dump` method to write a pickled representation of the object
# `favorite_works` to the file object with path 'favorites.pkl'. The file
# is opened in mode 'wb', which that file is opened for writing in binary mode.
pickle.dump( favorite_works, open('favorites.pkl', 'wb'))
# `Savedlist -- {'Parker': 'Anthropology', 'Saariaho': 'Amers', 'Bach': 'Musical Offering'}`
print("Savedlist --", favorite_works)

# Use the `load` method to read a pickled object representation from the file
# object with path 'favorites.pkl' and return the reconstituted object hierarchy
# specified therein.
retrieved_favorites = pickle.load( open("favorites.pkl", "rb"))
# `Retrieved list -- {'Parker': 'Anthropology', 'Saariaho': 'Amers', 'Bach': 'Musical Offering'}`
print("Retrieved list --", retrieved_favorites)

# === Parsing and pickling folksongs ===

# ==== Parse folksongs from the music21 corpus ====

# ``time.time()` returns the time in seconds since the epoch (an arbitrary
# reference time) as a floating point number.
start = time.time()

# Parsing songs from 'han' and 'boehme' opuses
oChina = corpus.parse('essenFolksong/han1')
print('han1 loaded')
oCEurope = corpus.parse('essenFolksong/boehme10')
print('boehme10 loaded')

end = time.time()

# timing stats
interval = round(end - start)
# On my computer, parsing takes 8 seconds.
print("Parsing took", interval, "seconds.\n")


# ==== Create list of features with ids p1 - p8 and r31 - r35 ====
featureList = ['p' + str(i) for i in range(1, 9)]
featureList.extend(['r' + str(i) for i in range(31, 36)])
# Get feature extractors using this list of ids
featureExtractors = features.extractorsById(featureList)

# ==== Create DataSet ====
start = time.time()

# Instantiate `DataSet`
ds = features.DataSet(classLabel='Region')
# Add `featureExtractors`
ds.addFeatureExtractors(featureExtractors)
# `addData` for each stream in the oChina and oCEurope opuses
for w in oChina.scores:
    wID = 'essenFolkson/%s-%s' % ('han1', w.metadata.number)
    ds.addData(w, classValue='China', id=wID)
print('han1 scores added to training data set')

for w in oCEurope.scores:
    wID = 'essenFolksong/%s-%s' % ('europe1', w.metadata.number)
    ds.addData(w, classValue='CentralEurope', id=wID)
print('boehme10 added to training data set')

# Process data and feature extractors
ds.process()
# On my computer, processing the `DataSet` takes 76 seconds.
print('dataset processed')

# timing stats
end = time.time()
interval = round(end - start)
print("Feature extraction took", interval, "seconds.\n")

# ==== Pickle and unpickle the `DataSet` ====
start = time.time()

# Save the `DataSet` by pickling the output of `getFeaturesAsList()`
path = 'folkSongExample.pkl'
pickle.dump(ds.getFeaturesAsList(), open(path, 'wb'))
print('dataset written as a pickled file')

# ==== 'Unpickle' and load dataset ====
start = time.time()

# Load the datset
path = 'folkSongExample.pkl'
dataset = pickle.load(open(path, 'rb'))
