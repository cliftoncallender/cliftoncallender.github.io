"""
[Example code](hmm_example.py) for Hidden Markov Model (HMM).
Specific example and some code taken from
[Wikipedia](https://en.wikipedia.org/wiki/Hidden_Markov_model#A_concrete_example).
This code is limited to generating hidden states and their corresponding
emissions. We'll return to the more interesting and advanced questions of
finding the most likely hidden states, parameters, and likely number of hidden
states on the basis of a given observable sequence 
"""

import random

# Make a random selection from a dictionary with weighted keys
def weighted_choice(transitions):
    prob = random.random()

    for state, value in transitions.items():
        if prob <= value:
            return state
        else:
            prob -= value
    return None

# Generate sequence of hidden states
def generate_states(states, start_probability, transition_probability, length):
    start_state = weighted_choice(start_probability)
    chain = [start_state]
    for i in range(1, length):
        next_state = weighted_choice(transition_probability[start_state])
        chain.append(next_state)
        start_state = next_state
    return chain

# Generate sequence of emissions based on the sequence of hidden states.
def generate_emissions(state_sequence, emission_probability):
    emissions = []
    for state in sequence:
        emission = weighted_choice(emission_probability[state])
        emissions.append(emission)
    return emissions

# Tuples of (hidden) states and observations
states = ('Rainy', 'Sunny')
observations = ('walk', 'shop', 'clean')

# Dictionaries of start probabilities. Keys are states and values are their
# respective probabilities.
start_probability = {'Rainy': 0.6, 'Sunny': 0.4}

# Dictionaries of transition and emission probabilities with states
# as keys.
# Values of these keys are *another* dictionary with possible next states or
# emissions as keys and their respective transition probabilities as values.

transition_probability = {
   'Rainy' : {'Rainy': 0.7, 'Sunny': 0.3},
   'Sunny' : {'Rainy': 0.4, 'Sunny': 0.6},
   }
 
emission_probability = {
   'Rainy' : {'walk': 0.1, 'shop': 0.4, 'clean': 0.5},
   'Sunny' : {'walk': 0.6, 'shop': 0.3, 'clean': 0.1},
   }

# Generate sequence of hidden states.
sequence = generate_states(states, start_probability,
                           transition_probability, 10)
print('Sequence of hidden states:', sequence, '\n')

# Generate sequence of emissions based on the sequence of hidden states.
emissions = generate_emissions(sequence, emission_probability)
print('Observed emissions:', emissions)
