import sympy as sp
from kostka_d_matrix import *

def d_variant(n, conj_first=True, conj_second=True):
    parts = list(partitions(n)); out={}
    for lam in parts:
        for mu in parts:
            s = sp.Integer(0)
            for nu in parts:
                a = kostka(conj(nu), lam) if conj_first else kostka(nu, lam)
                if not a: continue
                second = conj(mu) if conj_second else mu
                s += a * kostka_foulkes_tilde(nu, second)
            out[(lam,mu)] = sp.expand(sp.simplify(s * t**(-n_stat(conj(lam)))))
    return parts, out

print("=== RANK / NON-VACUITY of the 209-pair check ===")
for n in range(2,7):
    parts, D = d_variant(n)
    nz   = sum(1 for k,v in D.items() if v != 0)
    nonconst = sum(1 for k,v in D.items() if v != 0 and sp.Poly(v,t).degree() > 0)
    dom  = sum(1 for lam in parts for mu in parts if dominates(mu,lam))
    deg  = max((sp.Poly(v,t).degree() for v in D.values() if v!=0), default=0)
    distinct = len({sp.srepr(sp.expand(v)) for v in D.values()})
    print(f" n={n}: pairs={len(parts)**2:4d} nonzero={nz:4d} nonconstant={nonconst:4d} "
          f"dominance-pairs={dom:4d} maxdeg={deg:2d} distinct-values={distinct}")

print("\n=== NEGATIVE CONTROLS: break a conjugate, checks must FAIL ===")
for label, cf, cs in [("K_{nu lam} (drop ' on nu)", False, True),
                      ("Ktilde_{nu mu} (drop ' on mu)", True, False),
                      ("both conjugates dropped", False, False)]:
    n=5
    parts, D = d_variant(n, cf, cs)
    neg=bad1=0; tot=0
    for lam in parts:
        for mu in parts:
            v=D[(lam,mu)]; tot+=1
            if v!=0:
                p=sp.Poly(v,t)
                if any(c<0 for c in p.all_coeffs()): neg+=1
            if sp.simplify(v.subs(t,1) - count_01_matrices(lam, conj(mu))) != 0: bad1+=1
    print(f"  variant [{label}]: n=5 negcoeff={neg}/{tot}  d(1)!=M in {bad1}/{tot}  "
          f"=> {'FAILS (control fired)' if (neg or bad1) else 'PASSES -- CHECK IS BLIND'}")
