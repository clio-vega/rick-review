"""Prop 6.1 referee check, fast mode: t specialised to rationals, exact Fraction
arithmetic throughout.  Same two printed inputs (Prop 2.1 and eq (2.1))."""
import sys, time
sys.path.insert(0, '/home/clio/projects/reviews/code-20261010')
import star
from star import *
from symfun import partitions, e_poly, e_mu, mono_coeff, kappa
from fractions import Fraction
from itertools import permutations

def solve(M, rhs):
    """exact Gaussian elimination over Q; M is list of rows"""
    n = len(M); m = len(M[0])
    A = [row[:] + [rhs[i]] for i, row in enumerate(M)]
    piv = []
    r = 0
    for cidx in range(m):
        p = next((i for i in range(r, n) if A[i][cidx] != 0), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]
        pv = A[r][cidx]
        A[r] = [v / pv for v in A[r]]
        for i in range(n):
            if i != r and A[i][cidx] != 0:
                f = A[i][cidx]
                A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        piv.append(cidx); r += 1
        if r == n: break
    sol = [Fraction(0)] * m
    for i, cidx in enumerate(piv): sol[cidx] = A[i][m]
    # consistency
    for i in range(r, n):
        if A[i][m] != 0: raise ArithmeticError("inconsistent: not in e-span")
    return sol

_cache = {}
def e_expand_num(P, n, N):
    key = (n, N)
    parts = list(partitions(n))
    if key not in _cache:
        enus = {nu: e_mu(nu, N) for nu in parts}
        M = [[mono_coeff(enus[nu], mu, N).get(0, Fraction(0)) for nu in parts] for mu in parts]
        _cache[key] = M
    M = _cache[key]
    rhs = [mono_coeff(P, mu, N).get(0, Fraction(0)) for mu in parts]
    sol = solve(M, rhs)
    return dict(zip(parts, sol))

def run(lam, tval, N=None, verbose=True):
    star.set_t(Fraction(tval)); _cache.clear()
    n = sum(lam); N = N or n
    parts = list(partitions(n))
    lamS = tuple(sorted(lam, reverse=True))
    kap = {mu: kappa(lamS, mu) for mu in parts}
    stats = dict(k1_ok=0, k1_bad=0, kviol=0, knonzero=0, k2_diff=0, k2_tot=0,
                 ord_diff=0, fails=[], viols=[])
    base = None
    for order in sorted(set(permutations(lam))):
        a, b, c = order
        ec = e_poly(c, N); eb = e_poly(b, N)
        # LHS: [u^2] of E_a E_b E_c(1),  u = s-1
        lhs_poly = p_zero()
        for q in range(3):
            Fq = E_k_p(ec, b, q, N)
            if p_is_zero(Fq): continue
            p_ = 2 - q
            G = E_k_p(Fq, a, p_, N)
            if not p_is_zero(G): lhs_poly = p_add(lhs_poly, G)
        lhs = e_expand_num(lhs_poly, n, N)
        # RHS
        Ea2_bc = E_k_p(p_mul(eb, ec), a, 2, N)
        Ea2_c  = E_k_p(ec, a, 2, N)
        Ea2_b  = E_k_p(eb, a, 2, N)
        Gamma = p_sub(p_sub(Ea2_bc, p_mul(eb, Ea2_c)), p_mul(ec, Ea2_b))
        DaDb  = E_k_p(E_k_p(ec, b, 1, N), a, 1, N)
        rhs = e_expand_num(p_add(Gamma, DaDb), n, N)
        drop = {'e_a E_b^(2)(e_c)': p_mul(e_poly(a, N), E_k_p(ec, b, 2, N)),
                'e_b E_a^(2)(e_c)': p_mul(eb, Ea2_c),
                'e_c E_a^(2)(e_b)': p_mul(ec, Ea2_b)}
        for mu in parts:
            d = lhs[mu] - rhs[mu]
            if kap[mu] == 1:
                if d == 0: stats['k1_ok'] += 1
                else:
                    stats['k1_bad'] += 1
                    stats['fails'].append((order, mu, d))
            else:
                stats['k2_tot'] += 1
                if d != 0: stats['k2_diff'] += 1
        for name, P in drop.items():
            exp = e_expand_num(P, n, N)
            for mu in parts:
                if exp[mu] != 0:
                    stats['knonzero'] += 1
                    if kap[mu] < 2:
                        stats['kviol'] += 1
                        stats['viols'].append((order, name, mu, kap[mu]))
        if base is None: base = lhs
        else: stats['ord_diff'] += sum(1 for mu in parts if base[mu] != lhs[mu])
    if verbose:
        nk1 = len([m for m in parts if kap[m] == 1])
        print(f"  lam={str(lam):10s} t={str(tval):6s} N={N} | "
              f"kappa=1: {stats['k1_ok']}/{stats['k1_ok']+stats['k1_bad']} pass ({nk1} mu) | "
              f"kappa>=2 support: {stats['knonzero']-stats['kviol']}/{stats['knonzero']} ok | "
              f"neg.ctrl kappa>=2 differ: {stats['k2_diff']}/{stats['k2_tot']} | "
              f"ord.indep diffs: {stats['ord_diff']}")
        for f in stats['fails'][:4]: print("     FAIL", f)
        for v in stats['viols'][:4]: print("     KAPPA VIOLATION", v)
    return stats

if __name__ == '__main__':
    lams = [l for l in [(2,2,1),(3,2,1),(2,2,2),(3,3,1),(3,2,2),(4,2,1),(3,3,2),(4,3,1),(3,3,3)]]
    tv = sys.argv[1] if len(sys.argv) > 1 else '5/3'
    for lam in lams:
        t0 = time.time()
        try:
            run(lam, Fraction(tv))
            print(f"     [{time.time()-t0:.1f}s]")
        except Exception as ex:
            print(f"  lam={lam} ERROR {type(ex).__name__}: {ex}  [{time.time()-t0:.1f}s]")
