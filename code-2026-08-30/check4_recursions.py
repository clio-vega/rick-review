from core import *
import pickle
Psi = {b: sp.sympify(v) for b,v in pickle.load(open('psi.pkl','rb')).items()}
BMAX=7
cnt={}
def rec(name,ok):
    cnt[name]=cnt.get(name,[0,0]); cnt[name][0]+=1; cnt[name][1]+=(1 if ok else 0)
    if not ok: print("   *** FAIL",name)

# --- K5 in the RATIONAL form the brief asks about, plus the pair-grouping proof
S = sum(u**2*(sum(U)-u)*(sp.Rational(1,1)/(u-v)+sp.Rational(1,1)/(u-w))
        for u,v,w in [(u1,u2,u3),(u2,u1,u3),(u3,u1,u2)])
rec('K5 rational sum = 3e2', sp.simplify(sp.together(S) - 3*e2)==0)
for (a,bb,c) in [(u1,u2,u3),(u1,u3,u2),(u2,u3,u1)]:
    pair = (a**2*(bb+c) - bb**2*(a+c))/(a-bb)
    rec('K5 pair-grouping: each pair = e2', sp.simplify(sp.cancel(pair)-e2)==0)

# --- FULL Psi-recursion
sig = sigma_E
for b in range(0,BMAX):
    rhs = sp.expand((E2s-(b+1)*E1s+(b+1)**2)*Psi[b])
    if b>=1: rhs -= sp.expand(3*b*E3s*sig(Psi[b-1]))
    if b>=2: rhs -= sp.expand(b*(b-1)*(E1s-2*b-2)*E3s*sig(Psi[b-2]))
    rec('full Psi-recursion', sp.expand(rhs-Psi[b+1])==0)

# --- weight bound
for b in range(BMAX+1):
    rec('weight bound w(Psi_b)<=b', wmax(Psi[b])<=b)
    rec('weight EXACTLY b (E2^b coeff = 1)', sp.Poly(Psi[b],E1s,E2s,E3s).coeff_monomial(E2s**b)==1)

# --- sigma_top: is it really the associated graded of sigma?
for b in range(BMAX+1):
    P = Psi[b]
    for w,part in weight_parts(P).items():
        rec('sigma_top = gr(sigma) on each weight slice',
            sp.expand(wslice(sig(part),w) - sigma_top(part))==0)

# --- top-weight recursion
tops = {b: top(Psi[b]) for b in range(BMAX+1)}
for b in range(0,BMAX):
    rhs = sp.expand((E2s-(b+1)*E1s)*tops[b])
    if b>=1: rhs -= sp.expand(3*b*E3s*sigma_top(tops[b-1]))
    if b>=2: rhs -= sp.expand(b*(b-1)*E1s*E3s*sigma_top(tops[b-2]))
    rec('top-weight recursion', sp.expand(rhs-tops[b+1])==0)

# --- SHIFT-ODE  (1+E1 T)F' = (E2-E1)F - E3 T(3+E1 T) Ftilde
N=BMAX+1
F = sum(tops[b]*Tv**b/sp.factorial(b) for b in range(N))
Ft = sigma_top(F)
lhs = sp.expand((1+E1s*Tv)*sp.diff(F,Tv))
rhs = sp.expand((E2s-E1s)*F - E3s*Tv*(3+E1s*Tv)*Ft)
d = sp.Poly(sp.expand(lhs-rhs),Tv)
bad=[m[0] for m,c in zip(d.monoms(),d.coeffs()) if m[0]<=BMAX-1 and sp.expand(c)!=0]
rec('SHIFT-ODE (orders 0..%d)'%(BMAX-1), not bad)

# --- Rick's ERRATA FIX: A characterised by (1+E1T)A'=(E2-E1)A, A_n = prod(E2-rE1)
A = sum(sp.prod([E2s-r*E1s for r in range(1,k+1)])*Tv**k/sp.factorial(k) for k in range(N+1))
dA = sp.Poly(sp.expand((1+E1s*Tv)*sp.diff(A,Tv)-(E2s-E1s)*A),Tv)
rec('errata fix: A ODE, no E1 division',
    not [m[0] for m,c in zip(dA.monoms(),dA.coeffs()) if m[0]<=N-1 and sp.expand(c)!=0])

# --- THE PIECE RICK ASSERTED WITHOUT DOING: M side, division-free
M = sum(sp.Integer(-1)**(n-1)*sp.Rational(n*n-1,n)*E1s**(n-2)*Tv**n for n in range(2,N+4))
dM = sp.Poly(sp.expand((1+E1s*Tv)**3*sp.diff(M,Tv) + Tv*(3+E1s*Tv)),Tv)
rec('errata gap: (1+E1T)^3 M\' = -T(3+E1T) over Q[E1][[T]]',
    not [m[0] for m,c in zip(dM.monoms(),dM.coeffs()) if m[0]<=N and sp.expand(c)!=0])

# --- Atilde = A/(1+E1T)^2  division-free (unit denominator)
inv2 = sp.series(1/(1+E1s*Tv)**2, Tv, 0, N+1).removeO()
At = sigma_top(A)
dAt = sp.Poly(sp.expand(At - sp.expand(A*inv2)),Tv)
rec('Atilde = A (1+E1T)^-2', not [m[0] for m,c in zip(dAt.monoms(),dAt.coeffs()) if m[0]<=N-1 and sp.expand(c)!=0])

# --- final 3-term recursion from the cubic ODE
for b in range(0,BMAX):
    r = sp.expand((E2s-(3*b+1)*E1s)*tops[b])
    if b>=1: r += sp.expand(b*(2*E1s*E2s-(3*b-1)*E1s**2-3*E3s)*tops[b-1])
    if b>=2: r += sp.expand(b*(b-1)*(E1s**2*E2s-(b-1)*E1s**3-E1s*E3s)*tops[b-2])
    rec('cubic-ODE 3-term recursion', sp.expand(r-tops[b+1])==0)

print()
for k,(n,g) in sorted(cnt.items()): print(f"  {k:52s} {g}/{n}")
