"""
freshpair_review.py -- Clio, REVIEW 2026-11-19 c2, Lyra Prop. 3 (8a316ca, 3221be1, dbc1b9d).

An INDEPENDENT implementation of the within-block fresh-pair e-process. The only things
copied from Lyra's code are the DGP formulas (judge_probs, null, alt, top-3, latent, drift),
because those are the objects under review. Pairing, increments, slack, bettors and wealth
are my own code, and a separate cross-check (crosscheck_lyra.py) compares them with hers.

Setting (Lyra's harness): Q=10 equal-width theta strata, BLOCK=20 items per block, N=4000
(M=200 blocks), and rejection when the wealth reaches 20 (alpha=0.05).
A cell is a (block m, stratum k) with n items. Cells with n<2 place no bet (X=0).

Increments for a cell with n>=2, items s_1<...<s_n:
  cyclic : X = mean_r [ W_i(s_r) W_j(s_r) - W_i(s_r) W_j(s_{r+1 mod n}) ] - delta
  LOO    : X = mean_r [ W_i(s_r) W_j(s_r) - W_i(s_r) * mean_{u!=r} W_j(s_u) ] - delta
Slacks (R_i, R_j = within-cell ranges of p_i, p_j):
  d1      = max(R_i, R_j)            Lyra's per-block delta (first order)
  d2cyc   = R_i R_j / 2              second order, valid for ANY permutation pairing
  d2loo   = n/(n-1) * R_i R_j / 4    second order, LOO
Null means (proved in the review):
  E[cyclic raw] = mean_r (p_i(s_r)-c)(p_j(s_r)-p_j(s_{r+1}))  for any constant c  <= R_i R_j/2
  E[LOO raw]    = n/(n-1) Cov_cell(p_i, p_j)                                     <= n/(n-1) R_i R_j/4
"""
import sys
import numpy as np

Q, BLOCK, N, THRESH = 10, 20, 4000, 20.0
M = N // BLOCK


# ---------------- DGPs (formulas copied from Lyra's dgp.py / run_equicorr_puzzle.py) ------------
def judge_probs(theta, base_i=0.30, base_j=0.35):
    p_i = np.clip(base_i + 0.50 * (theta - 0.5), 0.02, 0.98)
    p_j = np.clip(base_j + 0.50 * (theta - 0.5), 0.02, 0.98)
    return p_i, p_j


def gen(kind, rng, gamma=0.0):
    theta = rng.uniform(0.0, 1.0, size=N)
    if kind == 'latent':
        theta = np.clip(theta + rng.uniform(-0.15, 0.15), 0.0, 1.0)
    if kind == 'drift':
        tf = np.linspace(0.0, 1.0, N)
        p_i, p_j = judge_probs(theta, 0.20 + 0.25 * tf, 0.25 + 0.25 * tf)
    else:
        p_i, p_j = judge_probs(theta)
    stratum = np.clip((theta * Q).astype(int), 0, Q - 1)
    if kind == 'alt':
        shock = rng.uniform(size=N) < gamma
    elif kind == 'top3':
        shock = (rng.uniform(size=N) < gamma) & (stratum >= Q - 3)
    else:
        shock = np.zeros(N, bool)
    W_i = np.where(shock, 1, (rng.uniform(size=N) < p_i).astype(int))
    W_j = np.where(shock, 1, (rng.uniform(size=N) < p_j).astype(int))
    return theta, stratum, p_i, p_j, W_i, W_j


