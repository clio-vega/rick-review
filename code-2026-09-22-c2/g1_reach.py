"""(G1) reachability check for proofs/2026-09-22-c1-crystal-edges-are-exchange-moves.tex.

The stated obstruction is that the X=empty construction pairs the REDUCED pair
(S\{b-1}, T\{b}), "which need not be additive".  The exhaustive null runs over n <= 7.
Question (per the review brief): does n <= 7 even CROSS the regime in which a
non-additive reduced pair exists?  If every reduced pair in range is additive, the
null is vacuous and the gap is untested, not tested-and-passed.
"""
import sys
sys.path.insert(0, '/home/clio/projects/proofs/code-q220')
from affine import *
from emptyX import case3_bs
from itertools import combinations

def is_additive(S, T, n):
    if len(S) >= n or len(T) >= n: return False
    w = window(compose(u_S(S, n), u_S(T, n)), n)
    return length(w, n) == len(S) + len(T)

def propersubsets(n):
    out = []
    for r in range(0, n):
        for c in combinations(range(n), r):
            out.append(frozenset(c))
    return out

print(f"{'n':>2} {'X=0 add.pairs':>13} {'(pair,b) cases':>14} {'reduced NON-additive':>21}")
tot_pairs = tot_cases = tot_bad = 0
first = []
for n in range(3, 9):
    subs = propersubsets(n)
    npairs = ncases = nbad = 0
    for S in subs:
        for T in subs:
            if set(S) | set(T) != set(range(n)):   # X(S,T) = empty
                continue
            if not is_additive(S, T, n):
                continue
            npairs += 1
            for (b, t) in case3_bs(S, T, n):
                ncases += 1
                Sp = frozenset(S) - {(b - 1) % n}
                Tp = frozenset(T) - {b}
                if not is_additive(Sp, Tp, n):
                    nbad += 1
                    if len(first) < 6:
                        first.append((n, sorted(S), sorted(T), b, t, sorted(Sp), sorted(Tp)))
    print(f"{n:>2} {npairs:>13} {ncases:>14} {nbad:>21}")
    tot_pairs += npairs; tot_cases += ncases; tot_bad += nbad
print(f"\ntotal n=3..8: {tot_pairs} additive pairs with X=empty, {tot_cases} (pair,b) cases, "
      f"{tot_bad} with NON-additive reduced pair")
if first:
    print("\nsmallest witnesses (n, S, T, b, t, S', T'):")
    for f in first: print("  ", f)
