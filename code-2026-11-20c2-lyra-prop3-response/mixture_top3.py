"""Q(b): Regime 2 (shock only in strata 7-9).  Compare, under d2 cyclic slack, R=500:
  EQ    : equal weights cap/Q (Lyra's FIXED)
  TOP3  : cap/3 on strata 7-9 (support of the alternative known: an ORACLE on support)
  MIX   : (EQ-wealth + TOP3-wealth)/2 -- average of two e-processes on one filtration, valid
          for any alternative; reject when MIX >= 20.
  MIXWIN : average of the 8 contiguous top-3 windows {k,k+1,k+2} plus EQ (9 components, equal
          prior) -- a support-AGNOSTIC mixture (no knowledge that the shock sits in 7-9).
Null row (static, gamma=0) checks Type-I of each.  Uses my 11-19 c2 engine (freshpair_review.py),
which agrees with Lyra's increments to 1.1e-16."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'code-2026-11-19c2-lyra-prop3'))
import numpy as np, freshpair_review as F
R = int(sys.argv[1])
for kind, g in (('null', 0.0), ('top3', 0.20), ('top3', 0.35)):
    rej = dict(EQ=0, TOP3=0, MIX=0, MIXWIN=0)
    for r in range(R):
        rng = np.random.default_rng(1000 + r)
        _, st, pi, pj, Wi, Wj = F.gen(kind, rng, g)
        X, b, live, delta = F.stream(F.increments(st, pi, pj, Wi, Wj), 'd2cyc')
        cap = 1 / b
        def W(lam):
            return F.wealth(X, lam)[1]
        lam_eq = np.full((F.M, F.Q), cap / F.Q)
        wins = []
        for k0 in range(F.Q - 2):
            l = np.zeros((F.M, F.Q)); l[:, k0:k0 + 3] = cap / 3; wins.append(W(l))
        w_eq, w_top3 = W(lam_eq), wins[7]
        rej['EQ'] += np.any(w_eq >= F.THRESH)
        rej['TOP3'] += np.any(w_top3 >= F.THRESH)
        rej['MIX'] += np.any((w_eq + w_top3) / 2 >= F.THRESH)
        rej['MIXWIN'] += np.any((w_eq + sum(wins)) / 9 >= F.THRESH)
    print(kind, g, {k: round(v / R, 3) for k, v in rej.items()}, flush=True)
