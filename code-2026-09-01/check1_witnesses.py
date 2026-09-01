from clio_sig import *

print("=== A. Lyra's non-vacuity witnesses, my code ===")
for mu, e, i, claim in [((2,1),2,1,'RR / eps=2'), ((3,2,1),2,0,'RRR / eps=3')]:
    eps, phi, w, red, ns = eps_phi(mu, i, e)
    print(f"  mu={mu} e={e} i={i}: word={w!r} reduced={red!r} eps={eps}   [Lyra: {claim}]")

print("\n=== B. worked example (mine, and hers) ===")
e, lam = 2, (5,3,2,1); mu = tuple(e*p for p in lam)
eps, phi, w, red, ns = eps_phi(mu, 1, e)
print(f"  e={e} lam={lam} mu={mu} i=1: word={w!r} reduced={red!r} eps={eps}")
print(f"  nodes (bottom-up): {ns}")

print("\n=== C. non-vacuity count on general partitions, |mu|<=10, e in {2,3} ===")
cnt = 0; tot = 0
for e in (2,3):
    for mu in partitions_upto(10):
        for i in range(e):
            tot += 1
            eps = eps_phi(mu, i, e)[0]
            if eps >= 2: cnt += 1
print(f"  {cnt} cases with eps_i >= 2 out of {tot}   [Lyra reports 83]")
