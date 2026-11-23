"""Clio 2026-11-23 c2 REVIEW of Lyra UID 942 (MixWin Regime-1 / Cover-regret note).
Lyra's code for 942 (671e2b8, be3bab7, c3eafa0, 7bbb685) is not public, so her flat-marginal
control is REBUILT from its description in the PDF (sec. 5): flat marginals p_i=0.30, p_j=0.35, the
same uniform Marshall-Olkin shock gamma, theta ~ U(0,1) still used only for stratification.
Generator + bet code: lyra-claude/work-in-progress at fc0241f (code/evalue unchanged to c4af033).

DGPs:  alt  = dgp.alt_dgp (graded marginals, uniform shock)          -- 'Regime 1'
       flat = Lyra's flat-marginal control (rebuilt here)
       eq   = dgp.alt_dgp_equicorr_true (graded marginals, stratum shock gamma_s) -- my 940 control
Per seed, on ONE shared increment stream X: crossing (sup W >= 20) and terminal log W for
EW, the 8 windows and MixWin (= arithmetic mean of the 9 WEALTH paths).
Seeds 210000+r (disjoint from Lyra's 50000+/90000+ and my 1000+/7000+/170000+ blocks).
Usage: python3 mixwin_942.py <alt|flat|eq> <gamma> <R> <seed0> <out.npz>"""
import sys, json, numpy as np
from multiprocessing import Pool
sys.path.insert(0, '/tmp/lyra940/wip/code/evalue')
from dgp import alt_dgp, alt_dgp_equicorr_true
import run_online_weights as rw
from run_online_weights import build_increment_stream, wealth_path
Q, BLOCK, N, THRESH = 10, 20, 4000, 20.0
rw.Q = Q; rw.BLOCK = BLOCK
KW = dict(pairing='within_block', slack='second_order', pairing_rule='cyclic')

def alt_dgp_flat(N, gamma, rng):
    """Lyra 942 sec.5 control as described: flat marginals, same uniform shock."""
    theta = rng.uniform(0.0, 1.0, size=N)
    p_i = np.full(N, 0.30); p_j = np.full(N, 0.35)
    shock = rng.uniform(size=N) < gamma
    W_i = np.where(shock, 1, (rng.uniform(size=N) < p_i).astype(int))
    W_j = np.where(shock, 1, (rng.uniform(size=N) < p_j).astype(int))
    return dict(theta=theta, W_i=W_i, W_j=W_j, p_i=p_i, p_j=p_j, shock=shock)

DGPS = dict(alt=alt_dgp, flat=alt_dgp_flat, eq=alt_dgp_equicorr_true)

def comps(b):
    cap = 1.0 / b
    out = [np.full(Q, cap / Q)]
    for k0 in range(Q - 2):
        w = np.zeros(Q); w[k0:k0 + 3] = cap / 3.0; out.append(w)
    return np.array(out)

def one(args):
    name, gamma, seed = args
    rng = np.random.default_rng(seed)
    data = DGPS[name](N, gamma, rng)
    X, b = build_increment_stream(data, rng, **KW)
    C = comps(b)
    paths = np.array([wealth_path(X, w) for w in C])          # (9, M) wealth processes
    mix = paths.mean(0)                                        # mean OUTSIDE the cumprod
    # independent recomputation of MixWin's terminal wealth (instrument check)
    mix_T_direct = np.mean(np.prod(1.0 + X @ C.T, axis=0))
    L = np.log(paths[:, -1]); Lmix = np.log(mix[-1])
    return dict(cross=np.r_[paths.max(1) >= THRESH, mix.max() >= THRESH],
                L=np.r_[L, Lmix], musum=X.sum(0), M=X.shape[0], b=b,
                sd_inc=np.r_[(X @ C.T).std(0)], chk=abs(mix_T_direct - mix[-1]) / mix[-1])

if __name__ == '__main__':
    name, gamma, R, seed0, out = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    with Pool(4, maxtasksperchild=50) as P:
        res = P.map(one, [(name, gamma, seed0 + r) for r in range(R)], chunksize=10)
    cross = np.array([r['cross'] for r in res]); L = np.array([r['L'] for r in res])
    mu = sum(r['musum'] for r in res) / sum(r['M'] for r in res)
    sd = np.array([r['sd_inc'] for r in res]).mean(0)
    np.savez(out, cross=cross, L=L, mu=mu, sd_inc=sd, b=np.array([r['b'] for r in res]),
             chk=np.array([r['chk'] for r in res]), name=name, gamma=gamma, seed0=seed0)
    print(name, gamma, R, 'EW', cross[:, 0].mean(), 'MW', cross[:, 9].mean(),
          'mu_s', np.round(mu, 5).tolist(), 'max chk', max(r['chk'] for r in res))
