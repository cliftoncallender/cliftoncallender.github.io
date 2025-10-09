# == Greatly simplified version of Temperley's meter-finding model ==

from music21 import converter

# Upper-level beats
U = 0.95

# Tactus
T = 0.74

# Lower-level beats
L = 0.38

# dictionary of meter: (name, prior probability)
meters = {(U, L, T, L): ('simple duple', 0.76 * 0.78),
          (U, L, T, L, T, L): ('simple triple', 0.24 * 0.78),
          (U, L, L, T, L, L): ('compound duple', 0.76 * 0.22)}

# Test rhythms given explicitly
rhythm1 = [1, 0, 0, 1, 1, 0, 1, 0]
rhythm2 = [0, 1, 0, 0, 1, 1, 0, 1]
rhythm3 = [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0,
          1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
rhythm4 = [1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0]

# Test rhythm derived from folksong
url = 'http://kern.humdrum.org/cgi-bin/ksdata?file=magyar28.krn&l=' \
      'essen/europa/magyar&format=kern'
song = converter.parse(url).flat.notes
total_duration = song.highestOffset + song[-1].quarterLength
rhythm5 = [0] * int(total_duration) * 2
for n in song:
    rhythm5[int(n.offset * 2)] = 1

def meter_prob(meter, rhythm, offset, prior_prob=1):
    """Given a `meter` (in the dictionary `meters`), `offset`, and
    prior probability (`prior_prob`) of the meter, return probability of the
    `rhythm`.
    """
    total_prob = 1
    for i, pulse in enumerate(rhythm):
        prob = meter[(i + offset) % len(meter)]
        if not pulse:
            prob = 1 - prob
        total_prob *= prob
    return total_prob * prior_prob

# Test model against all meters given above in all possible offsets
rhythm = rhythm5 # try all six of the meters defined above
for meter in meters:
    for offset in range(len(meter)):
        print(meters[meter][0], 'offset= ', offset)
        print(meter_prob(meter, rhythm, offset, prior_prob=meters[meter][1]))
        print()

"""
Highest probabilities for the rhythms defined are:  
`rhythm1`: simple duple, offset = 0  
`rhythm2`: simple duple, offset = 3  
`rhythm3`: simple triple, offset = 0  
`rhythm4`: tied between simple duple, offset = 3 and compound duple, offset =
2 or 5  
`rhythm5`: simple triple, offset = 5
"""