# ---------------- increments -------------------------------------------------------------------
def increments(stratum, p_i, p_j, W_i, W_j):
    """Return dict of (M,Q) arrays: n, raw_cyc, raw_loo, d1, d2cyc, d2loo, Ejx_cyc, Ejx_loo,
    and also allfail_j (all W_j in cell are 0) for Lyra's rule."""
    out = {k: np.zeros((M, Q)) for k in
           ('n', 'raw_cyc', 'raw_loo', 'd1', 'd2cyc', 'd2loo', 'E_cyc', 'E_loo', 'allfail_j')}
    blk = np.arange(N) // BLOCK
    order = np.lexsort((np.arange(N), stratum, blk))   # group by (block, stratum), index order
    key = blk[order] * Q + stratum[order]
    starts = np.flatnonzero(np.r_[True, key[1:] != key[:-1]])
    ends = np.r_[starts[1:], len(order)]
    for a, z in zip(starts, ends):
        idx = order[a:z]
        m, k = divmod(int(key[a]), Q)
        n = len(idx)
        out['n'][m, k] = n
        if n < 2:
            continue
        wi, wj = W_i[idx].astype(float), W_j[idx].astype(float)
        pi, pj = p_i[idx], p_j[idx]
        nxt = np.roll(np.arange(n), -1)
        out['raw_cyc'][m, k] = np.mean(wi * wj - wi * wj[nxt])
        out['raw_loo'][m, k] = np.mean(wi * wj - wi * (wj.sum() - wj) / (n - 1))
        Ri, Rj = np.ptp(pi), np.ptp(pj)
        out['d1'][m, k] = max(Ri, Rj)
        out['d2cyc'][m, k] = Ri * Rj / 2.0
        out['d2loo'][m, k] = n / (n - 1) * Ri * Rj / 4.0
        out['E_cyc'][m, k] = np.mean(pi * (pj - pj[nxt]))
        out['E_loo'][m, k] = n / (n - 1) * np.mean((pi - pi.mean()) * (pj - pj.mean()))
        out['allfail_j'][m, k] = float(np.all(wj == 0))
    return out


def stream(inc, design):
    raw = inc['raw_cyc'] if design.endswith('cyc') else inc['raw_loo']
    delta = {'d1cyc': inc['d1'], 'd2cyc': inc['d2cyc'], 'd2loo': inc['d2loo'],
             'd1loo': inc['d1']}[design]
    live = inc['n'] >= 2
    X = np.where(live, raw - delta, 0.0)
    b = 1.0 + delta.max()
    return X, b, live, delta


# ---------------- bettors: lam (M,Q), lam>=0, sum<=cap ------------------------------------------
def bettors(X, live, delta, inc, cap):
    """Predictable bettors may use theta of blocks <= m (strata known beforehand, so live and
    delta of block m) and OUTCOMES of blocks < m only. 'peek' and 'lyra_rule' are look-ahead."""
    L = {}
    L['fixed'] = np.full((M, Q), cap / Q)
    nl = live.sum(1, keepdims=True)
    L['fixed_live'] = np.where(live, cap / np.maximum(nl, 1), 0.0)            # empty-cell adaptive
    L['max_n'] = np.zeros((M, Q))                                              # biggest live cell
    L['max_n'][np.arange(M), np.argmax(np.where(live, inc['n'], -1), 1)] = cap
    L['max_n'] *= live.any(1, keepdims=True)
    big = np.where(live, delta, np.inf)
    L['min_slack'] = np.zeros((M, Q))                                          # fairest live cell
    L['min_slack'][np.arange(M), np.argmin(big, 1)] = cap
    L['min_slack'] *= live.any(1, keepdims=True)
    # my 11-18 attack made predictable: stratum k>=5, live now, and in the most recent
    # PAST live cell of stratum k every W_j was 0
    rep = np.zeros((M, Q)); last = np.zeros(Q)
    for m in range(M):
        for k in range(5, Q):
            if live[m, k] and last[k] == 1:
                rep[m, k] = 1.0
        upd = live[m]
        last[upd] = inc['allfail_j'][m, upd]
    s = rep.sum(1, keepdims=True)
    L['replay_1118'] = np.where(s > 0, rep * cap / np.maximum(s, 1), 0.0)
    # momentum: whole cap on the live stratum with the largest cumulative past X
    cum = np.vstack([np.zeros(Q), np.cumsum(X, 0)[:-1]])
    L['momentum'] = np.zeros((M, Q))
    L['momentum'][np.arange(M), np.argmax(np.where(live, cum, -np.inf), 1)] = cap
    L['momentum'] *= live.any(1, keepdims=True)
    # ---- look-ahead positive controls (NOT predictable) ----
    pos = np.where(X > 0, 1.0, 0.0); s = pos.sum(1, keepdims=True)
    L['PEEK'] = np.where(s > 0, pos * cap / np.maximum(s, 1), 0.0)
    fire = np.zeros((M, Q)); fire[:, 5:] = (live & (inc['allfail_j'] == 1))[:, 5:]
    s = fire.sum(1, keepdims=True)
    L['LYRA_RULE'] = np.where(s > 0, fire * cap / np.maximum(s, 1), 0.0)
    return L


