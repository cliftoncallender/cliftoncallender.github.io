# == Dynamic programming and examples ==

"""
Example code for recursion, dynamic programming (using memoization), min-cost
path problem, and minimal voice leading. (Original code [here](dynamic_programming.py))
"""

# 
import numpy as np

# === Fibonacci numbers ===

# ==== Bottom-up approach ====
def fib(n):
    # base cases
    if n < 1:
        return 0
    if n in [1, 2]:
        return 1
    
    # iteration
    a = 1
    b = 1
    for i in range(3, n + 1):
        result = a + b
        a = b
        b = result
    return result
        
# ==== Recursive approach ====
def fib_recurse(n):
    
    # base cases
    if n < 1:
        return 0
    if n in [1, 2]:
        return 1

    # recursive case
    return fib_recurse(n-2) + fib_recurse(n-1)

"""
Notice that for n > 30 `fib_recurse(n)` is progressively and significantly
 slower than `fib(n)`.
 """

# === Dynamic Programming ===
 
# ==== Top-down approach (memoization) ====
 
memo = {}
def fib_memo(n):

    # base cases
    if n < 1:
        return 0
    if n in [1, 2]:
        return 1

    # if problem already solved, find solution in the memo
    try:
        return memo[n]

    # if problem is not in the memo, solve and memoize
    except KeyError:
        memo[n] = fib_memo(n-2) + fib_memo(n-1)
        return memo[n]

# Test the timing of the three Fibonacci functions 
import time

n = 35

start_time = time.time()
answer = fib(n)
end_time = time.time()
print('fib(%s) = %s' % (n, answer))
print('Answer found in', end_time - start_time, 'ms')
print()

start_time = time.time()
answer = fib_recurse(n)
end_time = time.time()
print('fib_recurse(%s) = %s' % (n, answer))
print('Answer found in', end_time - start_time, 'ms')
print()

start_time = time.time()
answer = fib_memo(n)
end_time = time.time()
print('fib_memo(%s) = %s' % (n, answer))
print('Answer found in', end_time - start_time, 'ms')
print()

# === Min cost path naive recursion ===

# ==== naïve recursive solution ====

def min_cost(cost, row, col):
    """
    Given a `cost` matrix of shape (size) `row` by `col`, return the value of
    the minimum cost path through the matrix.
    """
    
    # base cases
    if row == 0 and col == 0:
        return cost[row, col]
    if row < 0 or col < 0:
        return float('Inf')

    # recursive case
    result = cost[row][col] + min(min_cost(cost, row-1, col),
                                  min_cost(cost, row, col-1),
                                  min_cost(cost, row-1, col-1))
    return result

# ==== with memoization ====

#
memo = {}
def min_cost_memo(cost, row, col):
    """
    Memoized version of `min_cost` function
    """
    # Base cases
    if row == 0 and col == 0:
        return cost[0][0]
    if row < 0 or col < 0:
        return float('Inf')

    # check memo
    try:
        return memo[(row, col)]
    # recursive case
    except KeyError:
        result = cost[row][col] + min(min_cost_memo(cost, row, col-1),
                                      min_cost_memo(cost, row-1, col-1),
                                      min_cost_memo(cost, row-1, col))
        # write result to memo
        memo[(row, col)] = result
        return result


M = np.array([[1, 2, 3],
              [4, 8, 2],
              [1, 5, 3]])
# `the minimum cost is 8`
print('For matrix `M` the minimum cost is', min_cost(M, 2, 2))
print()

N = 10
# "A random seed (or seed state, or just seed) is a number (or vector) 
# used to initialize a pseudorandom number generator." – [Wikipedia](https://en.wikipedia.org/wiki/Random_seed)
np.random.seed(42)
random_matrix = np.random.random([N, N])
print('random_matrix is')
print(random_matrix)
# `random_matrix is`  
#`[[ 0.37454012  0.95071431  0.73199394  0.59865848  0.15601864  0.15599452`  
#`   0.05808361  0.86617615  0.60111501  0.70807258]`  
#` [ 0.02058449  0.96990985  0.83244264  0.21233911  0.18182497  0.18340451`  
#`   0.30424224  0.52475643  0.43194502  0.29122914]`  
#` [ 0.61185289  0.13949386  0.29214465  0.36636184  0.45606998  0.78517596`  
#`   0.19967378  0.51423444  0.59241457  0.04645041]`  
#` [ 0.60754485  0.17052412  0.06505159  0.94888554  0.96563203  0.80839735`  
#`   0.30461377  0.09767211  0.68423303  0.44015249]`  
#` [ 0.12203823  0.49517691  0.03438852  0.9093204   0.25877998  0.66252228`  
#`   0.31171108  0.52006802  0.54671028  0.18485446]`  
#` [ 0.96958463  0.77513282  0.93949894  0.89482735  0.59789998  0.92187424`  
#`   0.0884925   0.19598286  0.04522729  0.32533033]`  
#` [ 0.38867729  0.27134903  0.82873751  0.35675333  0.28093451  0.54269608`  
#`   0.14092422  0.80219698  0.07455064  0.98688694]`  
#` [ 0.77224477  0.19871568  0.00552212  0.81546143  0.70685734  0.72900717`  
#`   0.77127035  0.07404465  0.35846573  0.11586906]`  
#` [ 0.86310343  0.62329813  0.33089802  0.06355835  0.31098232  0.32518332`  
#`   0.72960618  0.63755747  0.88721274  0.47221493]`  
#` [ 0.11959425  0.71324479  0.76078505  0.5612772   0.77096718  0.4937956`  
#`   0.52273283  0.42754102  0.02541913  0.10789143]]`

# `Minimum cost for the random_matrix is 3.33835343297`
print('Minimum cost for the `random_matrix` is:', 
      min_cost_memo(random_matrix, N-1, N-1))
