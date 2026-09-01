import re
from clio_sig import *
pat = re.compile(r'^(AR)*A?$')

for (es, N, label) in [((2,3,4,5), 8, "primary  (Lyra: 938 triples)"),
                       ((2,3,4,5,6), 11, "extended (Lyra: 3900 triples)")]:
    tot = viol = badform = 0
    epsvals = {}
    zero_when_i0 = True
    for e in es:
        for lam in partitions_upto(N):
            mu = tuple(e*p for p in lam)
            for i in range(e):
                eps, phi, w, red, _ = eps_phi(mu, i, e)
                tot += 1
                epsvals[eps] = epsvals.get(eps, 0) + 1
                if eps > 1: viol += 1
                if not pat.match(w): badform += 1
                if i % e == 0 and eps != 0: zero_when_i0 = False
    print(f"{label}: e in {es}, |lam|<={N}")
    print(f"   triples={tot}  violations(eps>1)={viol}  words failing ^(AR)*A?$ = {badform}")
    print(f"   eps distribution: {dict(sorted(epsvals.items()))}   eps_0==0 always: {zero_when_i0}")
