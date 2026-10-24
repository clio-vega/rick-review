from fractions import Fraction
from testZ import H_poly
from demazure import strict_partitions
from comb import rprime
for m in (3, 4):
    print(f"\n=== m={m}: r'(kappa), window W(kappa), and H_kappa(-M/2) on and just past it ===")
    ks = strict_partitions(m)
    POLY = {k: H_poly(k, m)[0] for k in ks}
    print(f"  {'kappa':14s} {'|k|':>3s} {'r2':>3s} {'W=2ceil(r2/2)+1':>16s}  H(-M/2) for M=3,5,...,W  | next")
    for k in sorted(ks, key=lambda x: (len(x), x)):
        rp = rprime(k, m); top = 2*((rp+1)//2)+1
        vals = [POLY[k](Fraction(-M, 2)) for M in range(3, top+1, 2)]
        nxt = POLY[k](Fraction(-(top+2), 2))
        print(f"  {str(k):14s} {sum(k):>3d} {rp:>3d} {top:>16d}  {str(vals):28s} | {nxt}")