print()

# === Finding min-cost path ===

# ==== Min cost path returning memo rather than value ====
def min_cost_path(cost, row, col):
    memo = {(0, 0): cost[0][0]}

    # helper function contained with the larger function
    def min_cost_memo(cost, row, col):
        # base cases
        if row == 0 and col == 0:
            return cost[0][0]
        if row < 0 or col < 0:
            return float('Inf')

        # recursive case
        try:
            return memo[(row, col)]
        except KeyError:
            result = cost[row][col] + min(min_cost_memo(cost, row, col-1),
                                          min_cost_memo(cost, row-1, col-1),
                                          min_cost_memo(cost, row-1, col))
            memo[(row, col)] = result
            return result
        
    # call helper function
    min_cost_memo(cost, row, col)

    # return memo (rather than minimum cost)
    return memo

# ==== trackback algorithm ====

def trackback(memo, row, col):
    """
    `memo` is a dictionary created in `min_cost_path` based on a matrix
    of shape `row` by `col`.
    """
    # create a path with the final cell as the initial item
    path = [(row, col)]

    # continue loop until the last item in the path is the cell (0, 0)
    while path[-1] != (0, 0):
        row, col = path[-1]

        # consider the neighbors to the left, above, and diagonal
        neighbors = [(row-1, col), (row, col-1), (row-1, col-1)]
        neighbor_costs = []
        for neighbor in neighbors:
            try:
                cost = memo[neighbor]
            # if neighbor is not in memo, the cell is outside of the matrix
            except KeyError:
                cost = float('Inf')
            neighbor_costs.append(cost)

        # find the neighbor with the minimum cost
        index = np.argmin(neighbor_costs)
        # append this neighbor to the path
        path.append(neighbors[index])
    return path[::-1]

# ==== example minimum cost path ====
path_costs = min_cost_path(M, 2, 2)
#Dictionary or memo of minimum path costs for matrix `M` is  
# `{(0, 0): 1, (1, 0): 5, (2, 0): 6, (0, 1): 3, (1, 1): 9, (2, 1): 10, 
#  (0, 2): 6, (1, 2): 5, (2, 2): 8}`
print('Dictionary or memo of minimum path costs for matrix `M` is\n', 
      path_costs)
path = trackback(path_costs, 2, 2)
#Minimum cost path for `M` is  
# `[(0, 0), (0, 1), (1, 2), (2, 2)]`
print('Minimum cost path for `M` is\n', path)
print()

# === Minimum voice leading ===

def minimal_vl(A, B):
    """
    `A` and `B` or lists or numpy arrays representing pitch-class sets.
    
    Returns the minimum distance, and tuples for `A` and `B` ordered by 
    voices and including any doubled pcs.
    
    For example,
    
    `>>> A = [9, 11, 4]`  
    `>>> B = [10, 3, 5]`  
    `>>> minimal_vl(A, B)`  
    `(4.0, (4, 4, 9, 11), (3, 5, 10, 10))`
    
    indicating that the total voice-leading distance is 4, and the voice
    leading contains the following four voices: 4 to 3, 4 to 5, 9 to 10,
    and 11 to 10.
    """
    # Create sorted numpy arrays for each pcset
    A = np.sort(A)
    B = np.sort(B)

    # Generate a voice-leading matrix of motions from A to all rotations of B
    rows = len(A)
    cols = len(B)
    B_rotations = [np.roll(B, i) for i in range(cols)]
    matrices = [generate_vl_matrix(A, B_rot) for B_rot in B_rotations]

    # Memo for each voice-leading matrix
    memos = []
    for matrix in matrices:
        memos.append(min_cost_path(matrix, rows, cols))

    # Find minimal voice-leading distance and path
    min_distances = []
    for i, memo in enumerate(memos):
        min_distances.append(memo[(rows, cols)] - matrices[i][0][0])
    min_index = np.argmin(min_distances)
    path = trackback(memos[min_index], rows, cols)
    B_rot = B_rotations[min_index]
    chord1, chord2 = zip(*[(A[x%rows], B_rot[y%cols]) for x, y in path[:-1]])
    return min_distances[min_index], chord1, chord2

def generate_vl_matrix(X, Y):
    """
    Helper function for `minimal_vl`. `X` and `Y` are lists or numpy arrays
    representing pc-sets.
    
    Returns a 2D matrix. Rows correspond to `X[0]`, `X[1]`, ... 
    `X[-1]`, `X[0]`. Columns correspond to `Y[0]`, `Y[1]`, ..., `Y[-1]`,
    `Y[0]`.
    """
    # Add copy of first pc to the end of the list (circular space)
    X = np.append(X, X[0])
    Y = np.append(Y, Y[0])

    # Create empty matrix
    vl_M = np.empty([len(X), len(Y)])

    # Fill matrix with all pairwise interval classes
    for i, x in enumerate(X):
        for j, y in enumerate(Y):
            vl_M[i][j] = vl_dist(x, y)
    return vl_M

def vl_dist(x, y):
    """
    `x` and `y` are pitch classes.
    
    Returns the interval class between `x` and `y`.
    """
    return min((x - y) % 12, (y - x) % 12)

A = [0, 2, 4, 6, 7, 9, 10]
B = [6, 8, 10, 0, 1, 3, 4]

# ==== example voice leading ====
vld, chord1, chord2 = minimal_vl(A, B)
# Minimal voice-leading distance: 4.0
print('Minimal voice-leading distance:', vld)
# Minimal voice-leading path: `(0, 2, 4, 4, 6, 7, 9, 10) -> 
# (0, 1, 3, 4, 6, 8, 10, 10)`
print('Minimal voice-leading path:', chord1, '->', chord2)