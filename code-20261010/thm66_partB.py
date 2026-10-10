import sys; sys.path.insert(0,'/home/clio/projects/reviews/code-20261010')
import thm66_check as M, sympy
from fractions import Fraction
from symfun import kappa
lam=(2,2,2)
print("printed Thm 6.6 vs MY subset-formula engine, lambda=(2,2,2)")
for mu in [(5,1),(3,3),(4,2)]:
    k=kappa(lam,mu)
    pr=M.printed_lead(2,2,2,mu[0],mu[1])
    print(f"  mu={mu} kappa={k} ({'IN scope' if k==1 else 'OUT of scope'}) printed={sympy.factor(pr)}")
    for tv in ['5/3','3/5','7/4']:
        mine=M.my_lead(lam,mu,Fraction(tv))
        prv=sympy.Rational(sympy.cancel(pr.subs(M.T,sympy.Rational(Fraction(tv)))))
        print(f"      t={tv:5s} mine={str(mine):18s} printed={str(prv):18s} {'MATCH' if sympy.Rational(mine)==prv else 'DIFFER'}")
    sys.stdout.flush()
