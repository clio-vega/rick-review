from core import *
import random, pickle
Psi = {b: sp.sympify(v) for b,v in pickle.load(open('psi.pkl','rb')).items()}
def rnd(deg=4,n=8):
    """random polynomials in u1,u2,u3"""
    out=[]
    for _ in range(n):
        f=sp.Integer(0)
        for _ in range(6):
            f += random.randint(-4,4)*u1**random.randint(0,deg)*u2**random.randint(0,deg)*u3**random.randint(0,deg)
        out.append(sp.expand(f))
    return out
tests = rnd(4,10)
E = lambda f: sp.expand(D(0,f)+D(1,f)+D(2,f))
e2D = lambda f: sp.expand(D(0,D(1,f))+D(0,D(2,f))+D(1,D(2,f)))
cnt={}
def rec(name,ok):
    cnt[name]=cnt.get(name,[0,0]); cnt[name][0]+=1; cnt[name][1]+= (1 if ok else 0)
    if not ok: print("   *** FAIL", name)

# (I1)
for f in tests:
    for i in range(3):
        rec('I1', sp.expand(Tmap(U[i]*f) - (U[i]*Tmap(f) - Tmap(D(i,f))))==0)
# T(u_i X) = u_i sigma_i T(X)   (the form actually used in I2)
for f in tests:
    for i in range(3):
        s = Tmap(f).subs({U[i]:U[i]-1})
        rec('I2a: T(u_i X)=u_i sig_i T(X)', sp.expand(Tmap(U[i]*f) - U[i]*sp.expand(s))==0)
# (T-Id)
for f in tests:
    lhs = Tmap(e2*f)
    rhs = e2*Tmap(f)
    for i in range(3):
        j,k = [x for x in range(3) if x!=i]
        rhs -= U[i]*Tmap(D(j,f)+D(k,f))
    rhs += Tmap(e2D(f))
    rec('T-Id', sp.expand(lhs-rhs)==0)
# (I2)
for f in tests:
    rec('I2', sp.expand(Tmap(e3*f) - e3*sigma(Tmap(f)))==0)
# (I3),(I4) on symmetric f
symtests = [sp.Integer(1), e1, e2, e3, e2**2, e1*e2, e2**3, e1*e3, e2*e3, e1**2*e2, e2**2*e3]
for f in symtests:
    rec('I3', sp.expand(Psi_u(e1*f) - ((e1-3)*Psi_u(f) - Psi_u(E(f))))==0)
    rec('I4', sp.expand(Psi_u(e3*f) - e3*sigma(Psi_u(f)))==0)
# (I3) corollary on e_2^b
for b in range(6):
    rec('I3-cor', sp.expand(to_E(Psi_u(e1*e2**b)) - (E1s-2*b-3)*Psi[b])==0)
# (I4) corollary Psi(e1 e3 e2^{b-2})
for b in range(2,7):
    lhs = to_E(Psi_u(e1*e3*e2**(b-2)))
    rhs = sp.expand((E1s-2*b-2)*E3s*sigma_E(Psi[b-2]))
    rec('I3I4-cor', sp.expand(lhs-rhs)==0)
# (K1)-(K5)
for b in range(0,6):
    f = sp.expand(e2**b*V)
    S = sp.Integer(0)
    for i in range(3):
        j,k=[x for x in range(3) if x!=i]
        S += U[i]*(D(j,f)+D(k,f))
    rhs = (2*b+1)*e1*e2**b*V - (b*(e1*e2-3*e3)*e2**(b-1)*V if b>=1 else 0)
    rec('K1', sp.expand(S-rhs)==0)
rec('K2', sp.expand(sum(D(a,D(bb,e2)) for a in range(3) for bb in range(3) if a<bb) - e2)==0)
rec('K3', sp.expand(sum(D(a,e2)*D(bb,e2) for a in range(3) for bb in range(3) if a<bb) - (e2**2+e1*e3))==0)
rec('K4', sp.expand(sum(D(a,D(bb,V)) for a in range(3) for bb in range(3) if a<bb) - 2*V)==0)
Q = sp.expand(sum(D(a,e2)*D(bb,V) for a in range(3) for bb in range(3) if a!=bb))
rec('K5: Q=3e2V', sp.expand(Q-3*e2*V)==0)
rec('K5b: sum_a D_a(e2)D_a(V)=3e2V', sp.expand(sum(D(a,e2)*D(a,V) for a in range(3))-3*e2*V)==0)
# A_b := e2(D)(e2^b V)/V
for b in range(0,7):
    lhs = sp.cancel(e2D(sp.expand(e2**b*V))/V)
    rhs = (b+1)*(b+2)*e2**b + (b*(b-1)*e1*e3*e2**(b-2) if b>=2 else 0)
    rec('A_b coefficient (b+1)(b+2)', sp.expand(lhs-rhs)==0)
# THE FALSE-START LINE in 2.2, as literally written, is wrong:
b=sp.Symbol('b')
print("\n  false-start line coefficient of e2^b:  b(b-1) + (b^2+3b+2) =", sp.expand(b*(b-1)+b**2+3*b+2))
print("  correct coefficient:                   (b+1)(b+2)          =", sp.expand((b+1)*(b+2)))
print()
for k,(n,g) in sorted(cnt.items()): print(f"  {k:38s} {g}/{n}")
