"""thm:N  E_k = t^{-binom(k,2)} N o e_k o N^{-1}  on Lam_m,
with N P_nu = t^{n(nu)} s^{n(nu')} P_nu,  P_nu = Macdonald P(x; s, t^{-1}).
LHS: subset formula (printed).  RHS: Macdonald basis from Macdonald VI (3.4).
Two mechanisms, no shared code path beyond SymPy itself."""
import itertools, engine as E, macd
from sympy import simplify, cancel, expand, binomial, Integer, factor
s,t=E.s,E.t

def Nscal(nu):
    return t**E.n_stat(nu) * s**E.n_stat(E.conj(nu))

def test(m, maxdeg, Nfun=Nscal, kshift=lambda k: t**(-binomial(k,2)), label="thm:N"):
    ok=bad=0; vac=0; fails=[]
    X=E.xs(m)
    for d in range(0, maxdeg+1):
        for nu in E.partitions(d, maxlen=m) if d>0 else [()]:
            nu=tuple(nu)
            Pnu = macd.P_poly(nu,m) if nu else Integer(1)
            for k in range(1, m+1):
                if d+k > maxdeg+ (m): pass
                # LHS: E_k P_nu  (printed subset formula)
                lhs = E.E_k(Pnu, X, k)
                # RHS: t^{-C(k,2)} N ( e_k * N^{-1} P_nu )
                ek = E.e_sym(k, X)
                prod = expand(ek*Pnu)
                coeffs, badresid = macd.expand_in_P(prod, m, d+k)
                if badresid:
                    fails.append((nu,k,'P-expansion residual',badresid)); bad+=1; continue
                rhs = 0
                for kap,c in coeffs.items():
                    if c==0: continue
                    rhs += c * Nfun(kap)/Nfun(nu) * macd.P_poly(kap,m)
                rhs = cancel(expand(cancel(kshift(k)*rhs)))
                if lhs==0 and rhs==0:
                    vac+=1; ok+=1; continue
                if cancel(expand(lhs-rhs))==0: ok+=1
                else:
                    bad+=1; fails.append((nu,k,'mismatch',None))
    sys.stdout.flush()
    print(f"  {label}: m={m}, |nu|<={maxdeg}: {ok} of {ok+bad} pass, {bad} fail, {vac} vacuous (both sides 0)")
    for f in fails[:4]: print("     FAIL", f[:3])
    return ok,bad,vac

import sys
print("=== thm:N, as printed ===", flush=True)
tot=[0,0,0]
for m,md in [(2,3),(3,3),(4,2)]:
    o,b,v=test(m,md)
    tot[0]+=o; tot[1]+=b; tot[2]+=v
print(f"TOTAL thm:N: {tot[0]} of {tot[0]+tot[1]} pass, {tot[1]} fail, {tot[2]} vacuous")

print()
print("=== negative controls on thm:N (each MUST fail; a 0-failure control is blind) ===")
ctrls = [
  ("C1 swap n(nu)<->n(nu') in N",  lambda nu: t**E.n_stat(E.conj(nu))*s**E.n_stat(nu), lambda k: t**(-binomial(k,2))),
  ("C2 swap s<->t in N",           lambda nu: s**E.n_stat(nu)*t**E.n_stat(E.conj(nu)), lambda k: t**(-binomial(k,2))),
  ("C3 drop the t^{-C(k,2)}",      Nscal,                                              lambda k: Integer(1)),
  ("C4 prefactor s^{-C(k,2)}",     Nscal,                                              lambda k: s**(-binomial(k,2))),
  ("C5 N trivial (identity)",      lambda nu: Integer(1),                              lambda k: t**(-binomial(k,2))),
]
for lab,nf,kf in ctrls:
    o,b,v = test(3,2,Nfun=nf,kshift=kf,label=lab)
