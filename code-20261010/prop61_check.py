"""
Referee check of Proposition 6.1, FPSAC draft (work-in-progress @ e44e29f).

  Prop 6.1.  If (a,b,c) is any ordering of lambda and kappa(lambda,mu)=1, then
             [(s-1)^2] c_{lambda mu} = [e_mu]( Gamma_a(e_b,e_c) + D_a D_b(e_c) ).

  Gamma_a(e_b,e_c) := E_a^{(2)}(e_b e_c) - e_b E_a^{(2)}(e_c) - e_c E_a^{(2)}(e_b)
  D_k := E_k^{(1)}   (Theorem 3.2)

Both sides are computed from the PRINTED subset formula (Prop 2.1) + (2.1) only.
"""
import sys, time
sys.path.insert(0, '/home/clio/projects/reviews/code-20261010')
from star import *
from symfun import *
import sympy
from itertools import permutations

u = sympy.Symbol('u')   # u = s-1
t = sympy.Symbol('t')

def star_lambda_taylor(a, b, c, N, maxp=3):
    """e^*_{(a,b,c)} = E_a E_b E_c(1) as {power of u : poly}, using
       E_c(1)=e_c  (since E_c^{(r)}(1)=0 for r>=1)."""
    ec = e_poly(c, N)
    out = {}
    for q in range(maxp+1):
        Fq = E_k_p(ec, b, q, N)
        if p_is_zero(Fq): continue
        for p in range(maxp+1-q):
            G = E_k_p(Fq, a, p, N)
            if p_is_zero(G): continue
            out[p+q] = p_add(out.get(p+q, {}), G)
    return out

def report(lam, N=None, maxp=3):
    n = sum(lam)
    if N is None: N = n
    print(f"\n{'='*70}\nlambda = {lam}, n = {n}, N = {N}")
    parts = list(partitions(n))
    kap = {mu: kappa(tuple(sorted(lam, reverse=True)), mu) for mu in parts}

    results = {}
    for order in sorted(set(permutations(lam))):
        a, b, c = order
        T = star_lambda_taylor(a, b, c, N, maxp)
        lhs_poly = T.get(2, {})
        lhs = e_expand(lhs_poly, n, N)

        # RHS pieces
        ec = e_poly(c, N); eb = e_poly(b, N); ebec = p_mul(eb, ec)
        Ea2_bc = E_k_p(ebec, a, 2, N)
        Ea2_c  = E_k_p(ec,  a, 2, N)
        Ea2_b  = E_k_p(eb,  a, 2, N)
        Gamma  = p_sub(p_sub(Ea2_bc, p_mul(eb, Ea2_c)), p_mul(ec, Ea2_b))
        DaDb   = E_k_p(E_k_p(ec, b, 1, N), a, 1, N)
        rhs = e_expand(p_add(Gamma, DaDb), n, N)

        # the three terms the proof idea claims have kappa >= 2
        drop = {
            'e_a E_b^{(2)}(e_c)': p_mul(e_poly(a,N), E_k_p(ec, b, 2, N)),
            'e_b E_a^{(2)}(e_c)': p_mul(eb, Ea2_c),
            'e_c E_a^{(2)}(e_b)': p_mul(ec, Ea2_b),
        }
        results[order] = (lhs, rhs, drop)

    # ---- (i) Prop 6.1 itself, on kappa=1 ----
    ok = bad = 0
    for order, (lhs, rhs, drop) in results.items():
        for mu in parts:
            if kap[mu] != 1: continue
            d = sympy.simplify(lhs[mu] - rhs[mu])
            if d == 0: ok += 1
            else:
                bad += 1
                print(f"   FAIL order={order} mu={mu}: lhs-rhs = {d}")
    print(f" (i)  Prop 6.1 on kappa=1 : {ok}/{ok+bad} pass  "
          f"({len([m for m in parts if kap[m]==1])} such mu x {len(results)} orderings)")

    # ---- (ii) the load-bearing claim: the 3 terms are supported on kappa>=2 ----
    tot = viol = 0
    for order, (lhs, rhs, drop) in results.items():
        for name, P in drop.items():
            exp = e_expand(P, n, N)
            for mu in parts:
                if sympy.simplify(exp[mu]) != 0:
                    tot += 1
                    if kap[mu] < 2:
                        viol += 1
                        print(f"   KAPPA VIOLATION order={order} {name} mu={mu} kappa={kap[mu]}")
    print(f" (ii) 'kappa>=2' claim    : {tot} nonzero e_mu coefficients across the 3 terms x "
          f"{len(results)} orderings, {viol} with kappa<2")

    # ---- (iii) NEGATIVE CONTROL: does the identity also hold at kappa>=2? ----
    n2 = n2bad = 0
    for order, (lhs, rhs, drop) in results.items():
        for mu in parts:
            if kap[mu] < 2: continue
            n2 += 1
            if sympy.simplify(lhs[mu] - rhs[mu]) != 0: n2bad += 1
    print(f" (iii) negative control   : kappa>=2: {n2bad}/{n2} DIFFER "
          f"(want >0, else the kappa=1 hypothesis is doing no work)")

    # ---- (iv) ordering independence of the LHS (commutativity/associativity) ----
    ords = list(results)
    base = results[ords[0]][0]
    diffs = 0
    for o in ords[1:]:
        for mu in parts:
            if sympy.simplify(base[mu] - results[o][0][mu]) != 0: diffs += 1
    print(f" (iv)  LHS ordering-independent across {len(ords)} orderings: "
          f"{diffs} discrepancies (want 0)")
    return results, kap, parts

if __name__ == '__main__':
    for lam in [(1,1,1), (2,1,1), (2,2,1), (3,1,1)]:
        t0 = time.time()
        report(lam)
        print(f"   [{time.time()-t0:.1f}s]")
