"""Controls. A green reading is worthless unless the same harness reads red when
something is wrong. Two arms: (a) plant an error in the ENGINE, (b) plant an error
in each BRANCH of Rick's formula and count how many rows notice."""
from fractions import Fraction as F
from hl_orthogonality import GreenEngine, partitions
from compare_rick_day228 import X_rick, X_clio_thmC, TVALS
import sys

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 8

def rows(nmax):
    out = []
    for n in range(2, nmax+1):
        for l2 in range(1, n//2+1):
            lam = (n-l2, l2)
            for y in range(1, n):
                out.append((n, lam, n-y, y))
    return out
ROWS = rows(NMAX)

# ---------------- ARM (a): planted ENGINE error ----------------
print('=== ARM (a): plant an error in the engine P_lambda (n=6) ===')
n = 6
lams6 = list(partitions(6))
target = (4, 2)
idx = lams6.index((3, 2, 1))
for delta in (0, 1):          # delta=0 is the no-op arm: the two arms MUST differ
    pert = None if delta == 0 else (target, idx, delta)
    bad = 0; tot = 0
    for t in TVALS[:5]:
        E = GreenEngine(6, t, perturb=pert)
        for (nn, lam, x, y) in ROWS:
            if nn != 6: continue
            mu = tuple(sorted((x, y), reverse=True)); tot += 1
            if E.X(lam, mu) != X_rick(lam, x, y, t): bad += 1
    print('  perturb delta=%d -> %d/%d rows disagree with Rick' % (delta, bad, tot))

# ---------------- ARM (b): per-branch ablation of Rick's formula ----------------
print()
print('=== ARM (b): mutate ONE branch of Rick\'s formula; how many rows notice? ===')
def mutated(which):
    def f(lam, x, y, t):
        l1, l2 = lam
        if y > x: x, y = y, x
        if y < l2:
            return (t-1)*t**(l2-y)*(1+t**y) if which == 'y<l2' else (t-1)*t**(l2-1-y)*(1+t**y)
        if y == l2:
            if which == 'y=l2':   return (2 if x == y else 1) - (1-t)*t**l2
            if which == 'm_xy':   return 1 - (1-t)*t**(l2-1)      # drop the x=y doubling
            return (2 if x == y else 1) - (1-t)*t**(l2-1)
        return (t-1)*t**l2 if which == 'y>l2' else (t-1)*t**(l2-1)
    return f

engines = {}
for nn in range(2, NMAX+1):
    for t in TVALS[:5]:
        engines[(nn, t)] = GreenEngine(nn, t)

for which in ('none', 'y<l2', 'y=l2', 'y>l2', 'm_xy'):
    f = X_rick if which == 'none' else mutated(which)
    hit_rows, tot_rows = set(), set()
    for (nn, lam, x, y) in ROWS:
        mu = tuple(sorted((x, y), reverse=True))
        tot_rows.add((lam, x, y))
        for t in TVALS[:5]:
            if engines[(nn, t)].X(lam, mu) != f(lam, x, y, t):
                hit_rows.add((lam, x, y)); break
    print('  mutate %-6s -> %3d of %3d ordered rows disagree' % (which, len(hit_rows), len(tot_rows)))

# ---------------- how many rows live in each branch, and how many DISTINCT values ----------------
print()
print('=== branch occupancy and distinct values, Rick\'s index set n<=%d ===' % NMAX)
from collections import Counter, defaultdict
occ = Counter(); vals = defaultdict(set); occ_u = Counter()
seen_unordered = set()
for (nn, lam, x, y) in ROWS:
    l2 = lam[1]; ylo = min(x, y)
    br = 'y<l2' if ylo < l2 else ('y=l2' if ylo == l2 else 'y>l2')
    occ[br] += 1
    key = (lam, tuple(sorted((x, y), reverse=True)))
    if key not in seen_unordered:
        seen_unordered.add(key); occ_u[br] += 1
    sig = tuple(X_rick(lam, x, y, t) for t in TVALS)
    vals['all'].add(sig); vals[br].add(sig)
print('  ordered rows per branch   :', dict(occ))
print('  distinct rows per branch  :', dict(occ_u))
print('  DISTINCT VALUES overall   : %d  (out of %d ordered rows / %d distinct rows)'
      % (len(vals['all']), len(ROWS), len(seen_unordered)))
for br in ('y<l2','y=l2','y>l2'):
    print('  distinct values in %-5s : %d' % (br, len(vals[br])))
# x=y stratum
xy = [(lam,x,y) for (nn,lam,x,y) in ROWS if x == y]
print('  rows with x=y (m_xy=2)    : %d   %s' % (len(xy), [ (l,x) for (l,x,y) in xy ]))
print('  rows with lam=(L,L) (m=0) : %d' % len([1 for (nn,lam,x,y) in ROWS if lam[0]==lam[1]]))
print('  rows with BOTH            : %d' % len([1 for (nn,lam,x,y) in ROWS if lam[0]==lam[1] and x==y]))
