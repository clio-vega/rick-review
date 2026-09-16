"""Verify Rick's Day 193 closed form for e_3 * e_r against MY implementation."""
from hikita_star_clio import *
import sys, time

def qi(n):
    if n <= 0: return ZERO
    s = ZERO
    for i in range(n): s = s + t**i
    return s

# Rick's Day 193 closed form (proofs/2026-09-16-day193-e3-star-er-hikita.md, section 2)
def rick(r):
    pre = (q - ONE)/q**3
    return {
        3: ONE/q**3,
        2: pre * qi(r-1),
        1: pre * (qi(r+1)/qi(2)) * (q*qi(r) - t*qi(r-2)),
        0: pre * (qi(r+3)/(qi(2)*qi(3))) * (qi(r+1)*qi(r+2)*q**2
             - t*qi(2)*qi(r-1)*qi(r+1)*q + t**3*qi(r-2)*qi(r-1)),
    }

rs = [int(x) for x in sys.argv[1:]] or [1,2,3,4,5]
for r in rs:
    t0 = time.time()
    co, m = star_e(3, r)
    el = time.time() - t0
    R = rick(r)
    print("\n=== e_3 * e_%d   (m=%d, %.1fs) ===" % (r, m, el))
    print("  support (nonzero e_lambda):", sorted(co.keys(), reverse=True))
    allok = True
    for k in range(0, 4):
        lam = tuple(sorted((r+3-k, k), reverse=True)) if k > 0 else (r+3,)
        if r+3-k < k:
            print("   k=%d: not a partition, skip" % k); continue
        mine = co.get(lam, ZERO)
        his  = R[k]
        good = (mine - his) == 0
        allok = allok and good
        print("   c_%d  (e_%s):  %s" % (k, lam, "MATCH" if good else "*** MISMATCH ***"))
        if not good:
            print("        mine:", mine)
            print("        rick:", his)
    # anything in my support that Rick's 4 coefficients don't cover?
    covered = set()
    for k in range(0,4):
        if r+3-k >= k:
            covered.add(tuple(sorted((r+3-k,k), reverse=True)) if k>0 else (r+3,))
    extra = set(co.keys()) - covered
    if extra: print("   *** EXTRA nonzero terms outside Rick's form:", extra); allok=False
    print("   => %s ; #nonzero = %d, predicted min(3,%d)+1 = %d"
          % ("ALL MATCH" if allok else "DISCREPANCY", len(co), r, min(3,r)+1))
