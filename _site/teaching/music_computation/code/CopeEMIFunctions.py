"""
Functions from Cope's 1992 article in the Computer Music Journal,
"Modeling of Musical Intelligence in EMI" translated into Python. Actual code
is [here](CopeEMIFunctions.py).
"""
motive_size = 2
variance = 1

def allow_var(motive1, motive2):
    """
    Used by `allow-variation`. `motive1` and `motive2` are lists of integers
    representing directed pitch intervals.

    Compares `motive1` with original, inversion, retrograde, and retrograde
    inversion of `motive2`. If the absolute pairwise differences for any of
    these four comparisons are all less than or equal to the `variance`,
    returns `True`; otherwise, returns `False`.
    """
    min_length = min(len(motive1), len(motive2))
    comparisons = [motive2, inversion(motive2), retrograde(motive2),
                   inversion(retrograde(motive2))]
    for comparison in comparisons:
        for i in range(min_length):
            if abs(motive1[i] - comparison[i]) > variance:
                break
        else:
            return True
    return False

def inversion(motive):
    """
    Returns the inversion of `motive`.
    """
    return [-el for el in motive]

def retrograde(motive):
    """
    Returns the retrograde of `motive`.
    """
    return motive[::-1]

def allow_variation(motive, motive_list):
    """
    `motive` is a list of integers representing directed pitch intervals.
    `motive_list` is a list of such motives.

    For each `comparison` in `motive_list`, calls `all_var` to see if
    `comparison` matches `motive`. For successful matches, both `motive`
    and `comparison` are added to `signatures`.

    Returns `signatures`, a list of successful matches.
    """
    signatures = []
    for comparison in motive_list:
        if allow_var(motive, comparison):
            signatures.extend([motive, comparison])
    return signatures

def produce_intervals(work):
    """
    `work` is a list of integers representing pitches.

    Returns a list of intervals.
    """
    return [work[i] - work[i-1] for i in range(1, len(work))]

def break_into_patterns(intervals, size):
    """
    `intervals` is a list of integers. Returns a list of ngrams of `intervals`,
    where n = `size`.
    """
    return [intervals[i:i+size] for i in range(len(intervals)-size+1)]

def match(interval_lists1, interval_lists2):
    """
    Matches patterns for `pattern_match`. Steps through the motives in
    `interval_lists1` for comparisons with `interval_lists2` by calling
    `allow_variation`.
    """
    signatures = []
    for intervals in interval_lists1:
        signatures.extend(allow_variation(intervals, interval_lists2))
    return signatures

def pattern_match(work1, work2):
    """
    `work1` and `work2` are lists of integers representing sequences of pitches.

    Matches the works under analysis after they have been reduced to
    intervals and broken into motives the length of `motive_size`.
    The process used by `break_into_patterns` is thorough in that it finds
    every contiguous pattern of the length prescribed by `motive_size` so
    that, for example, `[1, 2, 3, -4, -5]` becomes
    `[[1, 2, 3], [2, 3, -4], [3, -4, -5]]`. Note that using intervals at
    this stage means that a `motive_size` of two equates to three actual notes.
    """
    intervals1 = break_into_patterns(produce_intervals(work1), motive_size)
    intervals2 = break_into_patterns(produce_intervals(work2), motive_size)
    signatures = match(intervals1, intervals2)
    return signatures

# Example `motive` and `motivelist`
motive = [4, 3]
motivelist = [[0, 0], [0, 0], [0, -4], [-4, -3], [-3, 0]]
print('motive:', motive)
print('motive list:', motivelist)

# Signatures discovered between `motive` and `motivelist` using
# `allow_varation`
print('motive in motive list?', allow_variation(motive, motivelist))
print()


# Example works
work1 = [72, 76, 79, 71, 72, 74, 72]
work2 = [76, 76, 76, 76, 72, 69, 69, 68, 68, 74, 71]
print('work 1 pitches:', work1)
print('work 2 pitches:', work2)

# Signatures derived from comparison of the two works
print('patterns in common:', pattern_match(work1, work2))
