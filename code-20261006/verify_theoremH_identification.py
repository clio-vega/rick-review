"""
DECISIVE independent check of Rick's Theorem H Corollary IDENTIFICATION:

    d_{lam mu}(t) := [s^{n(mu)}] c_{lam mu}     (from the ACTUAL Hikita star)
        ?=  t^{-n(lam')} sum_nu K_{nu' lam} Ktilde_{nu mu'}(t)   (Kostka composite)

LHS computed with Clio's OWN implementation of Hikita's star
(reviews/code-2026-09-16/hikita_star_clio.py, built from arXiv:2503.23597 source,
sharing no code with Rick's scripts).  RHS computed from cocharge Kostka-Foulkes.
Rick's s = q^{-1}.
"""
import sys, sympy as sp
sys.path.insert(0, '/home/clio/projects/reviews/code-2026-09-16')
import hikita_star_clio as H
from kostka_d_matrix import partitions, conj, kostka, n_stat, kostka_foulkes_tilde, dominates

t_s = sp.symbols('t'); q_s = sp.symbols('q'); s_s = sp.symbols('s')

def e_star_lambda(lam, m):
    """e_lam1 star ... star e_lamL  (= E_lam1 ... E_lamL (1)), in the e-basis."""
    A = {tuple([0]*m): H.ONE}            # the constant 1
    for k in reversed(list(lam)):
        A = H.scal((H.ONE/H.t)**(k*(k-1)//2), H.e_Y(k, A, m))
    return H.expand_in_e(A, sum(lam), m)

def ff_to_sympy(c):
    """Convert a sympy-field element in QQ(q,t) to a sympy expression."""
    return sp.sympify(str(c)).subs({sp.Symbol('q'): q_s, sp.Symbol('t'): t_s})

def coeff_s_power(cexpr, power):
    """Coefficient of s^power in cexpr, where s = 1/q."""
    e = sp.simplify(cexpr.subs(q_s, 1/s_s))
    e = sp.cancel(sp.together(e))
    num, den = sp.fraction(e)
    e = sp.expand(sp.cancel(num/den))
    return sp.simplify(sp.expand(e).coeff(s_s, power))

print("n  lam        mu         d_star (from Hikita star)      d_kostka        match")
print("-"*96)
agree = disagree = 0
for n in range(1, 5):
    m = n
    parts = [p for p in partitions(n)]
    # RHS cache
    Kt = {}
    for nu in parts:
        for kap in parts:
            Kt[(nu,kap)] = kostka_foulkes_tilde(nu, kap)
    for lam in parts:
        if lam[0] > m: continue
        try:
            C = e_star_lambda(lam, m)
        except AssertionError as ex:
            print(f"  n={n} lam={lam}: expand_in_e failed: {ex}"); continue
        for mu in parts:
            c = C.get(mu)
            cexp = ff_to_sympy(c) if c is not None else sp.Integer(0)
            d_star = coeff_s_power(cexp, n_stat(mu)) if c is not None else sp.Integer(0)
            rhs = sp.Integer(0)
            for nu in parts:
                k = kostka(conj(nu), lam)
                if k: rhs += k * Kt[(nu, conj(mu))]
            d_kos = sp.simplify(sp.expand(rhs * t_s**(-n_stat(conj(lam)))))
            ok = sp.simplify(sp.expand(d_star - d_kos)) == 0
            agree += ok; disagree += (not ok)
            flag = "OK" if ok else "**MISMATCH**"
            print(f"{n}  {str(lam):10s} {str(mu):10s} {str(d_star):28s} {str(d_kos):15s} {flag}")
print("-"*96)
print(f"AGREE {agree}   DISAGREE {disagree}")
