"""Rem 6.4, first claim: E_k = t^{k(m-k)} M_{k;1}, where M_{k;1} is DFK19 eq (1.5)
with (q,t)_DFK = (s, t^{-1}) and N = m.

DFK (1.5), from Clio's own verified-quote record of 1704.00154 (resolved from master.aux,
2026-10-02):   M_{alpha;n} = sum_{|I|=alpha} x_I^n prod_{i in I, j notin I} (t x_i - x_j)/(x_i-x_j) Gamma_I
with Gamma_I the q-shift on the variables in I."""
import itertools
from sympy import cancel, expand, Integer, simplify, binomial
import engine as E
s,t=E.s,E.t

def M_DFK(f,X,alpha,n,qD,tD):
    """DFK eq (1.5): M_{alpha;n}, Gamma_I = shift x_i -> qD x_i for i in I"""
    m=len(X); tot=0
    for I in itertools.combinations(range(m),alpha):
        xI=Integer(1)
        for i in I: xI*=X[i]
        pref=Integer(1)
        for i in I:
            for j in range(m):
                if j not in I: pref*=(tD*X[i]-X[j])/(X[i]-X[j])
        tot += xI**n * pref * f.subs({X[i]:qD*X[i] for i in I},simultaneous=True)
    return cancel(expand(cancel(tot)))

print("=== E_k  ==  t^{k(m-k)} M_{k;1}   with (q,t)_DFK=(s,t^{-1}), N=m ===")
ok=bad=0
for m in [2,3,4]:
    X=E.xs(m)
    for d in range(0,3):
        for lam in (list(E.partitions(d,maxlen=m)) if d>0 else [()]):
            f=E.mono_sym(lam,X) if lam else Integer(1)
            for k in range(1,m+1):
                lhs=E.E_k(f,X,k)
                rhs=cancel(t**(k*(m-k))*M_DFK(f,X,k,1,s,1/t))
                if cancel(expand(lhs-rhs))==0: ok+=1
                else:
                    bad+=1
                    if bad<4: print("   FAIL m=%s lam=%s k=%s"%(m,lam,k))
    print(f"  m={m}: cumulative {ok} pass, {bad} fail", flush=True)
print(f"E_k = t^{{k(m-k)}} M_{{k;1}}: {ok} of {ok+bad} pass, {bad} fail")

print()
print("=== controls (each MUST fail) ===")
for lab,expo in [("no prefactor (M_{k;1} alone)", lambda k,m: Integer(1)),
                 ("t^{-k(m-k)} instead", lambda k,m: t**(-k*(m-k))),
                 ("s^{k(m-k)} instead", lambda k,m: s**(k*(m-k)))]:
    o=b=0
    for m in [2,3]:
        X=E.xs(m)
        for d in range(0,3):
            for lam in (list(E.partitions(d,maxlen=m)) if d>0 else [()]):
                f=E.mono_sym(lam,X) if lam else Integer(1)
                for k in range(1,m+1):
                    if cancel(expand(E.E_k(f,X,k)-cancel(expo(k,m)*M_DFK(f,X,k,1,s,1/t))))==0: o+=1
                    else: b+=1
    print(f"  {lab:32s} {b} of {o+b} FAIL (ok={o})")

print()
print("=== the Thm 2.17 / (4.14) scalars, from Clio's recorded locators ===")
k,mm=E.symbols('k m') if hasattr(E,'symbols') else (None,None)
from sympy import symbols, Rational
k,mm=symbols('k m')
# Thm 2.17 (my record): tau_+(e_k(Y))|_Sym = q^{k/2} t^{-k(N-k)/2} M_{k;1}
#   => M_{k;1} = q^{-k/2} t^{+k(N-k)/2} tau_+(e_k(Y));  (q,t)->(s,t^{-1}), N->m
f_217 = s**(-k/2) * (1/t)**(k*(mm-k)/2)
# (4.14) (my record): nabla^{(N)} = C_N (t^{(N-1)/2} q^{1/2})^d (...)  ; d=k
f_414 = ((1/t)**((mm-1)/2) * s**Rational(1,2))**k
print("  from Thm 2.17 :", simplify(f_217), "  <- Rick prints t^{-k(m-k)/2} s^{-k/2}")
print("     residual   :", simplify(f_217 - t**(-k*(mm-k)/2)*s**(-k/2)))
print("  from (4.14)   :", simplify(f_414), "  <- Rick prints t^{-k(m-1)/2} s^{k/2}")
print("     residual   :", simplify(f_414 - t**(-k*(mm-1)/2)*s**(k/2)))
print("  full product  :", simplify(t**(k*(mm-k)) * f_217 * f_414), " <- must be t^{-C(k,2)}")
print("     residual   :", simplify(t**(k*(mm-k))*f_217*f_414 - t**(-k*(k-1)/2)))
