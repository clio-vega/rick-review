from neyman_check import *
from itertools import product
ok = bad = 0
for (k, n) in [(1,3),(2,4),(2,5),(3,5)]:
    lo, hi = 0, 3
    cands = [t for t in product(range(lo,hi+1), repeat=k) if is_cylpar(t,k,n)]
    for lam in cands:
        for mu in cands:
            if not contains(mu,lam,k,n): continue
            if nboxes(lam,mu,k,n) > 5: continue
            for ell in (1,2,3):
                a = gf_chain(lam,mu,k,n,ell)
                b = gf_direct(lam,mu,k,n,ell)
                a = {w:c for w,c in a.items() if c}
                b = {w:c for w,c in b.items() if c}
                if a == b: ok += 1
                else:
                    bad += 1
                    if bad < 4: print("MISMATCH", k,n,lam,mu,ell,a,b)
print(f"chain-model vs direct-filling: {ok} agree, {bad} disagree")
