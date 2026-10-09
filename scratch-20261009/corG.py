"""cor:G(d): sgn Lead_{lambda,(n)} = (-1)^{l-1} for all t>0  (", t != 1" was dropped at 6922660).
Test the DROPPED hypothesis: is t=1 actually fine?  Thm 4.1 (thm:G) is the instrument."""
import sympy as sp
from itertools import combinations
from sympy.utilities.iterables import partitions as sym_parts
t=sp.symbols('t')

def Lead_full(lam):                      # Theorem 4.1
    l=len(lam); n=sum(lam)
    K=0
    V=list(range(l))
    edges=[(i,j) for i in range(l) for j in range(i+1,l)]
    for r in range(l-1, len(edges)+1):
        for H in combinations(edges,r):
            # connected on [l]?
            par=list(range(l))
            def f(x):
                while par[x]!=x: par[x]=par[par[x]]; x=par[x]
                return x
            for (i,j) in H:
                a,b=f(i),f(j)
                if a!=b: par[a]=b
            if len({f(v) for v in V})!=1: continue
            K+= sp.prod([t**(lam[i]*lam[j])-1 for (i,j) in H])
    pref=(1-t**n)/sp.prod([(1-t**li) for li in lam])
    return sp.cancel(sp.together(pref*K))

print("lam           Lead(t) at t=1   sign ok?   (-1)^(l-1)   regular at t=1?")
allok=True
lams=[(1,1),(2,1),(1,1,1),(2,2),(3,1),(2,1,1),(1,1,1,1),(3,2),(2,2,1),(3,3),(2,2,2),(3,2,1),(4,3,2)]
for lam in lams:
    L=Lead_full(lam); l=len(lam); n=sum(lam)
    try:
        v1=sp.simplify(sp.limit(L,t,1))
    except Exception as e:
        v1="ERR"
    reg = (sp.simplify(sp.denom(sp.cancel(L)).subs(t,1))!=0) or True
    # evaluate exactly at t=1 after cancellation
    Lc=sp.cancel(L)
    try:
        at1=sp.simplify(Lc.subs(t,1))
    except Exception:
        at1=None
    want=(-1)**(l-1)
    pred=(-1)**(l-1)*sp.Integer(n)**(l-1)
    ok = sp.simplify(v1-pred)==0
    sgnok = sp.sign(v1)==want if v1 not in (sp.zoo,sp.nan) else False
    allok &= bool(ok and sgnok)
    print("%-13s %-16s %-10s %-12s %s" % (lam, v1, sgnok, want, "yes" if v1 not in (sp.zoo,sp.nan,sp.oo) else "NO"))
print("\n(c) prediction (-1)^{l-1} n^{l-1} matched and sign correct at t=1 in all cases:", allok)

print("\nSign over a grid of t>0 (including t=1), all lambda above:")
bad=[]
for lam in lams:
    L=sp.cancel(Lead_full(lam)); l=len(lam); want=(-1)**(l-1)
    for tv in [sp.Rational(1,100),sp.Rational(1,2),sp.Rational(9,10),1,sp.Rational(11,10),2,5,sp.Integer(50)]:
        val=sp.nsimplify(sp.limit(L,t,tv)) if tv==1 else sp.cancel(L.subs(t,tv))
        if val==0 or sp.sign(val)!=want: bad.append((lam,tv,val))
print("  violations:", bad if bad else "NONE")
print("\nControl - is the test able to FAIL?  check a deliberately wrong sign claim (want=+1 for l=3):")
lam=(2,2,2); L=sp.cancel(Lead_full(lam))
print("   Lead(2,2,2) at t=2 =", sp.cancel(L.subs(t,2)), " sign =", sp.sign(sp.cancel(L.subs(t,2))), " (-1)^{l-1} =", (-1)**2)
print("   so a '+1' claim for l=2 would be caught: Lead(2,1) at t=2 =", sp.cancel(sp.cancel(Lead_full((2,1))).subs(t,2)))
