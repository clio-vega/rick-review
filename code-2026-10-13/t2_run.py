import sys, time
sys.path.insert(0,'/home/clio/projects/reviews/code-2026-10-13')
from t2_dmatrix import *

def phi(r,u):
    p = FF.one
    for a in range(1,r+1): p *= (FF.one-u**a)
    return p
def blam(lam,u):
    p = FF.one
    for v,c in mult(lam).items(): p *= phi(c,u)
    return p

NMAX = int(sys.argv[1]) if len(sys.argv)>1 else 6
print("="*72)
print("CONTROL C1: Gram-Schmidt HL norms  <P_l,P_l>_u = 1/b_l(u)   [Macdonald III (4.9)]")
Pcache={}
for n in range(1,NMAX+1):
    N=n
    P,norms = HL_P(n,N,t); Pcache[n]=(P,norms,N)
    ok=sum(1 for l in norms if norms[l]*blam(l,t)==FF.one)
    print("  n=%d: %d/%d partitions   (N=%d variables)"%(n,ok,len(norms),N))
    for l in norms:
        if norms[l]*blam(l,t)!=FF.one: print("   C1 FAIL",l,norms[l],FF.one/blam(l,t))
print()

def d_by_eP(lam,mu,n):
    """t^{n(mu')-n(lam')} [P_{mu'}(x;1/t)] e_lam , P built by Gram-Schmidt in u=1/t."""
    N=n
    key=('inv',n)
    if key not in Pcache:
        Pcache[key]=HL_P(n,N,FF.one/t)+(N,)
    P,norms,_=Pcache[key]
    E=e_lambda(lam,N)
    keys=list(P.keys()); basis=[P[k] for k in keys]
    co=expand_in_basis(E,basis,keys)
    c=co.get(conj(mu),ZERO)
    return c*t**(nstat(conj(mu))-nstat(conj(lam)))

print("="*72)
print("MECHANISMS (a) H(3)-iteration  (b) e->P Gram-Schmidt  (c) K.Ktilde(charge)  (d) 0-1 at t=1")
agree_ab=agree_ac=agree_ad=tot=0; pos=0; posfail=[]
fails=[]
t0=time.time()
for n in range(1,NMAX+1):
    plist=list(partitions(n))
    for lam in plist:
        dH=d_by_H3(lam)
        for mu in plist:
            tot+=1
            a=dH.get(mu,ZERO)
            b=d_by_eP(lam,mu,n)
            c=d_by_KK(lam,mu)
            if a==b: agree_ab+=1
            else: fails.append(('ab',n,lam,mu,a,b))
            if a==c: agree_ac+=1
            else: fails.append(('ac',n,lam,mu,a,c))
            # (d) at t=1
            import sympy
            ts=sympy.Symbol('t'); ex=sympy.expand(a.as_expr())
            val=sympy.simplify(ex.subs(ts,1))
            cnt=count01(lam,conj(mu))
            if val==cnt: agree_ad+=1
            else: fails.append(('ad',n,lam,mu,val,cnt))
            # positivity: must be a POLYNOMIAL in t with nonneg integer coefficients
            if a==ZERO: pos+=1
            else:
                isden = (a.denom==FF.one.denom)
                coeffs=sympy.Poly(ex,ts).all_coeffs() if isden else [sympy.Integer(-1)]
                if isden and all(sympy.Rational(cc)>=0 and sympy.Rational(cc).q==1 for cc in coeffs): pos+=1
                else: posfail.append((n,lam,mu,ex))
    print("  n=%d done  (%.1fs, %d pairs so far)"%(n,time.time()-t0,tot))
print()
print("DOMAIN: all (lam,mu) with lam,mu |- n, 1 <= n <= %d  ==  %d ordered pairs"%(NMAX,tot))
print("(a) == (b)  e->P Gram-Schmidt          : %d / %d"%(agree_ab,tot))
print("(a) == (c)  K . Ktilde via charge      : %d / %d"%(agree_ac,tot))
print("(a)(1) == (d) 0-1 matrix count         : %d / %d"%(agree_ad,tot))
print("d_{lam,mu} in N[t] (positivity)        : %d / %d"%(pos,tot))
if fails:
    print("FAILURES (first 12):")
    for f in fails[:12]: print("   ",f)
if posfail:
    print("POSITIVITY FAILURES (first 8):")
    for f in posfail[:8]: print("   ",f)
