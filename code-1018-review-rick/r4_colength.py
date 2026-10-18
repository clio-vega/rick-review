"""
REVIEW 2026-10-18 -- first-hand check of the ONE step of Rick's Corollary 1 that
carries no owner locator: "the colength of span_O{Ahat_I} is #(D-edges)".

He derives it from (a) triangularity of Ahat w.r.t. Motegi's >= [Motegi Thm 2.6(i)],
so det Ahat = prod_I Ahat_{I,I}; and (b) a count of which diagonal root factors
vanish on D, giving 2^{N-1}, 2^{N-2}, 2^{N-2} for the three root families.

Checked here INDEPENDENTLY by computing ord_D(det Ahat) as a t-valuation along an
explicit uniformiser, and comparing with #E_D counted from the moment graph.
"""
import sys, itertools, random
sys.path.insert(0,'/home/clio/projects/proofs/code-1018c2-gauge')
import sympy as sp
from q484_engine import Atilde, subsets, geq, q

t = sp.Symbol('t')
def psi(v): return (1-q*v**2)/(1-q)
def Psi(w,M): return sp.prod([psi(w[m-1]) for m in M]) if M else sp.Integer(1)

def ord_t(expr):
    e = sp.cancel(sp.together(sp.expand(expr)))
    if e == 0: return sp.oo
    num, den = sp.fraction(e)
    return sp.Poly(num, t).monoms()[-1][0] - sp.Poly(den, t).monoms()[-1][0]

def divisors(N, c):
    """(name, w on D with uniformiser t, #E_D from the moment graph)."""
    out = []
    for a in range(1, N+1):
        for eps in (1, -1):
            w = list(c); w[a-1] = sp.Integer(eps) + t
            out.append((f'w{a}={eps:+d}', w,
                        len([M for M in subsets(N) if a in M])))
    for a, b in itertools.combinations(range(1, N+1), 2):
        w = list(c); w[b-1] = (1+t)/w[a-1]
        out.append((f'H_{a}{b} (w{a}w{b}=1)', w,
                    len([M for M in subsets(N) if a in M and b in M])))
    for a, b in itertools.permutations(range(1, N+1), 2):
        if a > b: continue
        w = list(c); w[b-1] = w[a-1] + t
        # CORRECTED: the matching {M: b in M, a not in M} <-> {M: a in M, b not in M}
        # is a BIJECTION, so #edges = 2^(N-2), NOT the 2^(N-1) matched VERTICES.
        # My first counter summed both sides and reported a mismatch against Rick's
        # 2^(N-2); his number is the right one. A count of edges is not a count of
        # endpoints -- and the over-count also contaminated the plant's report.
        out.append((f'w{a}=w{b}', w,
                    len([M for M in subsets(N) if b in M and a not in M])))
    return out

def run(N, plant=None):
    c = [sp.Rational(v) for v in ([sp.Rational(5,3), sp.Rational(7,4), sp.Rational(11,9)][:N])]
    rows = []
    for name, w, nedges in divisors(N, c):
        tot = 0
        for I in subsets(N):
            d = Atilde(N, w, list(I), list(I), X='C') * Psi(w, I)
            if plant is not None: d = d * plant(w, I)
            tot += ord_t(d)
        rows.append((name, tot, nedges, tot == nedges))
    return rows

print("=== triangularity (Motegi Thm 2.6(i)): A~_{M,I} = 0 unless M >= I ===")
for N in (2,3):
    bad = viol = 0
    wg = [sp.Rational(5,3), sp.Rational(7,4), sp.Rational(11,9)][:N]
    for M, I in itertools.product(subsets(N), subsets(N)):
        v = sp.cancel(Atilde(N, wg, list(M), list(I), X='C'))
        if not geq(M, I):
            if v != 0: viol += 1
        bad += 1
    print(f"  N={N}: {bad} pairs, off-support nonzero: {viol}  "
          f"{'OK (triangular)' if viol==0 else '*** NOT TRIANGULAR ***'}")

for N in (2,3):
    print(f"=== N={N}: ord_D(det Ahat) vs #E_D ===")
    for name, tot, ne, ok in run(N):
        print(f"  {name:22s} ord_D(det)={tot:3d}   #E_D={ne:3d}   {'OK' if ok else 'MISMATCH'}")
    # PLANT: an extra simple zero on H_12 in one diagonal entry must break the identity
    PL = lambda w, I: (1 - 1/(w[0]*w[1])) if I == tuple(range(1, N+1)) else sp.Integer(1)
    fired = [name for name, tot, ne, ok in run(N, PL) if not ok]
    print(f"  plant (extra H_12 zero in the top diagonal entry): fires on {fired or '*** BLIND ***'}")
