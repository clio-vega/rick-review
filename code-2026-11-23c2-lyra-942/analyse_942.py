"""Paired analysis of mixwin_942.py outputs. Columns: 0=EW, 1..8 windows {k,k+1,k+2}, 9=MixWin."""
import sys, json, numpy as np
from math import lgamma, log, exp, erfc, sqrt
def binom_two_sided(k, n):
    """Exact two-sided sign test p-value (p=1/2), symmetric so 2*min tail."""
    if n == 0: return 1.0
    lp = lambda i: lgamma(n + 1) - lgamma(i + 1) - lgamma(n - i + 1) - n * log(2)
    lo = min(k, n - k)
    return min(1.0, 2 * sum(exp(lp(i)) for i in range(lo + 1)))
def wilcoxon_p(x):
    """Wilcoxon signed-rank, normal approximation with average ranks for ties (R >= 4000 here)."""
    x = x[x != 0]; n = len(x); a = np.abs(x)
    order = a.argsort(); ranks = np.empty(n); ranks[order] = np.arange(1, n + 1)
    _, inv, cnt = np.unique(a, return_inverse=True, return_counts=True)
    ranks = np.bincount(inv, ranks) / cnt; ranks = ranks[inv]
    W = ranks[x > 0].sum(); m = n * (n + 1) / 4
    v = n * (n + 1) * (2 * n + 1) / 24 - (cnt ** 3 - cnt).sum() / 48
    z = (W - m) / sqrt(v); return erfc(abs(z) / sqrt(2)), z
rows = []
for f in sys.argv[1:]:
    d = np.load(f); c = d['cross']; L = d['L']; R = len(c)
    ew, mw = c[:, 0], c[:, 9]
    dd = mw.astype(float) - ew.astype(float)
    n10 = int((ew & ~mw).sum()); n01 = int((~ew & mw).sum())
    mcn = binom_two_sided(n01, n01 + n10)
    dL = L[:, 9] - L[:, 0]
    wil_p, wil_z = wilcoxon_p(dL)
    argmax = L[:, :9].argmax(1)
    gapmax = L[:, :9].max(1) - L[:, 9]
    # Gaussian approximation for P(EW is the argmax of the 9): fit mean/cov of L[:, :9], resample
    mu, S = L[:, :9].mean(0), np.cov(L[:, :9].T)
    Z = np.random.default_rng(0).multivariate_normal(mu, S, 200000)
    Z0 = np.random.default_rng(1).multivariate_normal(np.full(9, mu.mean()), S, 200000)  # equal means
    rows.append(dict(dgp=str(d['name']), gamma=float(d['gamma']), R=R,
        mu_s=np.round(d['mu'], 5).tolist(), mu_ratio=float(d['mu'][0] / d['mu'][-1]),
        EW=ew.mean(), MW=mw.mean(), gap_EW_minus_MW=-dd.mean(), paired_se=dd.std(ddof=1) / np.sqrt(R),
        EW_only=n10, MW_only=n01, mcnemar_p=mcn,
        meanL_EW=L[:, 0].mean(), meanL_MW=L[:, 9].mean(), meanL_win=L[:, 1:9].mean(0).round(3).tolist(),
        median_dL=float(np.median(dL)), mean_dL=dL.mean(), se_dL=dL.std(ddof=1) / np.sqrt(R),
        frac_MW_gt_EW=float((dL > 0).mean()), wilcoxon_p=float(wil_p), wilcoxon_z=float(wil_z),
        EW_argmax=float((argmax == 0).mean()), sd_L_EW=float(L[:, 0].std()), sd_L_win=float(L[:, 1:9].std(0).mean()),
        sd_inc_ratio=float(d['sd_inc'][1:].mean() / d['sd_inc'][0]),
        corr_EW_win=float(np.mean([np.corrcoef(L[:, 0], L[:, k])[0, 1] for k in range(1, 9)])),
        gauss_EW_argmax=float((Z.argmax(1) == 0).mean()), gauss_EW_argmax_equalmeans=float((Z0.argmax(1) == 0).mean()),
        sandwich_ok=int(((L[:, :9].max(1) - np.log(9) <= L[:, 9] + 1e-12) & (L[:, 9] <= L[:, :9].max(1) + 1e-12)).sum()),
        mean_regret=gapmax.mean(), comp_power=c[:, :9].mean(0).round(3).tolist()))
for r in rows:
    print(json.dumps({k: (round(v, 5) if isinstance(v, float) else v) for k, v in r.items()}))
