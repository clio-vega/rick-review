"""lem:I  [Y1^o + ... + Ym^o, x_1] = (s-1) x_1 Y_1^o   on Pol.
Plus negative controls. Checked on all monomials of degree <= D for each m."""
import itertools, engine as E
from sympy import simplify, expand, cancel, Integer
s,t = E.s, E.t

def monomials(X, d):
    m=len(X)
    for e in itertools.product(range(d+1), repeat=m):
        if sum(e)==d:
            term=Integer(1)
            for v,k in zip(X,e): term*= v**k
            yield e, term

def sumY(f, X, twisted=False):
    return cancel(sum(E.Yop(f,X,i,twisted=twisted) for i in range(1,len(X)+1)))

results={}
for m in [2,3,4]:
    X=E.xs(m)
    ok=bad=0; badlist=[]
    for d in range(0,4):
        for e,mon in monomials(X,d):
            # [sum Y^o, x_1] mon = sum Y^o (x_1 mon) - x_1 sum Y^o(mon)
            lhs = cancel(sumY(expand(X[0]*mon),X) - X[0]*sumY(mon,X))
            rhs = cancel((s-1)*X[0]*E.Yop(mon,X,1,twisted=False))
            if simplify(cancel(lhs-rhs))==0: ok+=1
            else: bad+=1; badlist.append((m,e))
    results[m]=(ok,bad,badlist)
    print(f"m={m}: lem:I  {ok} of {ok+bad} pass, {bad} fail")

# ---- negative controls: each must FIRE (i.e. produce failures) ----
print()
print("negative controls (each must fail; a control reading 0/N would mean the test is blind):")
X=E.xs(3)
mons=[mon for d in range(0,4) for e,mon in monomials(X,d)]

def control(name, rhsfun):
    ok=bad=0
    for mon in mons:
        lhs = cancel(sumY(expand(X[0]*mon),X) - X[0]*sumY(mon,X))
        try: r = rhsfun(mon)
        except Exception: bad+=1; continue
        if simplify(cancel(lhs-r))==0: ok+=1
        else: bad+=1
    print(f"  {name:48s} {bad} of {ok+bad} FAIL  (ok={ok})")

control("C1  (t-1) x1 Y1^o   [wrong parameter s->t]", lambda mon: cancel((t-1)*X[0]*E.Yop(mon,X,1,twisted=False)))
control("C2  (s-1) x1 Y2^o   [wrong index]",          lambda mon: cancel((s-1)*X[0]*E.Yop(mon,X,2,twisted=False)))
control("C3  (s-1) x1 Y1     [twisted pi, not pi_o]", lambda mon: cancel((s-1)*X[0]*E.Yop(mon,X,1,twisted=True)))
control("C4  (s+1) x1 Y1^o   [wrong sign]",           lambda mon: cancel((s+1)*X[0]*E.Yop(mon,X,1,twisted=False)))
