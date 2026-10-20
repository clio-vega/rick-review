"""Corollary Delta, fast: exact rational evaluation at several random points.
det(w_i^{c-k} - w_i^k)_{i=1..n,k=0..n-1} == 0  <=>  c in [0,2n-2] ?
A nonzero evaluation at ANY point certifies 'not identically zero'.
For the vanishing half we test MANY independent points (and the column
argument is structural, checked separately below)."""
from fractions import Fraction as F
import random

def det_ex(rows):
    """exact fraction-free-ish Gaussian elimination over Q"""
    n = len(rows); A = [r[:] for r in rows]; d = F(1)
    for i in range(n):
        p = next((r for r in range(i, n) if A[r][i] != 0), None)
        if p is None: return F(0)
        if p != i: A[i], A[p] = A[p], A[i]; d = -d
        d *= A[i][i]
        inv = F(1)/A[i][i]
        for r in range(i+1, n):
            if A[r][i] != 0:
                f = A[r][i]*inv
                for cc in range(i, n): A[r][cc] -= f*A[i][cc]
    return d

def mat(n, c, ws):
    return [[ws[i]**(c-k) - ws[i]**k for k in range(n)] for i in range(n)]

random.seed(20261020)
bad = []
print("n   c-range swept            zeros found (c values)        predicted [0,2n-2]")
for n in range(1, 8):
    zeros = []
    for c in range(-8, 2*n+9):
        vals = []
        for _ in range(4):
            ws = [F(random.randint(2, 400), random.randint(1, 97)) for _ in range(n)]
            if len(set(ws)) < n: continue
            vals.append(det_ex(mat(n, c, ws)))
        if all(v == 0 for v in vals):
            zeros.append(c)
    pred = list(range(0, 2*n-1))
    if zeros != pred: bad.append((n, zeros, pred))
    print(f"{n}   [-8,{2*n+8}]{'':12s} {str(zeros):28s}  {pred}")
print()
print("MISMATCHES:", bad if bad else "none")
print()
# structural check of the stated column argument
print("--- stated proof step: 'column c-k is minus column k' ---")
for n in range(1, 8):
    for c in range(0, 2*n-1):
        k = min(c, n-1)
        kp = c-k
        ok = 0 <= kp <= n-1
        assert ok, (n, c, k, kp)
    print(f"n={n}: for every c in [0,{2*n-2}], k=min(c,n-1) gives c-k in [0,{n-1}]  OK")
