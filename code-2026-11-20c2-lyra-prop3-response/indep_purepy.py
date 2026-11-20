"""Independent instrument (Clio, 2026-11-20 c2): pure-Python (no numpy, no import of Lyra's
code) re-implementation of the within-block cyclic fresh-pair e-process with second-order
slack delta_2 = R_i R_j / 2, on the STATIC null, for two predictable bettors:

  fixed      : lambda_k = (1/b)/Q on every stratum, every block.
  min-slack  : whole cap 1/b on the live cell (n>=2) of block m with the smallest delta.

Built from the DEFINITIONS only (Lyra's dgp.py formulas for p_i, p_j; equal-width strata;
BLOCK=20; Q=10; N=4000; threshold 20).  Different RNG (Python's Mersenne `random`, seeds
7_000_000 + r), so agreement with her table can only be within Monte-Carlo error.

Also records, per run, the exact conditional mean E[X_{m,k} | F_{m-1}] - which under H0 is
(1/n) sum_r p_i(s_r)(p_j(s_r) - p_j(s_{r+1})) - delta - and its maximum (must be <= 0), and the
minimum factor (must be > 0), and the number of n=2 live cells where the game is exactly fair.

Usage: python3 indep_purepy.py R [slack]   slack in {d2, d1, d2half, zero}
  'zero'   : LESION, delta = 0.  Cells are comonotone (p_i, p_j both increase in theta), so by the
             rearrangement inequality E[X|F] >= 0: the instrument must report max E[X|F] > 0.
  'd2half' : LESION, delta = R_i R_j / 4 (half the proved slack): conditional mean > 0 on
             comonotone cells; the instrument must report max E[X|F] > 0.
"""
import random, math, sys

Q, BLOCK, N, THRESH = 10, 20, 4000, 20.0
M = N // BLOCK


def clip(x, lo=0.02, hi=0.98):
    return lo if x < lo else hi if x > hi else x


def one_run(seed, slack):
    rnd = random.Random(seed)
    theta = [rnd.random() for _ in range(N)]
    p_i = [clip(0.30 + 0.50 * (t - 0.5)) for t in theta]
    p_j = [clip(0.35 + 0.50 * (t - 0.5)) for t in theta]
    W_i = [1 if rnd.random() < p else 0 for p in p_i]
    W_j = [1 if rnd.random() < p else 0 for p in p_j]
    stratum = [min(int(t * Q), Q - 1) for t in theta]

    X = [[0.0] * Q for _ in range(M)]
    D = [[None] * Q for _ in range(M)]          # delta per live cell, None if n<2
    max_cond_mean = -1e9
    n2_fair = 0
    for m in range(M):
        cells = [[] for _ in range(Q)]
        for s in range(m * BLOCK, (m + 1) * BLOCK):
            cells[stratum[s]].append(s)
        for k in range(Q):
            c = cells[k]
            n = len(c)
            if n < 2:
                continue
            Ri = max(p_i[s] for s in c) - min(p_i[s] for s in c)
            Rj = max(p_j[s] for s in c) - min(p_j[s] for s in c)
            if slack == 'd2':
                delta = 0.5 * Ri * Rj
            elif slack == 'd1':
                delta = max(Ri, Rj)
            elif slack == 'd2half':
                delta = 0.25 * Ri * Rj
            elif slack == 'zero':
                delta = 0.0
            else:
                raise ValueError(slack)
            raw = 0.0
            cm = 0.0
            for r in range(n):
                s, t = c[r], c[(r + 1) % n]
                raw += W_i[s] * (W_j[s] - W_j[t])
                cm += p_i[s] * (p_j[s] - p_j[t])
            X[m][k] = raw / n - delta
            D[m][k] = delta
            cmk = cm / n - delta
            max_cond_mean = max(max_cond_mean, cmk)
            if n == 2 and abs(cmk) < 1e-15:
                n2_fair += 1
    b = 1.0 + max(d for row in D for d in row if d is not None)
    cap = 1.0 / b

    out = {}
    for bettor in ('fixed', 'min-slack'):
        W, rej, fmin = 1.0, False, 1e9
        for m in range(M):
            if bettor == 'fixed':
                f = 1.0 + sum(cap / Q * X[m][k] for k in range(Q))
            else:
                live = [k for k in range(Q) if D[m][k] is not None]
                if not live:
                    f = 1.0
                else:
                    kstar = min(live, key=lambda k: D[m][k])   # theta-determined: predictable
                    f = 1.0 + cap * X[m][kstar]
            fmin = min(fmin, f)
            W *= f
            if W >= THRESH:
                rej = True
        out[bettor] = (rej, fmin)
    return out, max_cond_mean, n2_fair


def clopper_pearson(k, n, a=0.05):
    """Exact two-sided CP interval via bisection on the binomial CDF (pure Python)."""
    def cdf(x, p):
        return sum(math.comb(n, i) * p**i * (1 - p)**(n - i) for i in range(x + 1))
    def solve(f, lo, hi):
        for _ in range(80):
            mid = (lo + hi) / 2
            if f(mid):
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2
    lo = 0.0 if k == 0 else solve(lambda p: 1 - cdf(k - 1, p) < a / 2, 0.0, 1.0)
    hi = 1.0 if k == n else solve(lambda p: cdf(k, p) > a / 2, 0.0, 1.0)
    return lo, hi


if __name__ == '__main__':
    R = int(sys.argv[1])
    slack = sys.argv[2] if len(sys.argv) > 2 else 'd2'
    rej = {'fixed': 0, 'min-slack': 0}
    fmin = 1e9
    mcm = -1e9
    fair = 0
    for r in range(R):
        out, mc, nf = one_run(7_000_000 + r, slack)
        for bt in rej:
            rej[bt] += out[bt][0]
            fmin = min(fmin, out[bt][1])
        mcm = max(mcm, mc)
        fair += nf
    print(f'slack={slack} R={R}')
    for bt, k in rej.items():
        lo, hi = clopper_pearson(k, R)
        print(f'  {bt:10s} Type-I {k}/{R} = {k/R:.3f}   95% CP [{lo:.4f}, {hi:.4f}]')
    print(f'  max over all live cells of E[X|F_(m-1)] = {mcm:.3e}   (<= 0 required)')
    print(f'  min factor over both bettors = {fmin:.4f}   (> 0 required)')
    print(f'  exactly-fair n=2 cells (|E[X|F]|<1e-15) = {fair}')
