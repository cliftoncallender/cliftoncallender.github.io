## Feature extraction in music21

"""
Examples taken/adapted from "[Feature Extraction and Machine Learning of
Symbolic Music Using the music21 Toolkit](http://ismir2011.ismir.net/papers/PS3-6.pdf)"
Get original code [here](machine_learning_4.py).
"""

from music21 import converter, features
import numpy as np

# ==== Example 1 ====

"""
Handel's Messiah, movement 3-05  
Feature extracted: Direction of Motion
"""

url = 'Messiah_-_Handel_-_3.50_O_death_where_is_thy_sting.mxl'
handel = converter.parse(url)

# "The features implemented in `features.jSymbolic` are based on those found
# in jSymbolic and defined in Cory McKay’s MA Thesis, 'Automatic Genre
# Classification of MIDI Recordings.' The LGPL jSymbolic system can be found
# [here](http://jmir.sourceforge.net/jSymbolic.html)."

# "`DirectionOfMotionFeature` returns the fraction of melodic intervals that
# are rising rather than falling. Unisons are omitted."
fe = features.jSymbolic.DirectionOfMotionFeature(handel)

# Extracts the `DirectionOfMotionFeature` from `handel`.
feature = fe.extract()

# Features are extracted as vectors, thus the need for the index to report a
# feature as a single value rather than a list (or array):  
# `Percentage of melodic motion that is ascending: 0.55`
print('Percentage of melodic motion that is ascending:',
      feature.vector[0])

# ==== Example 2 ====

"""
Two movements from Handel's Messiah  
Feature extracted: Triple meter (1 = True, 0 = False)
"""

# Handel's Messiah, movement 3-04
handel2 = converter.parse("http://www.musedata.org/cgi-bin/mddata?" \
                          "composer=handel&edition=chry&genre=&work=" \
                          "messiah&format=kern&movement=3-04")
fe = features.jSymbolic.TripleMeterFeature(handel2)
# Movement 3-04 is in triple meter:  
# `Triple Meter Feature Vector for Handel movement 3-04: 1`
print('Triple Meter Feature Vector for Handel movement 3-04:',
      fe.extract().vector[0])

# Handel's Messiah, movement 3-05
handel = converter.parse('http://www.musedata.org/cgi-bin/mddata?' \
                         'composer=handel&edition=chry&genre=&work=' \
                         'messiah&format=kern&movement=3-05')
fe = features.jSymbolic.TripleMeterFeature(handel)
# Movement 3-05 is not in triple meter:  
# `Triple Meter Feature Vector for Handel movement 3-05: 0`
print('Triple Meter Feature Vector for Handel movement 3-05:',
      fe.extract().vector[0])

# ==== Example 3 ====

"""
Feature extraction by ID
"""

# M10 Chromatic Motion: Fraction of melodic intervals that correspond
# to a semitone.  
# M12 Melodic Thirds: Fraction of melodic intervals that are major or
# minor thirds.  
# M13 Melodic Fifths: Fraction of melodic intervals that are perfect fifths.
fes = features.extractorsById(['M10','M12','M13'])
# `fes` is a list of `music21.features.jSymbolic` subclasses:  
# `<class 'music21.features.jSymbolic.ChromaticMotionFeature'>`  
# `<class 'music21.features.jSymbolic.MelodicThirdsFeature'>`  
# `<class 'music21.features.jSymbolic.MelodicFifthsFeature'>`
for feature in fes:
    print(feature)


# ==== Example 4 ====


"""
Using music21's DataSet class, which combines a set of features and a
collection of data from which to extract the features. See the
[documentation](http://web.mit.edu/music21/doc/moduleReference/moduleFeaturesBase.html#dataset) 
for details.
"""

# Create a new `DataSet`. `classLabel` is string describing the labels for
# data added to the dataset.
ds = features.DataSet(classLabel='Composer')
fes = features.extractorsById(['M10','M12','M13'])
ds.addFeatureExtractors(fes)

# Add streams to the dataset using the `addData` method.

# Bach, Art of Fugue 7, mm. 1 - 50
art_of_fugue_7 = 'http://www.musedata.org/cgi-bin/mddata?composer=' \
                 'bach&edition=bg&genre=canon&work=1080&format=' \
                 'kern&movement=07'
b1 = converter.parse(art_of_fugue_7).measures(0, 50)
# Add stream with `classValue` 1 (for Bach) and `id` Art of Fugue
ds.addData(b1, classValue=1, id='Art of Fugue')

# Add stream with `classValue` 1 and `id` BWV 66.6
ds.addData('bwv66.6.xml', classValue=1, id='BWV 66.6')

# Handel, Messiah, movement 3-5
url = 'http://www.musedata.org/cgi-bin/mddata?composer=handel&' \
      'edition=chry&genre=&work=messiah&format=kern&movement=3-05'
handel_messiah_3_05 = converter.parse(url)
# Add stream with `classValue` 2 (for Handel) and `id` Messiah
ds.addData(handel_messiah_3_05, classValue=2, id='Messiah')

# Add stream with `classValue` 2 and `id` mystery Handel
url = 'http://www.midiworld.com/midis/other/handel/gfh-jm01.mid'
handel_mystery = converter.parse(url)
ds.addData(handel_mystery, classValue=2, id='mystery Handel')

# The `process` method processes "all Data with all FeatureExtractors."
ds.process()

# `getAttributeLabels` returns a list of attribute labels:  
# `Attribue labels: ['Identifier', 'Chromatic_Motion', 'Melodic_Thirds', 'Melodic_Fifths', 'Composer']`
print('Attribue labels:', ds.getAttributeLabels(), "\n")
# `getFeaturesAsList` returns a list of attribute values for all streams added
# to the `DataSet`:  
# `Features for work: ['Art_of_Fugue', 0.33980582524271846, 0.049352750809061485, 0.040453074433656956, 1]`  
# `Features for work: ['bwv66.6.xml', 0.22012578616352202, 0.11320754716981132, 0.05660377358490566, 1]`  
# `Features for work: ['Messiah', 0.06896551724137931, 0.1724137931034483, 0.0, 2]`  
# `Features for work: ['mystery_Handel', 0.18497576736672053, 0.1583198707592892, 0.03877221324717286, 2]`
for work in ds.getFeaturesAsList():
    print('Features for work:', work)
    print()

# Access identifiers, features values, and labels with the appropriate indices
# for `getFeaturesAsList`:  
dataset = np.array(ds.getFeaturesAsList())
# `>>> identifiers`  
# `array(['Art_of_Fugue', 'bwv66.6.xml', 'Messiah', 'mystery_Handel'],`  
# `      dtype='<U20')`  
identifiers = dataset[:, 0]
# `>>> data`  
# `array([['0.33980582524271846', '0.049352750809061485',`  
# `        '0.040453074433656956'],`  
# `       ['0.22012578616352202', '0.11320754716981132', '0.05660377358490566'],`  
# `       ['0.06896551724137931', '0.1724137931034483', '0.0'],`  
# `       ['0.18497576736672053', '0.1583198707592892', '0.03877221324717286']],`  
# `      dtype='<U20')`
data = dataset[:, 1:4]
# `>>> targets`  
# `array(['1', '1', '2', '2'],`  
# `      dtype='<U20')`
targets = dataset[:, 4]
