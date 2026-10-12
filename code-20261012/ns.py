"""prop:NS  gamma-hat x_i gamma-hat^{-1} = Y_i  on Pol, via the E_lambda eigenbasis of thm:C3.
Builds E_lambda by triangularising Z = sum_i c^{i-1} Y^o_i, exactly as thm:C3's proof does,
then checks the Gaussian conjugation. Also runs the three wrong Gaussians."""
import itertools
from sympy import symbols, cancel, expand, Integer, Rational, Poly, Matrix, binomial, factor
import engine as E
s,t=E.s,E.t

def monos(m,d):
    return [e for e in itertools.product(range(d+1),repeat=m) if sum(e)==d]
def mono(X,e):
    r=Integer(1)
    for v,k in zip(X,e): r*=v**k
    return r
def rk(lam,i):
    return sum(1 for j in range(len(lam)) if lam[j]>lam[i])+sum(1 for j in range(i) if lam[j]==lam[i])
def yvec(lam):
    return tuple(s**lam[i]*t**rk(lam,i) for i in range(len(lam)))
def theta(a,r):  return s**(a*(a-1)//2)*t**(a*r)
def gamma(lam):
    g=Integer(1)
    for i in range(len(lam)): g*=theta(lam[i],rk(lam,i))
    return g

def eigenbasis(m,d):
    """E_lambda = x^lambda + lower, eigenvector of every Y^o_i"""
    X=E.xs(m); ms=monos(m,d)
    # matrix of Y^o_i in the monomial basis
    cols={}
    for e in ms:
        cols[e]={}
        for i in range(1,m+1):
            img=expand(cancel(E.Yop(mono(X,e),X,i,twisted=False)))
            P=Poly(img,*X)
            cols[e][i]={f:P.coeff_monomial(f) for f in ms}
    out={}
    for lam in ms:
        # solve for v with v[lam]=1 and Y^o_i v = y_i(lam) v for all i, supported on ms
        # use the single operator Z with generic c to get a 1-dim eigenspace
        c=Rational(7,3)
        Zmat=Matrix([[sum(c**(i-1)*cols[e][i][f] for i in range(1,m+1)) for e in ms] for f in ms])
        zl=sum(c**(i-1)*yvec(lam)[i-1] for i in range(1,m+1))
        M=Zmat-zl*Matrix.eye(len(ms))
        ns=M.nullspace()
        pick=None
        for v in ns:
            if cancel(v[ms.index(lam)])!=0: pick=v; break
        if pick is None: continue
        pick=pick/pick[ms.index(lam)]
        out[lam]=expand(sum(cancel(pick[j])*mono(X,ms[j]) for j in range(len(ms))))
    return out,ms

print("=== prop:NS  gamma-hat x_i gamma-hat^{-1} = Y_i ===")
tot_ok=tot_bad=0
for m in [2,3]:
    X=E.xs(m)
    for d in [0,1,2]:
        eb,ms=eigenbasis(m,d)
        if d+1>3 and m>2: continue
        eb2,ms2=eigenbasis(m,d+1)
        for lam,El in eb.items():
            # gamma-hat x_i gamma-hat^{-1} E_lam = gamma(lam)^{-1} * gamma-hat ( x_i E_lam )
            for i in range(1,m+1):
                prod=expand(X[i-1]*El)
                P=Poly(prod,*X)
                # apply gamma-hat in the degree d+1 eigenbasis
                coef={}
                rem=dict((f,P.coeff_monomial(f)) for f in ms2)
                # expand prod in eigenbasis eb2 (triangular in prec; solve linear system)
                A=Matrix([[Poly(eb2[mu],*X).coeff_monomial(f) for mu in ms2 if mu in eb2] for f in ms2])
                keys=[mu for mu in ms2 if mu in eb2]
                b=Matrix([[rem[f]] for f in ms2])
                sol=A.solve(b)
                lhs=expand(sum(cancel(sol[j])*gamma(keys[j])*eb2[keys[j]] for j in range(len(keys))))
                lhs=cancel(lhs/gamma(lam))
                rhs=expand(cancel(E.Yop(El,X,i,twisted=True)))
                if cancel(expand(lhs-rhs))==0: tot_ok+=1
                else:
                    tot_bad+=1
                    if tot_bad<4: print("   FAIL m=%s d=%s lam=%s i=%s"%(m,d,lam,i))
    print(f"  m={m}: cumulative {tot_ok} pass, {tot_bad} fail", flush=True)
print(f"prop:NS: {tot_ok} of {tot_ok+tot_bad} pass, {tot_bad} fail")

print()
print("=== the three wrong Gaussians s^{+-C(a,2)} t^{+-ar} must fail already in degree 1 ===")
m=3; X=E.xs(m)
for (sg_s,sg_t,lab) in [(1,-1,"s^{+C(a,2)} t^{-ar}"),(-1,1,"s^{-C(a,2)} t^{+ar}"),(-1,-1,"s^{-C(a,2)} t^{-ar}")]:
    def gam(lam, a=sg_s, b=sg_t):
        g=Integer(1)
        for i in range(len(lam)):
            g*= s**(a*(lam[i]*(lam[i]-1)//2))*t**(b*lam[i]*rk(lam,i))
        return g
    eb0,_=eigenbasis(m,0); eb1,ms1=eigenbasis(m,1)
    fails=0; tests=0
    for lam,El in eb0.items():
        for i in range(1,m+1):
            tests+=1
            prod=expand(X[i-1]*El)
            A=Matrix([[Poly(eb1[mu],*X).coeff_monomial(f) for mu in ms1 if mu in eb1] for f in ms1])
            keys=[mu for mu in ms1 if mu in eb1]
            b=Matrix([[Poly(prod,*X).coeff_monomial(f)] for f in ms1])
            sol=A.solve(b)
            lhs=cancel(expand(sum(cancel(sol[j])*gam(keys[j])*eb1[keys[j]] for j in range(len(keys))))/gam(lam))
            rhs=expand(cancel(E.Yop(El,X,i,twisted=True)))
            if cancel(expand(lhs-rhs))!=0: fails+=1
    print(f"  {lab:26s}: {fails} of {tests} FAIL in degree 1")
