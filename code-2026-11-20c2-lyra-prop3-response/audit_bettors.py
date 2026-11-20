"""Predictability audit of Lyra's bettors (verify_prop3_freshpair.py @ ddf8cf6), static null,
delta_2 cyclic.  Uses HER build_increment_stream / build_lambda / wealth_path.

(1) Forced-firing census.  For each bettor, over all (m,k) with lambda_{m,k} > 0 on a live
    cell, count how often X_{m,k} == -delta_{m,k} (the all-W_j=0-type forced value) vs not.
    A firing whose event forces the increment's sign is no test (11-19 c2 lesson).
(2) Look-ahead lesion: for each data-adaptive bettor, a copy that may read block m.
    momentum_peek : cumX updated BEFORE betting (reads X[m]).
    replay_peek   : last_zero updated BEFORE betting (reads W_j of block m).
    The harness must show these lesions move (Type-I up), else it cannot see a one-step leak.
(3) Exact predictability check: perturb block m's outcomes AFTER lambda is built and verify
    lambda_m is unchanged - done by rebuilding lambda on a copy of X / wj_zero whose rows >= m
    are scrambled and comparing row m.
"""
import sys, json
import numpy as np
sys.path.insert(0, sys.argv[1])
import verify_prop3_freshpair as v
from dgp import null_dgp
R = int(sys.argv[2])

ADAPT = ['replay', 'momentum']


def lam_lesion(name, X, b, live, ncell, wj_zero):
    M, Qn = X.shape
    cap = 1.0 / b
    lam = np.zeros((M, Qn))
    if name == 'momentum_peek':
        cumX = np.zeros(Qn)
        for m in range(M):
            cumX += X[m]                      # LEAK: includes block m
            live_k = np.where(live[m])[0]
            if len(live_k):
                lam[m, live_k[np.argmax(cumX[live_k])]] = cap
    elif name == 'replay_peek':
        last_zero = np.zeros(Qn, dtype=bool)
        for m in range(M):
            for k in range(Qn):               # LEAK: update with block m first
                if live[m, k]:
                    last_zero[k] = wj_zero[m, k]
            for k in range(5, Qn):
                if live[m, k] and last_zero[k]:
                    lam[m, k] = cap
            s = lam[m].sum()
            if s > cap:
                lam[m] *= cap / s
    return lam


fires = {bt: [0, 0] for bt in v.BETTORS}          # [forced, unforced]
rej = {n: 0 for n in ['momentum', 'replay', 'momentum_peek', 'replay_peek']}
pred_viol = {bt: 0 for bt in v.BETTORS}
pred_checks = 0
rngp = np.random.default_rng(12345)
for r in range(R):
    rng = np.random.default_rng(1000 + r)
    data = null_dgp(v.N, rng)
    X, b = v.build_increment_stream(data, rng, pairing='within_block',
                                    slack='second_order', pairing_rule='cyclic')
    strata, live, ncell, wj_zero = v.cell_structure(data)
    dc = v.per_cell_delta(data, 'second_order', 'cyclic')
    for bt in v.BETTORS:
        lam = v.build_lambda(bt, X, b, live, ncell, wj_zero, dc)
        on = (lam > 0) & live
        forced = np.isclose(X, -dc, atol=1e-15, rtol=0) & on
        fires[bt][0] += int(forced.sum())
        fires[bt][1] += int(on.sum() - forced.sum())
        # (3) scramble rows >= m and compare row m, at 3 random m per run
        if r < 50:
            for m in rngp.integers(1, v.M_BLOCKS, size=3):
                X2, wz2 = X.copy(), wj_zero.copy()
                X2[m:] = rngp.permutation(X2[m:].ravel()).reshape(X2[m:].shape)
                wz2[m:] = ~wz2[m:]
                lam2 = v.build_lambda(bt, X2, b, live, ncell, wz2, dc)
                pred_checks += (bt == v.BETTORS[0])
                if not np.allclose(lam2[m], lam[m]):
                    pred_viol[bt] += 1
        if bt in rej:
            rej[bt] += bool(np.any(v.wealth_path(X, lam) >= v.THRESH))
    for name in ['momentum_peek', 'replay_peek']:
        lam = lam_lesion(name, X, b, live, ncell, wj_zero)
        rej[name] += bool(np.any(v.wealth_path(X, lam) >= v.THRESH))

print(json.dumps({'R': R,
                  'fires_forced_unforced': fires,
                  'predictability_violations_per_bettor(of 150 row checks)': pred_viol,
                  'typeI': {k: c / R for k, c in rej.items()}}, indent=1))
