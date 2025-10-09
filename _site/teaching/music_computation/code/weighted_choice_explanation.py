"""
[Explanatory code](weighted_choice_explanation.py) for making weighted random
choices.
"""

# Example: selecting from a jar with 2 red, 3 green, and 4 blue marbles.

# Using an explicit list
import random

marbles = ['R'] * 2 + ['G'] * 3 + ['B'] * 4
print(random.choice(marbles))

# What if we only know percentages?
# e.g. 37.524367% red, 23.96853% green, and 61.502897% blue

marbles = ['R'] * 37524367 + ['G'] * 23968530 + ['B'] * 61502897
print('marbles has a length of {}!'.format(len(marbles)))

# If you are running Python 3.6, use the new method `random.choices()`.
marbles = ['R', 'G', 'B']
weights = [37.524367, 23.96853, 61.502897]
print(random.choices(marbles, weights))

# Or use a dictionary where keys are weighted by their values rather than
# having items and their weights in separate lists
m = {'R': 2, 'G': 3, 'B': 4}
m2 = {'R': .37524367, 'G': .23968530, 'B': .61502897}

# `.keys()` and `.values()` are returned in congruent order
print(random.choices(list(m2.keys()), (m2.values())))

# Pre Python 3.6, code your own weighted choice
# Weighted random choice made by a series of `if`-`elif` statements
x = random.randint(1, 9)
print(x)
if 0 < x <= m['R']:
    print('R')
elif m['R'] < x <= m['R'] + m['G']:
    print('G')
elif m['R'] + m['G'] < x <= m['R'] + m['G'] + m['B']:
    print('B')
else:
    print('Problem!')

# Use a loop instead
x = random.randint(1, sum(m.values()))
print(x)
cum_weight = 0
for key in m:
    if cum_weight < x <= m[key] + cum_weight:
        print(key)
        break
    cum_weight += m[key]
else:
    print('Problem')

# Use a function instead
def weighted_choice(weights):
    # for non-integer sum of weights
    # `ValueError: non-integer stop for randrange()`
    x = random.randint(1, sum(weights.values()))
    cum_weight = 0
    for key in weights:
        if cum_weight < x <= weights[key] + cum_weight:
            return key
        cum_weight += weights[key]
    return 'Problem!'

# But what about non-integer weights?
def weighted_choice(weights):
    x = random.random() * sum(weights.values())
    cum_weight = 0
    for key in weights:
        if cum_weight <= x <= weights[key] + cum_weight:
            return key
        cum_weight += weights[key]
    return 'Problem!'
