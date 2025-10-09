# Music Computation
# Code from September 19, 2017

"""Original code [here](Sep19_2017.py)"""

from music21 import *

# == Assignment thoughts ==

# ==== Be careful using music21 reserved terms like **note**, **pitch**, and **duration** as variable names. ====

# The first line redefines `note` as a music21 note object instead of the
# music21 **note module**, resulting in an error when trying to create new
# note objects.
note = note.Note('e-4') #Don't do this!
print(note)
note2 = note.Note('f4') #This line will result in an error.

# ==== Don't assume that parts always begin at index 1 in the stream hierarchy ====

# In the file for BWV 348, the soprano part is at index 3 in the hierarchy.
# Better is to use the `.parts` property.
sBach = corpus.parse('bach/bwv348.mxl')
print('Elements at the highest level of the sBach stream hierarchy:')
for i, el in enumerate(sBach):
    print('sBach[' + str(i) + '] is ' + str(el))
print()
print('sBach[1] is', sBach[1])
print('sBach[3] is', sBach[3])
print('sBach.parts[0] is', sBach.parts[0])

# ==== Aim for the clearest and most efficient code. ====

# Building a music21 stream note by note by note ...
myStream = stream.Stream()
myStream.append(note.Note('D4', quarterLength=1.5))
myStream.append(note.Note('F4', quarterLength=0.5))
myStream.append(note.Note('A4', quarterLength=1/3))
myStream.append(note.Note('G#4', quarterLength=1/3))
myStream.append(note.Note('A4', quarterLength=1/3))
myStream.append(note.Note('E-4', quarterLength=0.5))
myStream.append(note.Note('E-4', quarterLength=0.5))

# Using lists of pitches and durations
pitches = ['d4', 'f4', 'a4', 'g#4', 'a4', 'e-4', 'e-4']
durations = [3/2, 1/2, 1/3, 1/3, 1/3, 1/2, 1/2]
s = stream.Stream()
# and iterating through list indices
for i in range(len(pitches)):
    s.append(note.Note(pitches[i], quarterLength=durations[i]))
# or iterating through tuples created by the built-in function `zip`.
for p, dur in zip(pitches, durations):
    s.append(note.Note(p, quarterLength=dur))

s.show('text')


# == Accessing music for parsing ==

# Using shortened filenames in the music21 local corpus
path = 'ciconia/quod_jactatur' ##you can omit the file extension
sCiconia = corpus.parse(path)
sCiconia.show('text')
sCiconia.show()

# Getting all paths to a composer in the music21 corpus
paths = corpus.getComposer('Schoenberg')
for path in paths:
    print(path)
    print()
    corpus.parse(path).show('text')
    print()

# Converting a file on the hard drive; note the use of `converter.parse` rather
# than `corpus.parse` for files that are not in the music21 local corpus.
path = '/Users/ccallender/Desktop/waldstein.krn'
sWaldstein = converter.parse(path)
sWaldstein.show()

# Getting a file from a url
url = 'http://kern.ccarh.org/cgi-bin/ksdata?location=users/craig/classical/beethoven/piano/sonata&file=sonata21-1.krn&format=kern'
sWaldstein = converter.parse(url)
sWaldstein.show()

# === Use of the **os** library for navigating file system/directory structure ===

# The `os` library is a basic operating system interface.
# You need to `import` this library for the examples below.
import os

# (In order to run the other blocks of code below you will need to
# download the europa subdirectory of the Essen folksong collection,
# unzip the file, modify the file paths as necessary depending on where
# the folder is installed on your machine.)

# Retrieving all files of a given type in a single directory
dir_name = '/Users/ccallender/Desktop/europa/deutschl/altdeu1/'
file_names = os.listdir(dir_name)
songs = [name for name in file_names if name.endswith('.krn')]
print(len(songs))
for song in songs:
    path = dir_name + song
    sSong = converter.parse(path)
    sSong.show('text')
    print()

# Retrieving all files of a given type in a directory and all its subdirectories
dir_name = '/Users/ccallender/Desktop/europa'
paths = []
for root, dirs, files in os.walk(dir_name):
    for file_name in files:
        if file_name.endswith('.krn'):
            paths.append(os.path.join(root, file_name))
print(len(paths)) #should be 6213, the number of songs in the europa directory

# == Helper functions for recreating "pitch promixity" finding from Huron ch. 5 ==

# helper function to count the frequency of items in a list
def update_count(keyList, count):
    """
    `keyList` is a list of keys; `count` is dictionary.
    
    Returns an updated dictionary in which the value of any key is the
    number of times that key occurs in `keyList` added to the previous value
    for this key in `count`.

    For example:

    `>>> count = {} # count is an empty dictionary`  
    `>>> mylist = [1, 2, 1, 2, 3, 1]`  
    `>>> update_count(mylist, count)`  
    `>>> count`  
    `{1: 3, 2: 2, 3: 1}`
    """
    for key in keyList:
        if key in count:
            count[key] += 1
        else:
            count[key] = 1

# helper function for printing a dictionary with keys sorted
def print_dict(my_dict):
    result = ''
    for key in sorted(my_dict, key=lambda key: key):
        print(str(key) + " : " + str(my_dict[key]))
