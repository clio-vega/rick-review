"""SEPARATOR for the support coincidence.

Rule S ("conjugate of the classical Schur support"): support of e_a*e_b*e_c in the
    e-basis = conjugates of the Schur support of e_a e_b e_c  (i.e. {mu : c^{mu'}_{1^a,1^b,1^c} > 0}).
Rule D ("two-row -> l-row dominance interval"): support = ALL mu with <= 3 rows,
    |mu| = n, mu dominates sort(a,b,c).

For two factors these agree (both give min(a,b)+1 two-row shapes). For THREE they
need not.  Compute the truth with my own implementation and see which survives.

  e_a * e_b * e_c = t^{-[a(a-1)+b(b-1)+c(c-1)]/2} * ( e_a(Y) e_b(Y) e_c(Y) . 1 )
(from Hikita line 267:  q(e_lambda(Y)) = t^{sum l_i(l_i-1)/2} e^{(q,t)}_lambda(X) )
"""
from hikita_star_clio import *
import sys, itertools

def star_many(parts, m=None):
    n = sum(parts)
    if m is None: m = n
    A = {tuple([0]*m): ONE}
    for p in sorted(parts):            # Y-operators commute, order irrelevant
        A = e_Y(p, A, m)
    A = scal((ONE/t)**sum(p*(p-1)//2 for p in parts), A)
    return expand_in_e(A, n, m), m

def dominates(mu, nu):
    s1 = s2 = 0
