# Music Computation
# Code from September 21, 2017

"""Original code [here](Sep21_2017.py)"""

# == Import Statements ==

# This line import **all** of the names and functions in the `os` library,
# including the functions `walk()` and `path.join()` used below.
# To refer to these names and functions, we must prefix the library name
# `os`; thus, `os.walk()` and `os.path.join()`.
import os

# This line imports **only** the name `Counter`, which is a function in the
# `collections` library. Since we are importing the name `Counter`
# directly, we do not need to prefix `collections`. (In fact, we are not
# importing the entire library, so using the name `collections` would
# produce an error.)
from collections import Counter

# This line is similar to that immediately above except for the use of "*".
# The asterisk is a wildcard character indicating that we are directly importing
# **all** names and functions associated with the `music21` library. Thus, we
# use (for example) `note.Note()` rather than `music21.note.Note()`.
from music21 import *

# == Counter

# A `Counter` is a container that keeps track of how many times equivalent
# items are added. (Thus it is essentially a multiset.) `Counter` is much more
# convenient than using a dictionary to count frequencies of items. For a
# tutorial on `Counter` see https://pymotw.com/2/collections/counter.html or
# see https://docs.python.org/2/library/collections.html#collections.Counter
# for the reference document.

# Here we create two seperate lists.
list1 = ['a', 'b', 'c', 'a', 'b', 'b']
list2 = ['b', 'c', 'd', 'd', 'b', 'b']

# Create a `Counter` of `list1` and assign to `count`.
count += Counter(list1)

# Output: `Counter({'b': 3, 'a': 2, 'c': 1})`
print(count)

# Create a `Counter` of `list2`, add to `count`, and then assign the result
# to `count`.
count += Counter(list2)

# Output: `Counter({'b': 6, 'd': 2, 'a': 2, 'c': 2})`
print(count)

# == Testing pitch proximity

# My code uses two functions:

# ==== Converting all files belonging to a given directory and its subdirectories to a music21 stream (if possible) ====

def all_streams(dir_name):
    """
    `dir_name` is a string corresonding to a directory name

    returns a list of streams for all files in `dir_name` and its subdirectories
    that can be parsed by music21
    """
    my_streams = []
    for root, dirs, files in os.walk(dir_name):
        for file_name in files:
            path = os.path.join(root, file_name)
            # `try` to execute the following block of code.
            # If an error is encountered, a `try` block code execution is
            # stopped and transferred down to the `except` block.
            # If not error is encountered, the `try` block code is successfully
            # executed.
            try:
                my_streams.append(converter.parse(path))
                number_completed += 1
            # the `except` block code is executed if an error occurs in the
            # `try` block
            except:
                # here we use the reserve word `pass` to indicate that there
                # are no statements to execute. (We simply want to ignore files
                # that can't be parsed by **music21**.)
                pass
    return my_streams
# ==== Returning a list of intervals from a stream consisting of a single line of pitches ====
def melody_to_intervals(my_stream, directed=False):
    """
    `my_stream` is a music21 stream assumed to be a single-line melody

    returns a list of intervals between successive pitches
    If `directed=True`, the intervals are directed. Otherwise, the intervals
    are undirected. If `melody_to_intervals` is called with a single parameter,
    then `directed` is set to `False` by default.
    """
    intervals = []
    flat_stream = my_stream.flat.notes
    for i in range(len(flat_stream) - 1):
        # `interval.Interval` is a music21 class for handling intervals.
        # See http://web.mit.edu/music21/doc/moduleReference/
        # moduleInterval.html#interval.
        interval_type = interval.Interval(flat_stream[i], flat_stream[i+1])
        # `.semitones` is a property of the `interval.Interval` class that
        # yields the interval in directed semitones
        current_interval = interval_type.semitones
        # If `directed` is False (meaning you want undirected intervals),
        # then take the absolute (`abs`) value.
        if not directed:
            current_interval = abs(current_interval)
        intervals.append(current_interval)
    return intervals

# ==== Pulling it all together ====
dir_name = '/Users/ccallender/Desktop/europa/deutschl/altdeu2/'

# Convert all songs in the altdeu1 dir to music21 streams.
my_streams = all_streams(dir_name)

# Create an empty `Counter`.
count = Counter()

# Update counts of intervals for every stream in `myStreams`.
for s in my_streams:
    count += Counter(melody_to_intervals(s))

# ==== Display absolute counts of intervals.
print('Absolute counts of intervals')
for key in count:
    print(key, 'semitone(s):', count[key])

# Print a blank line.
print()

# ==== Display normalized counts of intervals.

# `.values` returns a list of the values in a `Counter` or dictionary.
# `sum` returns the sum of all values in a list, tuple, or set.
total_count = sum(count.values())
for interval in count:
    # `round` is a built-in Python function.
    # `round(value, decimals)` will round `value` to the specified number
    # of `decimals`.
    percent = round(100 * count[interval] / total_count, 2)
    print(interval, 'semitone(s):', percent)
