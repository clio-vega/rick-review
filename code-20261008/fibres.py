"""Rick's HUNCH: 'for y != lam_2 the value does not involve lam_1'.
That is a claim about the fibre {lam_1 : lam_1 + lam_2 = x + y} at fixed (lam_2, y).
If every fibre is a singleton the invariance is a constant function wearing a theorem's
clothes. Count the fibres -- in his tested window, and then OUTSIDE it."""
from collections import defaultdict
from fractions import Fraction as F
from hl_orthogonality import GreenEngine
from compare_rick_day228 import X_rick, TVALS
import sys

def window(nmax):
    out = []
    for n in range(2, nmax+1):
        for l2 in range(1, n//2+1):
            lam = (n-l2, l2)
            for y in range(1, n):
                out.append((n, lam, n-y, y))
    return out

for NMAX in (10,):
    ROWS = window(NMAX)
    fib = defaultdict(set)
    for (n, lam, x, y) in ROWS:
        ylo, xhi = min(x, y), max(x, y)
        if ylo == lam[1]: continue              # hunch excludes y = lam_2
        fib[(lam[1], ylo)].add(lam[0])
    sizes = sorted((len(v) for v in fib.values()))
    print('=== fibres of (lam_2, min(x,y)) over lam_1, y != lam_2, |lam| <= %d ===' % NMAX)
    print('  number of distinct (lam_2, y) classes : %d' % len(fib))
    print('  fibre sizes                           : %s' % sizes)
    print('  singletons                            : %d of %d' % (sum(1 for s in sizes if s == 1), len(sizes)))
    print('  max fibre                             : %d' % max(sizes))
    print('  classes with fibre >= 2               : %d' % sum(1 for s in sizes if s >= 2))
    tot = sum(sizes)
    print('  rows covered (unordered)              : %d' % tot)
    for k in sorted(fib):
        print('     lam_2=%d, y=%d : lam_1 in %s' % (k[0], k[1], sorted(fib[k])))

# --- direct test of the invariance on ONE fibre, computed from the engine, not the formula ---
print()
print('=== invariance read off the ENGINE (not the formula): fix (lam_2,y), vary lam_1 ===')
for (l2, y) in [(2, 1), (3, 1), (3, 2), (2, 5), (1, 3)]:
    seen = {}
    for l1 in range(max(l2, 2*y - l2, 1), 11 - l2 + 1):
        if l1 < l2: continue
        n = l1 + l2
        if n < 2: continue
        x = n - y
        if y > x: continue
        sig = []
        for t in TVALS[:6]:
            E = GreenEngine(n, t)
            sig.append(E.X((l1, l2), tuple(sorted((x, y), reverse=True))))
        seen[l1] = tuple(sig)
    distinct = len(set(seen.values()))
    print('  lam_2=%d, y=%d : lam_1 = %s  -> %d distinct engine value(s) %s'
          % (l2, y, sorted(seen), distinct, 'INVARIANT' if distinct <= 1 else 'VARIES'))
