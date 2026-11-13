#!/usr/bin/env python3
"""FLOAT. Exact expected log-growth per step (enumeration over {-1,+1}^K) of three
combiners under an alternative with independent strata, P(X_s=+1)=(1+mu_s)/2.
M1 = mean over strata of per-stratum products (valid under arbitrary dependence)
M2 = product over time of the joint linear bet 1+sum_s lam_s X_s (valid under the
     global conditional null with arbitrary contemporaneous dependence), sum lam_s <= 1
M3 = product of per-stratum products (valid only if sequential/independent)
Each method's bet sizes are optimised (grid) for the stated alternative -- an oracle
comparison of attainable rates, not a practical tuning rule."""
import itertools, math
def rates(mus, grid=400):
    K = len(mus)
    lams = [i/grid for i in range(1, grid)]
    g1 = lambda lam, mu: (1+mu)/2*math.log(1+lam) + (1-mu)/2*math.log(1-lam)
    # M1 asymptotic rate = max_s best single-stratum rate
    best_single = [max(g1(l, m) for l in lams) for m in mus]
    r1 = max(best_single)
    r3 = sum(best_single)
    # M2: weights proportional to mu_s (oracle direction), total L in (0,1)
    tot = sum(abs(m) for m in mus) or 1
    def g2(L):
        w = [L*m/tot for m in mus]
        e = 0.0
        for xs in itertools.product((-1, 1), repeat=K):
            p = math.prod((1+m*x)/2 for m, x in zip(mus, xs))
            e += p*math.log(1 + sum(wi*x for wi, x in zip(w, xs)))
        return e
    r2 = max(g2(l) for l in lams[:-1])
    return r1, r2, r3
for mus in ([0.1]*4, [0.1, 0, 0, 0], [0.2]*4, [0.3, 0.1, 0, 0]):
    r1, r2, r3 = rates(mus)
    print(f"mu={mus}:  M1(mean of processes)={r1:.5f}  M2(joint linear bet)={r2:.5f}  M3(product, needs indep)={r3:.5f}")
