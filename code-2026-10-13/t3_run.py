import sys, time
sys.path.insert(0,'/home/clio/projects/reviews/code-2026-10-13')
import t3_star as S
from t3_star import (FF, s, t, ONE, ZERO, partitions, conj, nstat, qint, qfact,
                     star_lambda_M1, star_lambda_M2, eY, expand_in_e, _scal)
import sympy
NMAX = int(sys.argv[1]) if len(sys.argv)>1 else 5
ss, tt = sympy.symbols('s t')

print("="*74)
print("CHECK 3.1  thm:subset  --  M1 (Clio, Hikita Y-operators) vs M2 (Rick, subset formula)")
tot=ok=0; t0=time.time()
store={}
for n in range(1,NMAX+1):
    for lam in partitions(n):
        a=star_lambda_M1(lam); b=star_lambda_M2(lam)
        store[lam]=a
        tot+=1
        if a==b: ok+=1
        else:
            print("  MISMATCH",lam)
            for k_ in set(a)|set(b):
                if a.get(k_,ZERO)!=b.get(k_,ZERO):
                    print("    ",k_,"M1",a.get(k_,ZERO).as_expr(),"M2",b.get(k_,ZERO).as_expr())
    print("  n=%d done (%.1fs)"%(n,time.time()-t0))
print("  DOMAIN: all lam |- n, 1<=n<=%d   -> %d / %d agree"%(NMAX,ok,tot))

print()
print("="*74)
print("CHECK 3.2  G1: Hikita Thm 3.12 (printed, qt-CSF.tex l.883) e_1*e_r=(1-q^-1)[r+1]e_{r+1}+q^-1 e_1 e_r")
g1ok=g1tot=0
for r in range(0,NMAX):
    m=max(r+1,1)
    A={tuple([0]*m):ONE}
    if r>0:
        A=eY(r,A,m); A=_scal((ONE/t)**(r*(r-1)//2),A)
    B=eY(1,A,m)
    co=expand_in_e(B,r+1,m)
    pred={(r+1,):(ONE-s)*qint(r+1)}
    if r>0: pred[(r,1)]=s
    pred={k_:v for k_,v in pred.items() if v}
    g1tot+=1
    if co==pred: g1ok+=1
    else: print("   r=%d FAIL"%r, {k_:v.as_expr() for k_,v in co.items()}, "pred", {k_:v.as_expr() for k_,v in pred.items()})
print("  %d / %d  (r = 0..%d)"%(g1ok,g1tot,NMAX-1))

print()
print("="*74)
print("CHECK 3.3  thm:DS divisibility  s^{n(mu)} | c_{lam mu},  and support l(mu)<=l(lam)")
dv=dvt=sp=spt=0
for lam,co in store.items():
    for mu,c in co.items():
        dvt+=1
        ex=sympy.together(c.as_expr())
        q=sympy.simplify(ex/ss**nstat(mu))
        isp = sympy.Poly(sympy.expand(q),ss,tt).is_zero if q==0 else None
        try:
            P=sympy.Poly(sympy.expand(q),ss,tt); good=True
        except sympy.PolynomialError: good=False
        if good: dv+=1
        else: print("   DIVISIBILITY FAIL",lam,mu,ex)
        spt+=1
        if len(mu)<=len(lam): sp+=1
        else: print("   SUPPORT FAIL",lam,mu)
print("  s^{n(mu)} | c_{lam,mu} : %d / %d ;  l(mu)<=l(lam) : %d / %d"%(dv,dvt,sp,spt))

print()
print("="*74)
print("CHECK 3.4  cor:dmatrix   d_{lam,mu}(t) = [s^{n(mu)}] c_{lam,mu}   vs  Theorem H(3) iteration")
sys.path.insert(0,'/home/clio/projects/reviews/code-2026-10-13')
import t2_dmatrix as D
dok=dtot=0
for lam,co in store.items():
    n=sum(lam)
    dH=D.d_by_H3(lam)
    for mu in partitions(n):
        c=co.get(mu,ZERO)
        ex=sympy.expand(sympy.simplify(c.as_expr()/ss**nstat(mu)))
        lead=sympy.expand(ex.subs(ss,0))
        pred=sympy.expand(dH.get(mu,D.ZERO).as_expr()) if mu in dH else sympy.Integer(0)
        dtot+=1
        if sympy.simplify(lead-pred)==0: dok+=1
        else: print("   FAIL",lam,mu,"got",lead,"pred",pred)
print("  %d / %d  pairs (lam,mu), lam,mu |- n <= %d"%(dok,dtot,NMAX))

print()
print("="*74)
print("CHECK 3.5  G2: Hikita Lemma 6.3 (printed, l.1420)  d_{lam,(n)}(t) = [n]_t!/prod_i [lam_i]_t!")
g2ok=g2tot=0
for n in range(1,NMAX+1):
    for lam in partitions(n):
        dH=D.d_by_H3(lam)
        got=dH.get((n,),D.ZERO)
        pr=D.qfact(n)
        for p in lam: pr=pr/D.qfact(p)
        g2tot+=1
        if got==pr: g2ok+=1
        else: print("   FAIL",lam,got.as_expr(),pr.as_expr())
print("  %d / %d  lam |- n <= %d"%(g2ok,g2tot,NMAX))
