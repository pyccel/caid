# coding: utf-8
import numpy as np

# ... create Matrix L
def build_L(n):
    L = np.zeros((n, n))
    for i in range(0, n-1):
        L[i, i] = (i+1) * 1. / n
        L[i, i+1] = (n-i-1) * 1. / n
    L[n-1, n-1] = 1.
    return L
# ...

# ... create Matrix M
def build_M(n):
    M = np.zeros((n, n))
    M[0, 0] = 1.
    for i in range(1, n):
        M[i, i-1] = (i) * 1. / n
        M[i, i] = (n-i) * 1. / n
    return M
# ...

# ... create S matrix
def build_S(n, S):
    L = build_L(n)
    M = build_M(n)
    # ... create Su and Sd matrices
    Su = S.dot(L)
    Sd = S.dot(M)
    # ...
    S_new = np.zeros((n+1, n+1))
    S_new[0:n, 0:n] = Su
    S_new[n, 1:n+1] = Sd[-1, :]
    S_new[1:n+1, n] = Sd[:, -1]

    return S_new
    # ...

# ... matrix conversion
def matrix_conversion_ubspline_to_bernstein(n):
    # ... initialization
    S0 = np.ones((1, 1))
    # ...

    # ... recursive algo
    S = S0
    for d in range(1, n):
        S = build_S(d, S)
    # ...

    return S
# ...
