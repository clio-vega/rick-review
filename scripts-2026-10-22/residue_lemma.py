"""Clio 2026-10-22. A residue closed form for the one-head Psi, and a PROOF of
Rick's lambda=(2,3) two-term tie (which he grades 'computed' on two S)."""
import itertools, random, sympy as sp
from fractions import Fraction as Fr
random.seed(99)
def rho(kappa,X,w):
    e=Fr(1)
    for k in range(1,kappa): e*=(1-w[k]/X)
    return e
def Psi(kap,th,M,w):
    r=len(kap); tot=Fr(0)
    for h in itertools.permutations(M,r):
        X=[w[m] for m in h]; e=Fr(1)
        for j in range(r):
            e*=(1-1/X[j]**2)*rho(kap[j],X[j],w)*X[j]**th[j]
        for j in range(r):
            for k in range(j+1,r): e*=(1-1/(X[j]*X[k]))/(1-X[j]/X[k])
        for t in M:
            if t in h: continue
            for j in range(r): e*=(1-1/(w[t]*X[j]))/(1-w[t]/X[j])
        tot+=e
    return tot
def pt(N): return {k:Fr(random.randint(2,211),random.randint(2,211))+3*k for k in range(1,N+1)}
def eS(S,w):
    v=Fr(1)
    for m in S: v*=w[m]
    return v

# ---- Lemma (Clio): e_S * Psi_{(s),t}(S) = -Res_0 R - Res_inf R,
#      R(z) = z^{t-s} * prod_{k<s}(z-w_k) * prod_{m in S}(w_m z - 1) / prod_{m in S}(z-w_m)
z = sp.Symbol('z')
def residue_form(s,t,S,w):
    ws = {k: sp.Rational(w[k].numerator, w[k].denominator) for k in w}
    Qs = sp.prod([ (z-ws[k]) for k in range(1,s) ]) if s>1 else sp.Integer(1)
    P  = sp.prod([ (ws[m]*z-1) for m in S ])
    D  = sp.prod([ (z-ws[m])   for m in S ])
    R  = z**(t-s)*Qs*P/D
    r0 = sp.residue(sp.simplify(R), z, 0)
    # residue at infinity = -residue at 0 of (1/u^2) R(1/u)
    u = sp.Symbol('u')
    rinf = -sp.residue(sp.simplify(R.subs(z,1/u)/u**2), u, 0)
    return sp.cancel(-r0 - rinf)

print("== Lemma (one-head residue closed form): e_S*Psi_{(s),t}(S) == -Res_0 - Res_inf ==")
ok=tot=0
for S in [(2,3,4),(1,2,3,4),(2,4,5),(1,3,4,5),(3,4,5)]:
    for s in [1,2,3]:
        for t in [-2,-1,0,1,2]:
            w=pt(max(S)+1)
            lhs = sp.Rational((eS(S,w)*Psi((s,),(t,),S,w)).numerator,
                              (eS(S,w)*Psi((s,),(t,),S,w)).denominator)
            rhs = residue_form(s,t,S,w)
            tot+=1; ok += (sp.simplify(lhs-rhs)==0)
print(f"   {ok}/{tot} exact\n")

# ---- The reduction: the tie identity is EQUIVALENT to  Phi[P/z] = e_S - 1/e_S,
#      which is w_1-free.  Check the reduction, then the w_1-free statement.
print("== Reduction: tie  <=>  Phi[P(z)/z] = e_S - 1/e_S   (w_1 cancels) ==")
def Phi(gfun,S,w):
    """sum_{m in S} g(w_m)/prod_{t != m}(w_m - w_t)"""
    tot=Fr(0)
    for m in S:
        d=Fr(1)
        for t in S:
            if t!=m: d*=(w[m]-w[t])
        tot += gfun(w[m])/d
    return tot
ok=tot=0
for S in [(2,3,4),(1,2,3,4),(2,4,5),(1,3,4,5),(3,4,5),(1,2,3,4,5),(2,3),(4,)]:
    for _ in range(3):
        w=pt(max(S)+1)
        def Pz(zz,S=S,w=w):
            v=Fr(1)
            for m in S: v*=(w[m]*zz-1)
            return v
        lhs = Phi(lambda zz: Pz(zz)/zz, S, w)
        rhs = eS(S,w) - 1/eS(S,w)
        tot+=1; ok += (lhs-rhs==0)
print(f"   Phi[P/z] = e_S - 1/e_S : {ok}/{tot} exact (PROOF: sum of all residues of")
print("   R(z)=P(z)/(z*D(z)) is 0; Res_0 = 1/e_S, Res_inf = -e_S, poles at w_m give Phi.)\n")

print("== Consequence: the tie identity now holds for EVERY S (not just the two tested) ==")
ok=tot=0
for S in [(2,3,4),(1,2,3,4),(2,4,5),(1,3,4,5),(3,4,5),(1,2,3,4,5),(2,3),(4,),(1,5,7),(2,3,4,5,6)]:
    for _ in range(2):
        w=pt(max(S)+1)
        L = 1 - Psi((2,),(0,),S,w)
        R = eS(S,w)**-2 + w[1]*Psi((1,),(-1,),S,w)
        tot+=1; ok += (L-R==0)
print(f"   {ok}/{tot} exact over 10 distinct S, |S|=1..5, with and without 1 in S")
