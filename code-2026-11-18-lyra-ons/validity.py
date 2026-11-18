"""Q2. Past-only pairing makes V_s = W_i(s) W_j(t(s)) with W_j(t(s)) ALREADY OBSERVED, so
E[U_s - V_s | F_{s-1}] = p_i(s) (p_j(s) - W_j(t(s))), not <= delta.  A predictable bettor that
reads W_j(t(s)) breaks Type-I under the STATIC null.  Then: the same bettor against a
fresh-pair (both items unseen) design, and the size of delta under the drift null."""
import sys, numpy as np
sys.path.insert(0, '/tmp/lyra-wip/code/evalue')
import run_online_weights as rw
from dgp import null_dgp, drift_null_dgp
from eprocess import assign_strata, stratum_epsilon, make_online_past_pairing
Q, N, R, TH = 10, 4000, 1000, 20.0

def selective_block(d, rng, lam_tot=None):
    """Lyra's block joint bet X[m,s] (BLOCK=20), but lambda_{s,m} = cap/(#chosen) on strata whose
    block items ALL have an observed partner with W_j(t)=0 -- predictable since t(s)<s."""
    th = d['theta']; st = assign_strata(th, Q=Q); eps = stratum_epsilon(d['p_i'], d['p_j'], st, Q=Q)
    delta = 2 * eps; t = make_online_past_pairing(st, rng, Q=Q); hp = t != np.arange(N)
    U = d['W_i'] * d['W_j']; V = d['W_i'] * d['W_j'][t]
    inc = np.where(hp, U - V - delta[st], 0.0); b = 1 + delta.max(); cap = 1 / b
    W = 1.0; peak = 1.0
    for m in range(N // 20):
        sl = slice(20 * m, 20 * m + 20); X = np.zeros(Q); good = np.zeros(Q, bool)
        for s in range(Q):
            sel = (st[sl] == s) & hp[sl]
            if sel.any():
                X[s] = inc[sl][sel].mean()
                good[s] = (d['W_j'][t[sl][sel]] == 0).all() and s >= 5   # reads only the PAST
        lam = np.where(good, cap / max(good.sum(), 1), 0.0)
        W *= 1 + lam @ X; peak = max(peak, W)
    return peak >= TH, np.log(W)

def selective_fresh(d, rng):
    """Fresh-pair design: within each block, pair same-stratum items with each other (both unseen at
    bet time). The bettor has nothing about W_j(t) to read; give it the most it can see: bet cap on
    upper strata (s>=5) every block. E[X|F] = mean p_i(s)(p_j(s)-p_j(t)) - delta <= 0."""
    th = d['theta']; st = assign_strata(th, Q=Q); eps = stratum_epsilon(d['p_i'], d['p_j'], st, Q=Q)
    delta = 2 * eps; b = 1 + delta.max(); cap = 1 / b; W = 1.0; peak = 1.0; nbet = 0
    for m in range(N // 20):
        idx = np.arange(20 * m, 20 * m + 20); X = np.zeros(Q); has = np.zeros(Q, bool)
        for s in range(Q):
            I = idx[st[idx] == s]
            if len(I) >= 2:
                T = np.roll(I, 1)                      # cyclic pairing inside the block, t != s
                X[s] = np.mean(d['W_i'][I] * (d['W_j'][I] - d['W_j'][T]) - delta[s]); has[s] = s >= 5
        lam = np.where(has, cap / max(has.sum(), 1), 0.0); nbet += has.any()
        W *= 1 + lam @ X; peak = max(peak, W)
    return peak >= TH, np.log(W)

for name, f in [("past-only, selective bettor", selective_block), ("fresh-pair, upper-strata bettor", selective_fresh)]:
    rej, lw = zip(*[f(null_dgp(N, rng := np.random.default_rng(5000 + r)), rng) for r in range(R)])
    print(f"static null | {name:32s} Type-I {np.mean(rej):.3f}  (R={R}, 95% MC upper ~{np.mean(rej)+1.96*np.sqrt(max(np.mean(rej),1e-3)*(1-np.mean(rej))/R):.3f})  mean logW {np.mean(lw):+.2f}")

# delta under drift vs static
for name, g in [("static", null_dgp), ("drift", drift_null_dgp)]:
    d = g(N, np.random.default_rng(7)); st = assign_strata(d['theta'], Q=Q)
    print(f"{name:6s} null: delta_s = 2 eps_s (whole-stream oracle) = {np.round(2*stratum_epsilon(d['p_i'], d['p_j'], st, Q=Q), 3)}")
