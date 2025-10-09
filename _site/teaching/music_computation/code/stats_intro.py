# == Simulation and basis statistics in Python ==

# Original code [here](stats_intro.py).

import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
# Import [secret.py](secret.py) which contains the `success_rate`
# for instiating `FlipSim` in the examples below
import secret
import scipy.stats as stats

# === Simulation of Bernoulli trials ===

class FlipSim(object):
    """Class for simulating Bernoulli trials"""
    def __init__(self, success_rate):
        self.success_rate = success_rate
        self.trials = []

    def get_success_rate(self):
        return self.success_rate

    def flip(self):
        """Returns the result of a single 'flip'"""
        if random.random() <= self.success_rate:
            return True
        else:
            return False

    def flips(self, num_flips):
        """Returns a list of a single trial of `num_flips` flips"""
        return [self.flip() for i in range(num_flips)]

    def flip_trials(self, flips_per_trial, num_trials):
        """Returns a list of `num_trials` trials of `flips_per_trials` each"""
        self.trials = [self.flips(flips_per_trial) for i in range(num_trials)]
        return self.trials

# === Is it fair or loaded simulated coin? ===

sim = FlipSim(secret.value)
# 10,000 trials of 1,000 flips each. Experiment with different combinations
# of `flips_per_trial` and `num_trials`.
trials = sim.flip_trials(1000, 10000)

# Descriptive stats
means = [np.mean(trial) for trial in trials]
mean = np.mean(means)
sigma = np.std(means)

# Results should be similar to:  
# `The mean is 0.5300304`  
# `The standard deviation is 0.0157946977128`  

print('The mean is', mean)
print('The standard deviation is', sigma)

# `68% of the values lie between 0.514235702287 and 0.545825097713`  
# `95% of the values lie between 0.498441004574 and 0.561619795426`  
# `99.7% of the values lie between 0.482646306861 and 0.577414493139`
# Thus, on the basis of this particular simulation we can say with 95%
# confidence that `secret.value` lies between 0.498 and 0.562.

print('68% of the values lie between', mean - sigma, 'and', mean + sigma)
print('95% of the values lie between', mean - 2*sigma, 'and', mean + 2*sigma)
print('99.7% of the values lie between', mean - 3*sigma, 'and', mean + 3*sigma)

# === Plot the simulation ===

# `numpy.linspace` returns evenly spaced numbers over a specified interval.
# In this case the range of x is defined by the mean plus/minus three
# standard deviations.
x = np.linspace(mean - 3 * sigma, mean + 3 * sigma, 100)
# Create a histogram of the means
plt.hist(means, bins = 200)
# Draw the _probability distribution function_ (pdf) of the normal distribuation
# with mean `secret.value` and standard deviation of `sigma` within the range
# of `x`.
plt.plot(x, 10 * mlab.normpdf(x, secret.value, sigma))
# Show the plot
plt.show()

# === Using `scipy.stats` ===

# Create three different Bernoulli trials of 1,000 flips each with different
# success rates
x1 = FlipSim(0.5).flips(1000)
x2 = FlipSim(0.52).flips(1000)
x3 = FlipSim(0.57).flips(1000)

# Use Independent Two-Sampled T-test to test the Null Hypothesis that the
# means of two independent samples are the same.
# Results should be similar though not identical to:
# `Ttest_indResult(statistic=0.53653387639428951, pvalue=0.59164936190673534)`
# Null hypothesis is not rejected
print(stats.ttest_ind(x1, x2))
# `Ttest_indResult(statistic=-1.2543243107046314, pvalue=0.20987087051240788)`
# Null hypothesis is rejected
print(stats.ttest_ind(x1, x3))

# Use ANOVA to test the Null Hypothesis that the means of more than two
# independent samples are all the same.
# Results should be similar to:  
# `F_onewayResult(statistic=9.1459470595680799, pvalue=0.0001096574199724701)`
# Null Hypothesis is rejected
print(stats.f_oneway(x1, x2, x3))

# == Standard error of the means ==

# === Example from Temperley, _Music and Probability_, ch. 2 ===

sample = [1] * 599 + [0] * 401

# The standard deviation doesn't tell us what we want to know, because we are
# dealing with a single sample rather than the means of many samples.
mu = np.mean(sample)
sigma = np.std(sample)
print('mu = {}, std = {}'.format(mu, sigma))
plt.hist(sample)
plt.show()

# To estimate the mean from a single sample, use the Standard Error of the Means
# (SEM)
SEM = sigma / (len(sample) ** 0.5)
# `standard error of the means is 0.0154983547514`
print('standard error of the means is', SEM)
x = np.linspace(mu - 3 * SEM, mu + 3 * SEM, 100)
plt.plot(x, mlab.normpdf(x, mu, SEM))
plt.show()

# SEM is implemented directly in scipy.stats
SEM = stats.sem(sample)
# `95% confidence that population mean is between 0.5679877805090032`
# `and 0.6300122194909967`
print('95% confidence that population mean is between {} and {}'.
      format(mu - 2 * SEM, mu + 2 * SEM))

# Use the One-sample T-test to compare the mean of a sample with an expected
# mean
test_mean = 0.5 #
statistic, p_value = stats.ttest_1samp(sample, test_mean)
# `For one-sample T-test with given sample and a mean of 0.5 p-value is
# 2.6279100509e-10`
print('For one-sample T-test with given sample and a mean of',
      test_mean, 'p-value is', p_value)

# == Geometric distributions ==

# The following code is based on the ending conditions for Ash's algorithmic
# piece. Once the piece is at least 32 notes long, the next C4 produced
# initiates the ending of the piece. How many notes beyond 32 is it expected
# before C4 occurs?

def trial():
    # keep count of the notes produced before C4
    count = 0
    while True:
        # G3 = 0, A3 = 0, ..., C5 = 10
        value = random.randint(0, 10)
        # Stop trial if value is C4
        if value == 3:
            break
        count += 1
    return count

# Generate counts for 10,000 trials
N = 10000
trials = [trial() for _ in range(N)]
counts = Counter(trials)

# Create x and y values
xs = range(1, max(counts) + 1)
vals = [counts[x] for x in xs]
ys = np.array(vals) / N

# Plot the probability mass function of the resulting
# [geometric distribution](https://en.wikipedia.org/wiki/Geometric_distribution)
plt.title('Probability mass function\ngeometric distribution')
plt.ylabel('Probability')
plt.xlabel('Random selections until success')
plt.plot(xs, ys)
plt.show()

# Plot the cumulative distribution function
ys = np.cumsum(vals) / N
plt.title('Cumulative distribution function\ngeometric distribution')
plt.ylabel('Cumulative probability')
plt.show()

