"""
You can see the actual code file [here](markov_music_generator.py).
"""

# == music generations with Markov chains ==
import random
from music21 import corpus, stream, note

# ==== Find ngrams from a given list ====
def get_ngrams(seq, n):
    """
    Given a list `seq` returns a list of `ngrams` where each element is
    an n-tuple.

    Example:  
    `>>> seq = [1, 2, 1, 3, 1, 2, 7]`  
    `>>> find_ngrams(seq, 2)`  
    `[(1, 2), (2, 1), (1, 3), (3, 1), (1, 2), (2, 7)]`  
    `>>> find_ngrams(seq, 3)`  
    `[(1, 2, 1), (2, 1, 3), (1, 3, 1), (3, 1, 2), (1, 2, 7)]`  
    """
    ngrams = []
    # Iterate over `seq` in n-sized slices each converted to
    #an n-tuple and appended to `ngrams`.
    for i in range(len(seq) - n + 1):
        new_tuple = tuple(seq[i:i+n])
        ngrams.append(new_tuple)
    return ngrams

# ==== Create Markov model from a given list ====

def markov_model(seq, order):
    """
    Given a list `seq` returns a Markov model of the given `order`
    as a dictionary. The keys are `order`-sized tuples. The value for each
    key is a list of elements in `seq` that immediately follow
    occurances of the key in the `seq`.

    Example:  
    `>>> seq = [1, 2, 1, 3, 1, 2, 7]`  
    `>>> markov_model(seq, 1)`  
    `{(2,): [1, 7], (3,): [1], (1,): [2, 3, 2]}`  
    `>>> markov_model(seq, 2)`  
    `{(1, 2): [1, 7], (1, 3): [1], (3, 1): [2], (2, 1): [3]}`  
    """
    markov = {}
    # First use `find_ngrams` to slice `seq` appropriately.
    ngrams = get_ngrams(seq, order+1)
    # For each `ngram` in `ngrams` (where n = `order` + 1) the first
    # (n - 1) elements are used as the key and the last
    # element is appended to the list of possible
    # continuations.
    for ngram in ngrams:
        try:
            markov[ngram[:-1]].append(ngram[-1])
        except KeyError:
            markov[ngram[:-1]] = [ngram[-1]]
    return markov

# ==== Generate Markov chain ====

def markov_chain(markov, order, max_length=20):
    """
    Given a list `seq` returns a Markov chain of
    the given `order` with a maximum length of the integer `max_length`.
    """

    # The `start_state` for the Markov chain is chosen randomly from a list
    # of `keys()` in the `markov` dictionary.
    start_state = random.choice(list(markov.keys()))

    # Markov `chain` is a list beginning with the `start_state`.
    chain = list(start_state)

    #`while` loop to generate markov `chain`.
    while True:
        # Choose a random continuation, `next_state` from the elements of
        # the value for the current `start_state`.
        next_state = random.choice(markov[start_state])
        chain.append(next_state)
        if len(chain) >= max_length:
            break
        # Concatenate `next_state` to `start_state` and use the appropriate
        # slice of the resulting tuple as the new `start_state`.
        start_state = (start_state + (next_state,))[1:]
    return chain

# create empty dictionary for Markov model
markov = {}

# set `order` of the Markov model; experiment with changing the `order`
order = 2

sourceMaterial = corpus.parse('bach/bwv7.7')
for part in sourceMaterial.parts:
        notes = part.flat.notes
        # Use tuples of note pitches and duration to create Markov model
        note_tuples = [(n.nameWithOctave, n.quarterLength) for n in notes]
        markov.update(markov_model(note_tuples, order))
chain = markov_chain(markov, order)

output = stream.Stream()
# Convert chain of (pitch, duration) tuples to music21 note objects
# and append to `output` stream.
for ptch, dur in chain:
    output.append(note.Note(ptch, quarterLength=dur))
output.show()
