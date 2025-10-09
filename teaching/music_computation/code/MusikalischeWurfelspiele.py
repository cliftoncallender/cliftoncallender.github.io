"""
You can see the actual code file [here](MusikalischeWurfelspiele.py).
"""

from music21 import converter, stream, clef, meter, bar
import random

def init():
    """
    init function to parse MusikalischeWurfelspiele.xml and split
    the single stream of 176 measures into 176 streams each of one measure.
    """
    # parse Musikalische Wurfelspiele score
    s = converter.parse('MusikalischeWurfelspiele.xml')

    # split score into measures
    measures = [stream.Stream() for i in range(176)]
    for part in s.parts:
        for i, this_measure in enumerate(part.getElementsByClass('Measure')):
            measures[i].insert(0, this_measure.notesAndRests.stream())

    # chance table--each row corresponds to the option for a single measure
    # in the output
    table = [[96, 32, 69, 40, 148, 104, 152, 119, 98, 3, 54],
             [22, 6, 95, 17, 74, 157, 60, 84, 142, 87, 130],
             [141, 128, 158, 113, 163, 27, 171, 114, 42, 165, 10],
             [41, 63, 13, 85, 45, 167, 53, 50, 156, 61, 103],
             [105, 146, 153, 161, 80, 154, 99, 140, 75, 135, 28],
             [122, 46, 55, 2, 97, 68, 133, 86, 129, 47, 37],
             [11, 134, 110, 159, 36, 118, 21, 169, 62, 147, 106],
             [30, 81, 24, 100, 107, 91, 127, 94, 123, 33, 5],
             [70, 117, 66, 90, 25, 138, 16, 120, 65, 102, 35],
             [121, 39, 139, 176, 143, 71, 155, 88, 77, 4, 20],
             [26, 126, 15, 7, 64, 150, 57, 48, 19, 31, 108],
             [9, 56, 132, 34, 125, 29, 175, 166, 82, 164, 92],
             [112, 174, 73, 67, 76, 101, 43, 51, 137, 144, 12],
             [49, 18, 58, 160, 136, 162, 168, 115, 38, 59, 124],
             [109, 116, 145, 52, 1, 23, 89, 72, 149, 173, 44],
             [14, 83, 79, 170, 93, 151, 172, 111, 8, 78, 131]]
    
    return (measures, table)

def generate_selections(table):
    """
    Make a random choice from each of the 16 rows of the chance `table`.
    """
    selections = []
    for row in table:
        index = random.randint(0, 5) + random.randint(0, 5)
        selections.append(row[index])
    return selections

def create_waltz(measures, selections):
    """
    `measures` is a list of 176 streams of a single measure each. `selections`
    is a list corresponding to 16 of the 176 measure streams.

    Returns `out`, which is a stream consisting of the 16 selected measures.
    """
    # use selections to create output
    out = stream.Stream()
    for i in range(2):
        p = stream.Part()
        for selection in selections:
            p.append(measures[selection - 1][i])
        out.insert(0, p)
    return out

def add_clefs_and_timesignatures(s):
    """
    Add clefs and time signatures to the waltz (`s`).
    """
    s[0][0].insert(0, clef.TrebleClef())
    s[1][0].insert(0, clef.BassClef())
    for i in range(2):
        s[i][0].insert(0, meter.TimeSignature('3/8'))
        
def add_repeats(s):
    """
    Add repeat signs to the waltz (`s`).
    """
    for i in range(2):
        for m in [0, 8]:
            s[i][m].leftBarline = bar.Repeat(direction='start')
        for m in [7, 15]:
            s[i][m].rightBarline = bar.Repeat(direction='end')

def play_the_game(measures, table, show=True):
    """
    Generate a new Waltz based on Mozart's "Musikalische Wurfelspiele".
    `measures` is a list of 176 streams of a single measure each. `table` is
    a matrix for the possible selection for each measure of the resulting
    16-bar waltz.
    """
    selections = generate_selections(table)
    waltz = create_waltz(measures, selections)
    add_clefs_and_timesignatures(waltz)
    add_repeats(waltz)
    if show == True:
        waltz.show()
    return waltz

def options_by_measures(measures, table, show=True):
    """
    Sorts the possible measures by their location in the resulting waltz into
    a single music21 stream; e.g. the eleven possible first bars are
    bars 1 - 11 in the output stream, the eleven possible second bars are bars
    12 - 22 in the output stream, and so forth.
    """
    collated_measures = [cell for row in table for cell in row]
    measures_options = create_waltz(measures, collated_measures)
    add_clefs_and_timesignatures(measures_options)
    if show == True:
        measures_options.show()
    return measures_options

# split the instructions into individual measures and grab the chance table
measures, table = init()

## play the game!
play_the_game(measures, table)

## collect options for each measure of the waltz
options_by_measures(measures, table)
