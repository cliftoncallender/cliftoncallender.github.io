# == Complex numbers and the Fourier transform ==

"""
Original code [here](fourier_demo.py).
"""

# === Complex numbers ===

# ==== Complex numbers in Python ====

# creating complex numbers
a = 2 + 1j
# `(2+1j)`
print(a)
# `<class 'complex'>`
print(type(a))

# adding complex numbers
b = 2 - 3j
# `(4-2j)`
print(a + b)
# accessing real and imaginary parts  
# `2.0`
print(a.real)
# `1.0`
print(a.imag)
# magnitude of a complex number  
# `2.23606797749979`
print(abs(a))

# `cmath`---standard Python library for complex numbers
import cmath
# phase of a complex number (measured in radians)  
# `0.4636476090008061`
print(cmath.phase(a))
# Alternatively, convert complex numbers from rectangular to polar coordinates.
mag, angle = cmath.polar(a)
# `(2+1j): magnitude = 2.23606797749979, angle = 0.4636476090008061`
print('magnitude = {}, angle = {}'.format(mag, angle))
# Or convert from polar to rectangular coordinates  
# `(2+1j)`
print(cmath.rect(mag, angle))
# Multiplying complex numbers ...  
# `(7-4j)`
print(a * b)
# ... is the same as multiplying the magnitudes and adding the phases
mag2 = abs(a) * abs(b)
angle2 = cmath.phase(a) + cmath.phase(b)
# `(6.999999999999999-4j)`
print(cmath.rect(mag2, angle2))

# ==== Complex numbers in Numpy ====

import numpy as np

# creating complex numpy arrays
c = np.array([1 + 2j, 3 + 1j, 4 - 5j], dtype=complex)
# `[ 1.+2.j  3.+1.j  4.-5.j]`
print(c)
# complex zeros
z = np.zeros(3, dtype=complex)
# `[ 0.+0.j  0.+0.j  0.+0.j]`
print(z)
# complex random numbers
import random
r = random.random() + random.random() * 1j
# `(0.6589664597814023+0.23948971180747303j)` as one possible result
print(r)
# magnitudes of a complex array  
# `[ 2.23606798  3.16227766  6.40312424]`
print(np.absolute(c))
# phases of a complex array  
# `[ 1.10714872  0.32175055 -0.89605538]`
print(np.angle(c))

# === Fast Fourier Transform (FFT) in Numpy ===

# Indicator (or characterstic) function of a diminished seventh chord
P = [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0]
# FFT of the indicator function
F_P = np.fft.fft(P)
# `[  4.00000000e+00 +0.00000000e+00j  -8.26946080e-16 +7.77156117e-16j`  
# ` 0.00000000e+00 +7.65713740e-16j   0.00000000e+00 +0.00000000e+00j`  
# ` 4.00000000e+00 -1.60410220e-15j  -1.76491446e-15 +1.66533454e-15j`  
# ` 0.00000000e+00 +0.00000000e+00j  -6.12323400e-17 -1.11022302e-16j`  
# ` 4.00000000e+00 -3.20820439e-15j   0.00000000e+00 +0.00000000e+00j`  
# ` 0.00000000e+00 +9.37968382e-16j   8.76736042e-16 +7.77156117e-16j]`
print(F_P)
# Most of the values are 0 with miniscule floating-point errors. You can use
# the numpy `round` function to round numpy array values (including complex
# values) to a specified number of decimals.  
# `[ 4.+0.j -0.+0.j  0.+0.j  0.+0.j  4.-0.j -0.+0.j  0.+0.j -0.-0.j  4.-0.j `
# `0.+0.j  0.+0.j  0.+0.j]`
print(np.round(F_P, 6))
