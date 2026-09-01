"""Lemma (L) implies an explicit closed form for eps_i(e*lambda).
   n(lam,i,e) := #{ r : r = -i mod e, 1 <= r <= L, lam_{r-1} > lam_r }   (lam_L := 0)
   Predicted:  eps_i = 0            if i = 0 mod e
               eps_i = 1 if n>=1 else 0   otherwise
"""
from clio_sig import partitions_upto, eps_phi

def n_count(lam, i, e):
    L = len(lam)
    ext = list(lam) + [0]
    return sum(1 for r in range(1, L+1) if r % e == (-i) % e and ext[r-1] > ext[r])

bad = tot = 0; first = None
for e in range(2, 8):
    for lam in partitions_upto(12):
        mu = tuple(e*p for p in lam)
        for i in range(e):
            eps = eps_phi(mu, i, e)[0]
            pred = 0 if i % e == 0 else (1 if n_count(lam, i, e) >= 1 else 0)
            tot += 1
            if eps != pred:
                bad += 1
                if first is None: first = (e, lam, i, eps, pred)
print(f"closed form eps_i(e.lam): {tot-bad}/{tot} agree, {bad} mismatches" + (f"  first {first}" if first else ""))

# negative control: perturb the closed form and confirm the test sees it
for tweak, f in [("drop the i=0 case",      lambda lam,i,e: 1 if n_count(lam,i,e)>=1 else 0),
                 ("use n mod 2",            lambda lam,i,e: 0 if i%e==0 else n_count(lam,i,e)%2),
                 ("range 1<=r<=L-1",        lambda lam,i,e: 0 if i%e==0 else (1 if sum(1 for r in range(1,len(lam)) if r%e==(-i)%e and lam[r-1]>lam[r])>=1 else 0))]:
    b=t=0
    for e in range(2,8):
        for lam in partitions_upto(12):
            mu=tuple(e*p for p in lam)
            for i in range(e):
                t+=1
                if eps_phi(mu,i,e)[0] != f(lam,i,e): b+=1
    print(f"  neg control [{tweak:22s}]: {b:5d}/{t} mismatches  {'DETECTED' if b else '*** MISSED ***'}")

# edge cases
for e in (2,3):
    for lam in [(), (1,), (1,1), (2,2,2)]:
        mu = tuple(e*p for p in lam)
        print(f"  edge e={e} lam={lam} mu={mu}: " + ", ".join(
            f"i={i}: w={eps_phi(mu,i,e)[2]!r} eps={eps_phi(mu,i,e)[0]}" for i in range(e)))
