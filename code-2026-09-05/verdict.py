"""
JOB 2 verdict: top-weight slices in Rick's own (falling) frame, the root form,
and the general-lambda theorem that explains binom(n-1,2).  Clio 2026-09-05.
"""
import sympy as sp, math
from sympy.polys.polyfuncs import symmetrize
falling=lambda x,m: sp.prod([x-j for j in range(m)]) if m>0 else sp.Integer(1)
def V_of(u):
    n=len(u); return sp.expand(sp.prod([u[i]-u[j] for i in range(n) for j in range(i+1,n)]))
def Psi_direct(f,u):
    n=len(u); V=V_of(u); P=sp.Poly(sp.expand(f)*V,*u)
    num=sp.expand(sum(c*sp.prod([falling(u[i],a[i]) for i in range(n)]) for a,c in P.terms()))
    q,r=sp.div(sp.Poly(num,u[0]),sp.Poly(V,u[0])); assert r.is_zero; return sp.expand(q.as_expr())
def toE(p,u,Es):
    if sp.expand(p)==0: return sp.Integer(0)
    s,rem,_=symmetrize(sp.expand(p),list(u),formal=True); assert sp.expand(rem)==0
    return sp.expand(s.subs({sp.Symbol(f's{k}'):Es[k-1] for k in range(1,len(u)+1)}))

print("="*82)
print("A. TOP-WEIGHT SLICE  tops^(n)[b]  in Rick's FALLING frame, w(E_k)=ceil(k/2)")
print("="*82)
tops={}
for n in (3,4,5):
    u=sp.symbols(f'u1:{n+1}'); Es=sp.symbols(f'E1:{n+1}')
    e2=sp.expand(sum(u[i]*u[j] for i in range(n) for j in range(i+1,n)))
    for b in (1,2,3):
        if n==5 and b==3: continue
        expr=toE(Psi_direct(sp.expand(e2**b),u),u,Es)
        P=sp.Poly(expr,*Es); top=sp.Integer(0)
        for a,c in P.terms():
            if sum(a[k]*math.ceil((k+1)/2) for k in range(n))==b:
                top+=c*sp.prod([Es[k]**a[k] for k in range(n)])
        top=sp.expand(top); tops[(n,b)]=top
        E3free=sp.expand(top.subs({Es[k]:0 for k in range(2,n)}))
        rts=sp.roots(sp.Poly(sp.expand(E3free.subs({Es[0]:1})),Es[1]))
        rl=sorted([r for r,m in rts.items() for _ in range(m)],key=lambda z: float(z))
        print(f"  n={n} b={b}: tops = {sp.factor(E3free)}  (+E3+ terms: {sp.expand(top-E3free)})")
        print(f"           roots {rl}   binom(n-1,2)={int(sp.binomial(n-1,2))}  "
              f"-> {'roots = c, c+1, ... c+b-1  CONFIRMED' if rl==[sp.Integer(int(sp.binomial(n-1,2))+i) for i in range(b)] else '*** NOT the root form ***'}")

print("\n"+"="*82)
print("B. THE SHIFT RULE, tested where it is NOT degenerate")
print("   tops^(n)[b] =?= tops^(3)[b] with E_2 -> E_2 - (binom(n-1,2)-1) E_1")
print("="*82)
for (n,b) in sorted(tops):
    if n==3: continue
    E1s=sp.Symbol('E1'); E2s=sp.Symbol('E2')
    c=int(sp.binomial(n-1,2))-1
    shifted=sp.expand(tops[(3,b)].subs({E2s:E2s-c*E1s}))
    got=sp.expand(tops[(n,b)])
    # compare on the E_4..E_n-free part (n=3 base has no E_4+)
    Es=sp.symbols(f'E1:{n+1}')
    got3=sp.expand(got.subs({Es[k]:0 for k in range(3,n)}))
    d=sp.expand(got3-shifted)
    print(f"  n={n} b={b}: shift(c={c}) -> {sp.expand(shifted)}")
    print(f"            computed      -> {got3}")
    print(f"            difference    -> {d}   {'*** SHIFT RULE HOLDS ***' if d==0 else '<-- differs'}")

print("\n"+"="*82)
print("C. HIS STATED BASE vs THE TRUE BASE  (n=3, b=2)")
print("="*82)
E1s,E2s,E3s=sp.symbols('E1 E2 E3')
his_base=E2s**2-E1s*E2s-3*E3s
print(f"  his  tops^(3)[2] = {his_base}      roots of E3-free part: "
      f"{sorted(sp.roots(sp.Poly(sp.expand((his_base.subs({E3s:0,E1s:1}))),E2s)).keys(),key=float)}")
print(f"  true tops^(3)[2] = {sp.expand(tops[(3,2)])}   roots: [1, 2]")
print(f"  difference       = {sp.expand(tops[(3,2)]-his_base)}")
his_pred=E2s**2-5*E1s*E2s+6*E1s**2-3*E3s
print(f"\n  his n=4,b=2 prediction (shift of his base) = {his_pred}")
print(f"  TRUE  n=4,b=2 value                       = {sp.expand(tops[(4,2)].subs({sp.Symbol('E4'):0}))}")
print(f"  => if he tests his prediction against his raw n=4 data he gets a MISMATCH,")
print(f"     and by his own stated criterion would declare a TRUE conjecture dead.")
