"""
Clio, 2026-09-17. Three checks on Rick's Day 200 Section 5 (DS conjecture) and
Section 1 (Prop 1, bottom coefficient), using my own 2026-09-16 implementation.

(A) Count audit of "24 (Rick) + 33 (Clio) net of overlap".
(B) Prop 1: c_bot(a,r) = q^{-min(a,r)} on a grid.
(C) Conjecture 7 sharp form: leading coefficient of e^{(q,t)}_lambda is q^{-n(lambda)}.
"""
import sys
from hikita_star_clio import *
from triple import star_many, dominates

# ---------- (A) count audit ----------
print("=" * 70); print("(A) COUNT AUDIT of the DS evidence scorecard")
# Rick's length-2 set, PDF Sec 5: "18 cases (a,b) with a <= 4, b <= 6"
rick2 = sorted({tuple(sorted((a, b), reverse=True)) for a in range(1, 5) for b in range(1, 7)},
               reverse=True)
rick3 = [(2,1,1), (3,1,1), (2,2,1)]
rick4 = [(1,1,1,1), (2,1,1,1)]
rick = rick2 + rick3 + rick4
print("  Rick length-2 count      : %d  %s" % (len(rick2), "(matches his 18)" if len(rick2)==18 else "(NOT 18)"))
print("  Rick explicit finite lams: %d + %d + %d = %d distinct" % (len(rick2), len(rick3), len(rick4), len(set(rick))))
# My 2026-09-16 set, reviews/code-2026-09-16/out_dominance.txt
mine = []
for line in open("../code-2026-09-16/out_dominance.txt"):
    if line.strip().startswith("lam=("):
        lam = eval(line.split("lam=")[1].split(")")[0] + ")")
        mine.append(tuple(lam))
mine = sorted(set(mine), reverse=True)
print("  Clio lams (from log)     : %d" % len(mine))
ov = sorted(set(rick) & set(mine), reverse=True)
print("  OVERLAP                  : %d" % len(ov))
print("  UNION                    : %d   (NOT %d + %d = %d)" % (len(set(rick) | set(mine)), len(set(rick)), len(mine), len(set(rick)) + len(mine)))
print("  Rick-only                : %s" % (sorted(set(rick) - set(mine), reverse=True),))
print("  of which length >= 3     : %s" % ([l for l in set(rick) - set(mine) if len(l) >= 3],))
print("  Clio-only, length >= 3   : %d" % len([l for l in set(mine) - set(rick) if len(l) >= 3]))
print("  length>=3 in the UNION   : %d  (Rick %d, Clio %d)"
      % (len([l for l in set(rick) | set(mine) if len(l) >= 3]),
         len([l for l in rick if len(l) >= 3]), len([l for l in mine if len(l) >= 3])))

# ---------- (B) Prop 1 ----------
print(); print("=" * 70); print("(B) PROP 1: bottom coefficient of e_a * e_r is q^{-min(a,r)}")
allok = True
for a in range(1, 5):
    for r in range(1, 7):
        if a + r > 9: continue
        co, m = star_e(a, r)
        bot = tuple(sorted((a, r), reverse=True))
        got = co.get(bot, ZERO)
        want = (ONE/q)**min(a, r)
        ok = (got - want) == ZERO
        allok = allok and ok
        print("   a=%d r=%d  e_%-7s  %s%s" % (a, r, str(bot), "q^-%d OK" % min(a,r) if ok else "MISMATCH",
              "" if ok else "  got " + str(got)))
        sys.stdout.flush()
print("  Prop 1 on this grid:", "CONFIRMED" if allok else "FAILED")

# ---------- (C) Conjecture 7 leading coefficient ----------
print(); print("=" * 70); print("(C) CONJ 7 sharp form: leading coeff = q^{-n(lambda)}, n(lam)=sum (i-1)lam_i")
def nstat(lam): return sum(i * lam[i] for i in range(len(lam)))
allok = True
for lam in [(2,1),(2,2),(3,1),(3,2),(2,1,1),(2,2,1),(2,2,2),(3,2,1),(1,1,1),(1,1,1,1),(2,1,1,1),(3,1,1)]:
    co, m = star_many(list(lam))
    got = co.get(lam, ZERO); want = (ONE/q)**nstat(lam)
    ok = (got - want) == ZERO
    nonzero_all = all(v != ZERO for v in co.values())
    allok = allok and ok
    print("   lam=%-12s n(lam)=%-2d  %-10s  all coeffs nonzero: %s"
          % (str(lam), nstat(lam), "q^-%d OK" % nstat(lam) if ok else "MISMATCH", nonzero_all))
    sys.stdout.flush()
print("  Conj 7 diagonal on this set:", "CONFIRMED" if allok else "FAILED")
