"""Independent check of the Section 3(b) note's internals."""
import itertools, functools
import engine as E
from sympy import symbols, cancel, expand, Integer, factor, simplify, Matrix
t=E.t; w=symbols('w')
exec(open('t7_green.py').read().split("print(\"=== (a)")[0])   # reuse HL2, green, p_rho

print("=== 1. two-variable HL: P_rho = (x1 x2)^{rho_2} P_{(r)},  r = rho_1-rho_2 ===")
ok=bad=0
for r1 in range(0,6):
    for r2 in range(0,r1+1):
        lhs=HL2((r1,r2)); rhs=cancel(expand((X2[0]*X2[1])**r2*HL2((r1-r2,))))
        if cancel(expand(lhs-rhs))==0: ok+=1
        else: bad+=1; print("   FAIL",(r1,r2))
print(f"  {ok} of {ok+bad} pass, {bad} fail")

print()
print("=== 2. G_1(w) = P_rho(1,w;t) coefficients: 1 at k=rho_2,rho_1 ; 1-t strictly between ===")
def G1(rho):
    return cancel(expand(HL2(rho).subs({X2[0]:1,X2[1]:w},simultaneous=True)))
ok=bad=0; fails=[]
for r1 in range(0,7):
    for r2 in range(0,r1+1):
        rho=(r1,r2); g=G1(rho); r=r1-r2
        from sympy import Poly
        P=Poly(g,w)
        for k in range(0,r1+2):
            got=cancel(P.coeff_monomial(w**k))
            if r>=1:
                want = Integer(1) if k in (r2,r1) else (1-t if r2<k<r1 else Integer(0))
            else:
                want = Integer(1) if k==r2 else Integer(0)
            if cancel(got-want)==0: ok+=1
            else: bad+=1; fails.append((rho,k,got,want))
print(f"  {ok} of {ok+bad} coefficients match, {bad} fail")
for f in fails[:4]: print("     FAIL",f)

print()
print("=== 3. P_rho(1,t;t) = t^{rho_2}(1+t) for r>=1,  t^{rho_2} for r=0 ===")
ok=bad=0
for r1 in range(0,7):
    for r2 in range(0,r1+1):
        got=cancel(HL2((r1,r2)).subs({X2[0]:1,X2[1]:t},simultaneous=True))
        want=t**r2*(1+t) if r1-r2>=1 else t**r2
        if cancel(got-want)==0: ok+=1
        else: bad+=1; print("   FAIL",(r1,r2),factor(got),factor(want))
print(f"  {ok} of {ok+bad} pass, {bad} fail")

print()
print("=== 4. the worked example, piece by piece (lambda=(5,2), (x,y)=(4,3)) ===")
rho=(4,1)
from sympy import Poly
P=Poly(G1(rho),w)
print("  G_1 coefficients G_{1,k}, k=0..5:", [cancel(P.coeff_monomial(w**k)) for k in range(6)])
print("    Rick prints G_11=1, G_12=1-t, G_13=1-t, G_14=1, others 0")
print("  P_rho(1,t;t) =", factor(cancel(HL2(rho).subs({X2[0]:1,X2[1]:t},simultaneous=True))),
      "   Rick prints t(1+t)")
print("  b_lambda for lambda=(5,2) = (1-t)^2 :", factor((1-t)**2))
print("  X^(5,2)_(4,3) =", factor(cancel(green((5,2),(4,3)))), "  Rick prints t^2 - t")

print()
print("=== 5. his side finding: 'the raw formula also holds for y > x' ===")
def rick(lam,x,y):
    l1,l2=lam; m_xy=2 if x==y else 1
    if y<l2:  return (t-1)*t**(l2-1-y)*(1+t**y)
    if y==l2: return m_xy-(1-t)*t**(l2-1)
    return (t-1)*t**(l2-1)
ok=bad=0; n_ygtx=0
for n in range(2,11):
    for l2 in range(1,n//2+1):
        l1=n-l2
        if l1<l2: continue
        for y in range(1,n):
            x=n-y
            if x<1: continue
            if y<=x: continue
            n_ygtx+=1
            got=cancel(green((l1,l2),(x,y))); want=cancel(rick((l1,l2),x,y))
            if cancel(got-want)==0: ok+=1
            else: bad+=1
print(f"  y > x cases: {ok} of {n_ygtx} pass, {bad} fail  -> side finding {'CONFIRMED' if bad==0 else 'REFUTED'}")

print()
print("=== 6. ex:tworow's root-in-(-1,0) argument, on the diagonal class (x,y)=lambda ===")
ok=bad=0; tested=0
for l2 in range(3,10,2):          # lambda_2 >= 3 odd
    for l1 in range(l2+1,l2+6):   # lambda_1 > lambda_2
        n=l1+l2
        val=cancel(green((l1,l2),(l1,l2)))
        at_m1=cancel(val.subs(t,-1)); at_0=cancel(val.subs(t,0))
        tested+=1
        if at_m1==-1 and at_0==1: ok+=1
        else: bad+=1; print("   FAIL",(l1,l2),at_m1,at_0)
print(f"  '-1 at t=-1 and 1 at t=0' for lambda_1>lambda_2, lambda_2>=3 odd: {ok} of {tested} pass, {bad} fail")
# control: lambda_2 = 1 (he excludes it)
print("  control, lambda_2=1 (excluded by his hypothesis):")
for l1 in [2,3,4]:
    val=cancel(green((l1,1),(l1,1)))
    print(f"      lambda=({l1},1): X = {factor(val)}, at t=-1: {cancel(val.subs(t,-1))}, at t=0: {cancel(val.subs(t,0))}")
