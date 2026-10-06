"""
THE SOBER NORMALIZATION CHECK Rick flagged as owed (novelty audit 2026-10-01 §5b).

Kirillov math/9803006 §3.2 (as quoted by Rick):
    R_{lam mu}(t) = sum_eta K_{eta mu} K_{eta' lam}(t)
    and  e_lam = sum_mu M(e,P)_{lam mu} P_mu   with
         M(e,P)_{lam mu} = sum_nu K_{nu lam} K_{nu' mu}(t) = R_{mu lam}(t)

Rick's Corollary:
    d_{lam mu}(t) = t^{-n(lam')} sum_nu K_{nu' lam} Ktilde_{nu mu'}(t)

QUESTION: is Rick's d the SAME matrix as Kirillov's M(e,P)/R, and under WHICH
index and parameter substitution?  Rick's flag: "(t vs t^-1, P vs Q', mu vs mu')".
"""
import sympy as sp
from kostka_d_matrix import (partitions, conj, kostka, n_stat,
                             kostka_foulkes, kostka_foulkes_tilde, dominates)
t = sp.symbols('t')

def rick_d(lam, mu, parts, KT):
    s = sp.Integer(0)
    for nu in parts:
        k = kostka(conj(nu), lam)
        if k: s += k * KT[(nu, conj(mu))]
    return sp.simplify(sp.expand(s * t**(-n_stat(conj(lam)))))

def kirillov_M(lam, mu, parts, KF):
    """M(e,P)_{lam mu} = sum_nu K_{nu lam} K_{nu' mu}(t)   (Kirillov, verbatim form)"""
    s = sp.Integer(0)
    for nu in parts:
        k = kostka(nu, lam)
        if k: s += k * KF[(conj(nu), mu)]
    return sp.expand(s)

def kirillov_R(lam, mu, parts, KF):
    """R_{lam mu}(t) = sum_eta K_{eta mu} K_{eta' lam}(t)"""
    s = sp.Integer(0)
    for eta in parts:
        k = kostka(eta, mu)
        if k: s += k * KF[(conj(eta), lam)]
    return sp.expand(s)

for n in range(2, 6):
    parts = list(partitions(n))
    KF = {}; KT = {}
    for a in parts:
        for b in parts:
            KF[(a,b)] = kostka_foulkes(a,b)
            KT[(a,b)] = kostka_foulkes_tilde(a,b)
    print("="*78); print(f"n = {n}")
    # candidate relations to test
    tests = {
      "d_{lam mu}(t) == M(e,P)_{lam mu'}(t)"        : lambda l,m: (rick_d(l,m,parts,KT), kirillov_M(l,conj(m),parts,KF)),
      "d_{lam mu}(t) == M(e,P)_{lam mu}(t)"         : lambda l,m: (rick_d(l,m,parts,KT), kirillov_M(l,m,parts,KF)),
      "d_{lam mu}(1/t) == M(e,P)_{lam mu'}(t)"      : lambda l,m: (sp.simplify(rick_d(l,m,parts,KT).subs(t,1/t)), kirillov_M(l,conj(m),parts,KF)),
      "d_{lam mu}(t) == R_{mu' lam}(t)"             : lambda l,m: (rick_d(l,m,parts,KT), kirillov_R(conj(m),l,parts,KF)),
    }
    for name, f in tests.items():
        agree = total = 0
        for lam in parts:
            for mu in parts:
                a,b = f(lam,mu)
                total += 1
                if sp.simplify(sp.expand(a-b)) == 0: agree += 1
        print(f"  {name:42s}: {agree}/{total}" + ("  <-- IDENTITY" if agree==total else ""))
