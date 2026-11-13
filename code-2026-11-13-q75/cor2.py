"""Corollary 2: Sym_i -> (G_s)_i onto, i.e. rank of B_s restricted to
Sym_i x QSym_{d-i} equals r_i.  m_lambda = sum of M_alpha over rearrangements."""
import sys
from itertools import permutations
from qsym import comp_to_mask, M_in_F, F_product, rank, str_to_mask, r_vector
from thm1 import formula, alternating
def partitions(n, mx=None):
    if mx is None: mx = n
    if n == 0: yield (); return
    for p in range(min(n, mx), 0, -1):
        for rest in partitions(n - p, p): yield (p,) + rest
def m_in_F(lam):
    out = {}
    for alpha in set(permutations(lam)):
        for m, c in M_in_F(comp_to_mask(alpha), sum(lam)).items():
            out[m] = out.get(m, 0) + c
    return out
for L in range(2, int(sys.argv[1]) + 1):
    d = L + 1
    for s in alternating(L):
        sm = str_to_mask(s); rs = []
        for i in range(d + 1):
            if i in (0, d): rs.append(1); continue
            j = d - i
            rows = []
            for lam in partitions(i):
                f = m_in_F(lam)
                rows.append([sum(c * F_product(ma, i, mb, j).get(sm, 0) for ma, c in f.items())
                             for mb in range(1 << (j - 1))])
            rs.append(rank(rows))
        print(L, s, rs, 'onto' if rs == formula(L) else 'NOT ONTO')
