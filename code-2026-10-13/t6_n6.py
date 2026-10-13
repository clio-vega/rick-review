import sys,time,sympy
sys.path.insert(0,'/home/clio/projects/reviews/code-2026-10-13')
from t3_star import (FF,s,t,ONE,ZERO,partitions,conj,nstat,star_lambda_M1,star_lambda_M2)
import t2_dmatrix as D
ss,tt=sympy.symbols('s t')
print("EXTENSION of checks 3.1 and 3.4 to n=6, plus thm:DS's d(0)=1 and support claims")
t0=time.time(); ok31=t31=ok34=t34=0; ok0=t0c=0; oksup=tsup=0
for n in [6]:
    for lam in partitions(n):
        A=star_lambda_M1(lam); B=star_lambda_M2(lam)
        t31+=1
        if A==B: ok31+=1
        else: print("  3.1 MISMATCH",lam)
        dH=D.d_by_H3(lam)
        for mu in partitions(n):
            c=A.get(mu,ZERO)
            # support: c != 0 iff mu >= lam in dominance  (thm:DS)
            dom = D.dominates(mu,lam)
            tsup+=1
            if (c!=ZERO)==dom: oksup+=1
            else: print("  SUPPORT FAIL",lam,mu,"dominates=",dom,"c=",sympy.factor(c.as_expr()) if c!=ZERO else 0)
            ex=sympy.expand(sympy.simplify(c.as_expr()/ss**nstat(mu))) if c!=ZERO else sympy.Integer(0)
            lead=sympy.expand(ex.subs(ss,0))
            pred=sympy.expand(dH.get(mu,D.ZERO).as_expr()) if mu in dH else sympy.Integer(0)
            t34+=1
            if sympy.simplify(lead-pred)==0: ok34+=1
            else: print("  3.4 FAIL",lam,mu,lead,pred)
            if dom:
                t0c+=1
                if sympy.simplify(sympy.expand(lead).subs(tt,0)-1)==0: ok0+=1
                else: print("  d(0)=1 FAIL",lam,mu,lead)
        print("   lam=%s done (%.1fs)"%(lam,time.time()-t0))
print()
print("3.1  M1(Hikita Y-ops) == M2(subset formula), lam |- 6 : %d / %d"%(ok31,t31))
print("3.4  [s^{n(mu)}]c_{lam,mu} == H(3)-iteration        : %d / %d"%(ok34,t34))
print("thm:DS support = dominance up-set of lam           : %d / %d"%(oksup,tsup))
print("thm:DS  d_{lam,mu}(0) = 1 for mu >= lam            : %d / %d"%(ok0,t0c))