def wealth(X, lam):
    f = 1.0 + np.einsum('mq,mq->m', lam, X)
    return f, np.cumprod(f)


def run(kind, design, R, gamma=0.0, seed0=1000, cap_frac=1.0, want_bettors=True):
    rej, lw, fmin, zero = {}, {}, {}, {}
    fires_off = 0; fires = 0; mean_err = []
    for r in range(R):
        rng = np.random.default_rng(seed0 + r)
        _, stratum, p_i, p_j, W_i, W_j = gen(kind, rng, gamma)
        inc = increments(stratum, p_i, p_j, W_i, W_j)
        X, b, live, delta = stream(inc, design)
        cap = cap_frac / b
        L = bettors(X, live, delta, inc, cap) if want_bettors else {'fixed': np.full((M, Q), cap / Q)}
        for name, lam in L.items():
            assert np.all(lam >= -1e-15) and np.all(lam.sum(1) <= cap + 1e-12)
            f, Wp = wealth(X, lam)
            rej[name] = rej.get(name, 0) + int(np.any(Wp >= THRESH))
            lw.setdefault(name, []).append(np.log(np.maximum(Wp[-1], 1e-300)))
            fmin[name] = min(fmin.get(name, 9), f.min())
            zero[name] = zero.get(name, 0) + int(np.sum(f <= 1e-12))
        # Lyra's rule: does it ever fire on a cell where X != -delta ?
        firecells = (live & (inc['allfail_j'] == 1)); firecells[:, :5] = False
        fires += firecells.sum()
        fires_off += np.sum(np.abs(X[firecells] + delta[firecells]) > 1e-12)
        E = inc['E_cyc'] if design.endswith('cyc') else inc['E_loo']
        mean_err.append(np.max(np.where(live, E - delta, -np.inf)))
    res = {n: dict(typeI=rej[n] / R, lw=float(np.mean(lw[n])), fmin=float(fmin[n]),
                   zero=zero[n]) for n in rej}
    return res, dict(fires=int(fires), fires_off=int(fires_off),
                     max_Eminusdelta=float(np.max(mean_err)))


if __name__ == '__main__':
    R = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    print(f"Q={Q} BLOCK={BLOCK} N={N} M={M} THRESH={THRESH} R={R}")
    # (1) validity: every null x design x bettor
    for kind in ('null', 'latent', 'drift'):
        for design in ('d1cyc', 'd2cyc', 'd2loo'):
            res, aux = run(kind, design, R)
            print(f"\n[{kind:6s} {design}] Lyra-rule fires={aux['fires']} of which X!=-delta: "
                  f"{aux['fires_off']};  max over live cells of (E[raw]-delta) = {aux['max_Eminusdelta']:+.2e}")
            for n, v in res.items():
                print(f"   {n:12s} TypeI={v['typeI']:.3f}  mean logW={v['lw']:+9.3f}  "
                      f"min factor={v['fmin']:.4f}  factors<=1e-12: {v['zero']}")
    # (2) power, FIXED and fixed_live, Regime 1 and Regime 2 (top3)
    print("\nPOWER (fixed | fixed_live), R =", R)
    for kind, grid in (('alt', (0.02, 0.04, 0.06, 0.10, 0.15)), ('top3', (0.10, 0.20, 0.35))):
        for g in grid:
            row = []
            for design in ('d1cyc', 'd2cyc', 'd2loo'):
                res, _ = run(kind, design, R, gamma=g)
                row.append(f"{design}: {res['fixed']['typeI']:.3f} | {res['fixed_live']['typeI']:.3f}")
            print(f"  {kind:4s} gamma={g:.2f}   " + "   ".join(row))
