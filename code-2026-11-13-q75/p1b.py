"""P1b (r_2 = 1 iff s constant or even alternating), all s, direct pairing.
r_2(s) = rank of the 2 x 2^{d-3} matrix [F_s](F_a F_beta), a in {(2),(1,1)}."""
import sys, time
from itertools import combinations
from fractions import Fraction
from qsym import F_product, desc_mask, rep_perm

def is_even_alt(s):
    L = len(s)
    return L % 2 == 0 and all(s[p] != s[p + 1] for p in range(L - 1))
def is_const(s): return len(set(s)) <= 1

for d in range(4, int(sys.argv[1]) + 1):
    t0 = time.time(); L = d - 1; j = d - 2
    rows = {}   # smask -> {beta: [cA, cB]}
    for a_idx, ma in enumerate((0, 1)):     # mask 0 = (2), mask 1 = (1,1)
        for mb in range(1 << (j - 1)):
            for m, c in F_product(ma, 2, mb, j).items():
                rows.setdefault(m, {}).setdefault(mb, [0, 0])[a_idx] += c
        F_product.cache_clear()
    bad = []; hist = {0: 0, 1: 0, 2: 0}
    for sm in range(1 << L):
        ent = rows.get(sm, {})
        vecs = [v for v in ent.values() if v != [0, 0]]
        if not vecs: r = 0
        else:
            a0, b0 = vecs[0]
            r = 1 if all(a * b0 - b * a0 == 0 for a, b in vecs) else 2
        hist[r] += 1
        s = ''.join('1' if sm >> p & 1 else '0' for p in range(L))
        pred = 1 if (is_const(s) or is_even_alt(s)) else 2
        if r != pred: bad.append((s, r, pred))
    print('L=%2d: %6d strings, r2 histogram %s, mismatches vs P1b: %d %s  (%.0fs)'
          % (L, 1 << L, hist, len(bad), bad[:4], time.time() - t0), flush=True)
