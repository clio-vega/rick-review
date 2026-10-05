"""Theorem 1 of Rick's Day 207b, checked against the Y-operators from scratch."""
import itertools, sympy as sp
from aha import *

def poch(a, n):   # (a;t)_n
    return sp.prod([1 - a*t**i for i in range(n)]) if n > 0 else sp.Integer(1)
def alpha(j):
    if j < 0: return sp.Integer(0)
    return sp.prod([s - t**i for i in range(1, j+1)])/poch(t, j) if j > 0 else sp.Integer(1)
def c(n, j):
    if j < 0 or n-j < 0: return sp.Integer(0)
    return poch(s, n-j)/poch(t, n-j)*(alpha(j) - s*t**(n-j)*alpha(j-1))
def F(n, w):
    return sum(c(n, j)*w**j for j in range(n+1))

def mulpol(A, B):
    r = Pol(A.m)
    for m1, c1 in A.d.items():
        for m2, c2 in B.d.items():
            r._add(tuple(a+b for a, b in zip(m1, m2)), sp.expand(c1*c2))
    return r

def rhs_thm1(m, k, r):
    tot = Pol(m)
    for b in range(k+1):
        co = s**b * F(k-b, t**(r-b))
        tot = tot + mulpol(e_poly(m, b), e_poly(m, r+k-b)).scale(co)
    return tot.norm()

def check(m, k, r):
    L = ekY(e_poly(m, r), k).scale(t**(-sp.binomial(k, 2)))
    return (L - rhs_thm1(m, k, r)).norm().is_zero()
