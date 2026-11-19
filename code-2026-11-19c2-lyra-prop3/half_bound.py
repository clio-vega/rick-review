"""half_bound.py -- exhaustive check, for cells of size n=2..7, of the range of the RAW fresh-pair
increment over all 0/1 outcome vectors (w = W_i, v = W_j on the cell):
  cyclic: mean_r w_r (v_r - v_{r+1 mod n})
  LOO   : mean_r w_r (v_r - (sum v - v_r)/(n-1))
Claim: both lie in [-1/2, 1/2], so |X| <= 1/2 + delta and b = 1/2 + max delta is admissible.
Control: the past-only design (partner outside the cell, free bit) reaches -1."""
import itertools
from fractions import Fraction as Fr

for n in range(2, 8):
    cyc, loo = set(), set()
    for w in itertools.product((0, 1), repeat=n):
        for v in itertools.product((0, 1), repeat=n):
            cyc.add(sum(Fr(w[r] * (v[r] - v[(r + 1) % n]), n) for r in range(n)))
            S = sum(v)
            loo.add(sum(Fr(w[r]) * (v[r] - Fr(S - v[r], n - 1)) for r in range(n)) / n)
    print(f"n={n}: cyclic range [{min(cyc)}, {max(cyc)}]   LOO range [{min(loo)}, {max(loo)}]"
          f"   LOO min == -n/(4(n-1)) rounded? {min(loo)} vs {-Fr(n*n//4, n*(n-1))}")
# control: an outside partner bit u per item (past-only / independent partner)
n = 2
past = {sum(Fr(w[r] * (v[r] - u[r]), n) for r in range(n))
        for w in itertools.product((0, 1), repeat=n) for v in itertools.product((0, 1), repeat=n)
        for u in itertools.product((0, 1), repeat=n)}
print(f"control, outside partners, n=2: range [{min(past)}, {max(past)}]  (reaches -1)")
