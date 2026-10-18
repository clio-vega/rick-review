"""
Check Rick's CORRECTED count of predicted pole pairs for the twelve N=5 (c)-failures:
22, not the 26 of UID 819 (UID 820 correction 1, per-triple 1+1+1+2+3+3+3+2+1+1+1+3).

"Predicted pair" per UID 819 section 8: (a,b) with a,b in kappa <= nu and kappa\{a,b} >= lambda,mu
-- exactly the (M,I) instances Theorem 7's residue sum needs.  Purely combinatorial.
"""
from itertools import combinations
from motegi_order import geq, subsets

N = 5
S = subsets(N)
triples = [((), (3,), (1,2,4)), ((), (3,), (1,2,5)), ((), (4,), (1,2,5)),
           ((), (4,), (1,3,5)), ((), (4,), (2,3,5)), ((), (4,), (1,2,3,5)),
           ((), (1,4), (1,2,3,5)), ((), (2,4), (1,2,3,5)), ((), (3,4), (1,2,3,5)),
           ((), (3,4), (1,2,4,5)), ((), (3,5), (1,2,4,5)), ((1,), (4,), (1,2,3,5))]
rick = [1, 1, 1, 2, 3, 3, 3, 2, 1, 1, 1, 3]

def predicted_pairs(lam, mu, nu):
    out = set()
    for a, b in combinations(range(1, N+1), 2):
        for kap in S:
            if a in kap and b in kap and geq(nu, kap):
                kpp = tuple(k for k in kap if k not in (a, b))
                if geq(kpp, lam) and geq(kpp, mu):
                    out.add((a, b)); break
    return sorted(out)

tot = 0; mine = []
print(f"{'triple':>28} {'mine':>5} {'Rick':>5}  pairs")
for (lam, mu, nu), r in zip(triples, rick):
    P = predicted_pairs(lam, mu, nu)
    mine.append(len(P)); tot += len(P)
    flag = "" if len(P) == r else "   <-- MISMATCH"
    print(f"{str((lam,mu,nu)):>28} {len(P):>5} {r:>5}  {P}{flag}")
print(f"\nmy total {tot}   Rick's corrected total {sum(rick)}   "
      f"UID 819's superseded figure 26")
print("per-triple agreement:", mine == rick)

# the N=4 lone exception, and whether it is the same object as the (c)-failure
print("\n--- the N=4 '1 in 143/144' ---")
lam, mu, nu = (), (3,), (1, 2, 4)
print(f"triple {(lam,mu,nu)}: predicted pairs {predicted_pairs(lam,mu,nu)} at N=4-relevant labels")
print("Rick names it in UID 820 ('The single failure is ((), (3), (1,2,4)) on H12')")
print("and it is the SAME triple as the N=4 (c)-failure of UID 819 section 1 and the")
print("q-valuation-2 residue of section 6 -- one object, three artifacts, explained in section 5.")
# stratum test: max(lambda cup mu) <= b ?
print(f"in stratum on H12?  max(lam u mu) = {max(max(lam,default=0),max(mu,default=0))} <= b=2 ? "
      f"{max(max(lam,default=0),max(mu,default=0)) <= 2}")
