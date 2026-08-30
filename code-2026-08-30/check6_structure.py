from core import *
import itertools
cnt={}
def rec(name,ok):
    cnt[name]=cnt.get(name,[0,0]); cnt[name][0]+=1; cnt[name][1]+=(1 if ok else 0)
    if not ok: print("   *** FAIL",name)

# (A) T commutes with the S_3 action  => T preserves antisymmetry => Psi is WELL-DEFINED
#     (this lemma is nowhere in Rick's document, and the object does not exist without it)
import random
tests=[sp.expand(sum(random.randint(-4,4)*u1**random.randint(0,4)*u2**random.randint(0,4)*u3**random.randint(0,4)
        for _ in range(6))) for _ in range(8)]
for f in tests:
    for perm in itertools.permutations(range(3)):
        sub = {U[i]:U[perm[i]] for i in range(3)}
        rec('T commutes with S_3', sp.expand(Tmap(f.subs(sub,simultaneous=True))
                                             - Tmap(f).subs(sub,simultaneous=True))==0)
rec('T(V)=V', sp.expand(Tmap(V)-V)==0)

# (B) IDENTIFICATION: is Psi(s_mu) the factorial/shifted Schur function det((u_i)_{mu_j+3-j})/V ?
def schur(mu):
    mu = list(mu)+[0]*(3-len(mu))
    num = sp.Matrix(3,3, lambda i,j: U[i]**(mu[j]+2-j)).det()
    return sp.expand(sp.cancel(num/V))
def fac_schur(mu):
    mu = list(mu)+[0]*(3-len(mu))
    num = sp.Matrix(3,3, lambda i,j: ff(U[i], mu[j]+2-j)).det()
    return sp.expand(sp.cancel(num/V))
parts=[p for n in range(0,7) for p in
       [tuple(x) for x in [[a,b,c] for a in range(n+1) for b in range(a+1) for c in range(b+1)
                            if a+b+c==n]]]
for mu in parts:
    rec('Psi(s_mu) == factorial Schur s*_mu', sp.expand(Psi_u(schur(mu)) - fac_schur(mu))==0)

# (C) does that give Psi(e_2^b) = sum_mu <e_2^b, s_mu> s*_mu, with <e_2^b,s_mu> = K_{mu',(2^b)}?
for b in range(0,5):
    tgt = sp.expand(e2**b)
    # expand e_2^b in the Schur basis (3 variables)
    coeffs={}
    rem = tgt
    for mu in sorted([p for p in parts if sum(p)==2*b], reverse=True):
        s = schur(mu)
        # leading monomial u1^mu1 u2^mu2 u3^mu3
        c = sp.Poly(rem,u1,u2,u3).coeff_monomial(u1**mu[0]*u2**mu[1]*u3**mu[2])
        if c!=0:
            coeffs[mu]=c; rem = sp.expand(rem - c*s)
    rec('e_2^b expands in Schur basis', sp.expand(rem)==0)
    lhs = to_E(Psi_u(e2**b))
    rhs = to_E(sp.expand(sum(c*fac_schur(mu) for mu,c in coeffs.items())))
    rec('Psi(e_2^b) = sum_mu K_{mu\',(2^b)} s*_mu', sp.expand(lhs-rhs)==0)
    if b<=3: print(f"   b={b}: Schur support {dict(coeffs)}")
print()
for k,(n,g) in sorted(cnt.items()): print(f"  {k:42s} {g}/{n}")
