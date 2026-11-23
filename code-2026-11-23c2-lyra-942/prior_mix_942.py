"""(a) MixWin == a predictable linear bet: lambda_m = sum_j pi_j M_j(m-1) lambda^j / sum_j pi_j M_j(m-1)
       (buy-and-hold over the 9 components = Bayes/multiplicative-weights mixture). Checked to 1e-10.
   (b) Prior-weighted mixtures: pi_EW in {1/9, 1/3, 1/2, 2/3}, rest split evenly over the 8 windows.
       Regret bounds: vs EW <= log(1/pi_EW); vs any window <= log(8/(1-pi_EW)).
Seeds 230000+r (disjoint from all earlier blocks and from mixwin_942.py's 210000+).
Usage: python3 prior_mix_942.py <alt|flat|eq> <gamma> <R>"""
import sys, json, numpy as np
from multiprocessing import Pool
from mixwin_942 import DGPS, comps, build_increment_stream, wealth_path, KW, N, THRESH
PIS = [1/9, 1/3, 1/2, 2/3]
def one(args):
    name, gamma, seed = args
    rng = np.random.default_rng(seed)
    X, b = build_increment_stream(DGPS[name](N, gamma, rng), rng, **KW)
    C = comps(b); P = np.array([wealth_path(X, w) for w in C])          # (9, M)
    # (a) predictable-weight form of the uniform mixture
    prev = np.hstack([np.ones((9, 1)), P[:, :-1]])                       # M_j(m-1), M_j(0)=1
    lam = (prev.T @ C) / prev.sum(0)[:, None]                            # (M, Q), F_{m-1}-measurable
    err = np.max(np.abs(wealth_path(X, lam) / P.mean(0) - 1.0))
    out = [P[0].max() >= THRESH]
    for pi in PIS:
        w = np.r_[pi, np.full(8, (1 - pi) / 8)]
        out.append((w @ P).max() >= THRESH)
    return np.array(out), err
if __name__ == '__main__':
    name, gamma, R = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
    with Pool(4, maxtasksperchild=50) as Pl:
        res = Pl.map(one, [(name, gamma, 230000 + r) for r in range(R)], chunksize=10)
    c = np.array([r[0] for r in res]); err = max(r[1] for r in res)
    row = dict(dgp=name, gamma=gamma, R=R, EW=c[:, 0].mean(), max_rel_err_predictable_form=err)
    for k, pi in enumerate(PIS, 1):
        d = c[:, k].astype(float) - c[:, 0]
        row[f'pi={pi:.3f}'] = dict(power=c[:, k].mean(), gain_vs_EW=d.mean(), paired_se=d.std(ddof=1) / np.sqrt(R))
    print(json.dumps(row))
