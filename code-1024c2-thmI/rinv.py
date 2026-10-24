"""Is the p=1 KLG count R-invariant?  R(r,c)=(m-1-c,m-1-r) is order-REVERSING and
swaps rows/columns, so it FLIPS the forced (1',1) order in a 2-box line while leaving
the 'diagonal box must be unprimed' constraint alone.  Prediction: NOT invariant.
Clio 2026-10-24 c2 peer review of Rick's Theorem I."""
from comb import D, strict_partitions, contains, R
from testZ import klg_count_p1, is_rim
from collections import Counter

def Rset(theta, m):
    return frozenset(R(b, m) for b in theta)

print("R-invariance of the p=1 KLG count, over actual (kappa,rho) Pieri pairs")
tot = diff = 0
hist_theta, hist_Rtheta = Counter(), Counter()
examples = []
for m in range(2, 8):
    for kap in strict_partitions(m):
        Dk = D(kap, m)
        for rho in strict_partitions(m):
            if rho == kap or not contains(kap, rho): continue
            th = Dk - D(rho, m)
            if not th or not is_rim(th) or len(th) > 12: continue
            a = klg_count_p1(th); b = klg_count_p1(Rset(th, m))
            tot += 1; hist_theta[a] += 1; hist_Rtheta[b] += 1
            if a != b:
                diff += 1
                if len(examples) < 6:
                    examples.append((m, kap, rho, sorted(th), a, sorted(Rset(th,m)), b))
    print(f"  m<={m}: pairs {tot}, count(theta) != count(R theta) in {diff}")
print(f"\n  histogram over theta   : {dict(sorted(hist_theta.items()))}")
print(f"  histogram over R(theta): {dict(sorted(hist_Rtheta.items()))}")
print(f"\n  disagreeing examples (m, kappa, rho, theta, N(theta), R(theta), N(R theta)):")
for e in examples: print("   ", e)
