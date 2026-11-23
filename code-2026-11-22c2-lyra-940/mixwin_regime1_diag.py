"""Clio 2026-11-23 REVIEW of Lyra UID 940 (WIP b4b09e2 / code fc0241f).
MixWin on Regime 1: instrument check before mechanism.
 (1) per-stratum net drift mu_s = E[X_{m,s}] under alt_dgp (is Regime 1 'uniform' AFTER slack?)
 (2) paired power EW vs MixWin with discordant counts and paired SE (shared X stream)
 (3) the same on alt_dgp_equicorr_true (Lyra's genuinely equicorrelated DGP) -- the prediction:
     if the gain is heterogeneity of mu_s, it shrinks/flips there.
Seeds 170000+r (disjoint from Lyra's 50000+, 90000+ and my earlier 1000+, 7000+ blocks).
Usage: python3 mixwin_regime1_diag.py <dgp: alt|eq> <gamma> <R> <seed0>"""
import sys, json, numpy as np
sys.path.insert(0, '/tmp/lyra940/wip/code/evalue')
from dgp import alt_dgp, alt_dgp_equicorr_true
import run_online_weights as rw
from run_online_weights import build_increment_stream, wealth_path
Q, BLOCK, N, THRESH = 10, 20, 4000, 20.0
rw.Q = Q; rw.BLOCK = BLOCK
KW = dict(pairing='within_block', slack='second_order', pairing_rule='cyclic')

def comps(b):
    cap = 1.0 / b
    out = [np.full(Q, cap / Q)]
    for k0 in range(Q - 2):
        w = np.zeros(Q); w[k0:k0 + 3] = cap / 3.0; out.append(w)
    return out

dgpname, gamma, R, seed0 = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
dgp = alt_dgp if dgpname == 'alt' else alt_dgp_equicorr_true
rej = np.zeros((R, 2), bool); musum = np.zeros(Q); mucnt = 0
comp_rej = np.zeros(9)      # which single component crosses alone (diagnostic)
minfac = np.inf
for r in range(R):
    rng = np.random.default_rng(seed0 + r)
    data = dgp(N, gamma, rng)
    X, b = build_increment_stream(data, rng, **KW)
    musum += X.sum(0); mucnt += X.shape[0]
    cs = comps(b)
    paths = np.array([wealth_path(X, w) for w in cs])
    minfac = min(minfac, float((1.0 + X @ np.array(cs).T).min()))   # clamp check: factor >= 0 always?
    eq, mw = paths[0], paths.mean(0)
    rej[r] = (eq.max() >= THRESH, mw.max() >= THRESH)
    comp_rej += (paths.max(1) >= THRESH)
d = rej[:, 1].astype(float) - rej[:, 0].astype(float)
n10 = int((rej[:, 0] & ~rej[:, 1]).sum()); n01 = int((~rej[:, 0] & rej[:, 1]).sum())
print(json.dumps(dict(dgp=dgpname, gamma=gamma, R=R, seed0=seed0,
    EW=rej[:, 0].mean(), MixWin=rej[:, 1].mean(), gap_EW_minus_MW=-d.mean(),
    paired_se=float(d.std(ddof=1) / np.sqrt(R)), EW_only=n10, MW_only=n01,
    mu_s=[round(x, 6) for x in (musum / mucnt)], comp_power=[round(x / R, 3) for x in comp_rej],
    min_factor=minfac)))
