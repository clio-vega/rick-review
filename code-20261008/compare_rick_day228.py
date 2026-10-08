"""
Cross-check of Rick's Day 228 two-row x two-part closed form (WIP 018f5c2 /
rick-research 20d0146d, proofs/2026-10-07-day228-two-row-green-and-separator.md §A)
and Clio's Theorem C (clio-vega/work-in-progress 8c148bc) against an INDEPENDENT
third instrument: hl_orthogonality.GreenEngine (Gram-Schmidt definition of HL P).

Rick, for y <= x, lam=(l1,l2), l2>=1, x+y=n=|lam|, m_xy = 1 + [x=y]:
    y <  l2 :  (t-1) t^{l2-1-y} (1+t^y)
    y =  l2 :  m_xy - (1-t) t^{l2-1}
    y >  l2 :  (t-1) t^{l2-1}

Clio Thm C, lam=(a,b), m=min(x,y):
    m =  b           : 1 + [a=b] + (t-1) t^{b-1}
    1 <= m <= b-1    : (t-1) t^{b-1} + (t-1) t^{b-m-1}
    m >  b           : (t-1) t^{b-1}
"""
from fractions import Fraction as F
from hl_orthogonality import GreenEngine, b_lambda
import sys

def X_rick(lam, x, y, t):
    l1, l2 = lam
    if y > x: x, y = y, x                      # Rick's script normalises here too
    if y < l2:  return (t-1) * t**(l2-1-y) * (1 + t**y)
    if y == l2: return (2 if x == y else 1) - (1-t) * t**(l2-1)
    return (t-1) * t**(l2-1)

def X_clio_thmC(lam, x, y, t):
    a, b = lam
    m = min(x, y)
    if m == b:     return 1 + (1 if a == b else 0) + (t-1)*t**(b-1)
    if 1 <= m <= b-1: return (t-1)*t**(b-1) + (t-1)*t**(b-m-1)
    return (t-1)*t**(b-1)

def X_clio_indicator(lam, x, y, t):
    """Clio Thm C in its *indicator* form -- the primary statement in the paper."""
    a, b = lam
    v = (1 if y == b else 0) + (1 if x == b else 0) + (t-1)*t**(b-1)
    if 1 <= y <= b-1: v += (t-1)*t**(b-y-1)
    if 1 <= x <= b-1: v += (t-1)*t**(b-x-1)
    return v

# 25 rational sample points, none a root of unity, none 0 or 1
TVALS = [F(2), F(3), F(5), F(7), F(-2), F(-3), F(-5), F(1,2), F(1,3), F(2,3),
         F(3,2), F(5,2), F(7,3), F(-1,2), F(-2,3), F(4), F(6), F(-4), F(5,3),
         F(7,2), F(9,4), F(11,5), F(-3,2), F(-5,3), F(13,6)]

def run(nmax=10, perturb_at=None, verbose=True):
    """perturb_at: (n, lam, idx, delta) plants an error in the engine, to test the harness."""
    rows = []          # (n, lam, x, y) with EVERY ordered (x,y), Rick's index set
    for n in range(2, nmax+1):
        for l2 in range(1, n//2 + 1):
            lam = (n - l2, l2)
            for y in range(1, n):
                rows.append((n, lam, n - y, y))
    disagree_rick, disagree_clioC, disagree_clioI, nonint = [], [], [], []
    engine_vals = {}
    for n in range(2, nmax+1):
        for t in TVALS:
            pert = None
            if perturb_at and perturb_at[0] == n:
                pert = (perturb_at[1], perturb_at[2], perturb_at[3])
            E = GreenEngine(n, t, perturb=pert)
            for (nn, lam, x, y) in rows:
                if nn != n: continue
                mu = tuple(sorted((x, y), reverse=True))
                gt = E.X(lam, mu)
                engine_vals.setdefault((lam, x, y), {})[t] = gt
                if t.denominator == 1 and gt.denominator != 1:
                    nonint.append((lam, mu, t, gt))
                if gt != X_rick(lam, x, y, t):
                    disagree_rick.append((lam, (x, y), t, gt, X_rick(lam, x, y, t)))
                if gt != X_clio_thmC(lam, x, y, t):
                    disagree_clioC.append((lam, (x, y), t, gt, X_clio_thmC(lam, x, y, t)))
                if gt != X_clio_indicator(lam, x, y, t):
                    disagree_clioI.append((lam, (x, y), t, gt, X_clio_indicator(lam, x, y, t)))
        if verbose: print('  n=%d done' % n, flush=True)
    return dict(rows=rows, rick=disagree_rick, clioC=disagree_clioC,
                clioI=disagree_clioI, nonint=nonint, engine=engine_vals)

if __name__ == '__main__':
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    print('=== LIVE ARM: engine vs Rick vs Clio Thm C, n=2..%d, %d t-values ===' % (nmax, len(TVALS)))
    R = run(nmax)
    print('ordered (lam,(x,y)) rows                   : %d' % len(R['rows']))
    print('distinct (lam, unordered class) pairs      : %d' %
          len({(lam, tuple(sorted((x,y), reverse=True))) for (_n,lam,x,y) in R['rows']}))
    print('engine non-integral at integral t          : %d' % len(R['nonint']))
    print('engine vs RICK   disagreements             : %d' % len(R['rick']))
    print('engine vs CLIO Thm C (case form)           : %d' % len(R['clioC']))
    print('engine vs CLIO Thm C (indicator form)      : %d' % len(R['clioI']))
    for k in ('rick','clioC','clioI'):
        for w in R[k][:6]: print('   %s WITNESS' % k.upper(), w)
