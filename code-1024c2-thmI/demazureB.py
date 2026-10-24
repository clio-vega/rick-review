"""Independent Hilbert polynomials H^OG_kappa(j) = chi(X_kappa, L^j) for Schubert
varieties in OG(m,2m+1), via the Demazure character formula for SO(2m+1) = B_m.
Built from the root system; the type-C sibling is demazure.py.  Clio 2026-10-24 c2.

Conventions (B_m).  Weights live in (1/2)Z^m; we store the INTEGER vector v = 2*lambda.
  simple roots  alpha_i = eps_i - eps_{i+1} (i<m),   alpha_m = eps_m   (SHORT)
  coroots       alpha_i^vee = eps_i - eps_{i+1},     alpha_m^vee = 2 eps_m
  pairings      <lam,alpha_i^vee> = lam_i - lam_{i+1} = (v_i - v_{i+1})/2   (i<m)
                <lam,alpha_m^vee> = 2 lam_m = v_m
  spinor weight omega_m = (1/2,...,1/2)   ->   v = (1,...,1);   j*omega_m -> v=(j,...,j)
  step vectors in v-coords: 2*alpha_i.
"""
from fractions import Fraction
from itertools import combinations
import demazure as C   # reuse the Weyl group: W(B_m)=W(C_m)=signed perms, same lengths

def alphaB2(i, m):
    """2*alpha_i in v-coordinates."""
    v = [0]*m
    if i < m: v[i-1] = 2; v[i] = -2
    else:     v[m-1] = 2
    return tuple(v)

def pairingB(v, i, m):
    if i < m:
        d = v[i-1] - v[i]
        assert d % 2 == 0, "half-integer pairing: weight left the lattice"
        return d // 2
    return v[m-1]

def demazureB(f, i, m):
    a = alphaB2(i, m); out = {}
    for v, co in f.items():
        n = pairingB(v, i, m)
        if n >= 0:
            for k in range(n+1):
                w = tuple(v[t] - k*a[t] for t in range(m))
                out[w] = out.get(w, 0) + co
        elif n == -1:
            continue
        else:
            for k in range(1, -n):
                w = tuple(v[t] + k*a[t] for t in range(m))
                out[w] = out.get(w, 0) - co
    return {k: val for k, val in out.items() if val}

def chiB(word, v, m):
    f = {tuple(v): 1}
    for i in reversed(word):
        f = demazureB(f, i, m)
    return sum(f.values())

def H_OG_values(kappa, m, js):
    """chi(X_kappa, L^j) for j in js, via Demazure at the DOMINANT weights j*omega_m (j>=0)."""
    S = C.subset_of_kappa(kappa, m)
    w = C.min_rep(sorted(S), m)
    word = C.reduced_word(w, m)
    return [chiB(word, (j,)*m, m) for j in js]

def H_OG_poly(kappa, m):
    """the Hilbert POLYNOMIAL, interpolated from j = 0..|kappa| (degree |kappa|, Snapper)."""
    d = sum(kappa)
    js = list(range(d+1))
    vals = H_OG_values(kappa, m, js)
    return C.lagrange(list(zip(js, vals)))
