"""Does the (1,1,2) weight generalise as w(E_k) = ceil(k/2) in n variables?
   Test n=4: is w(Psi(e_2^b)) <= b with w(E_1,E_2,E_3,E_4)=(1,1,2,2)?"""
import sympy as sp, itertools, time
n=5
U=sp.symbols('v1:%d'%(n+1))
Es=sp.symbols('F1:%d'%(n+1))
W=[ (k+1)//2 for k in range(1,n+1) ]   # ceil(k/2)
print("  weights w(E_k) = ceil(k/2):", dict(zip(range(1,n+1),W)))
V=sp.expand(sp.prod([U[i]-U[j] for i in range(n) for j in range(i+1,n)]))
e=[sp.expand(sp.Add(*[sp.Mul(*c) for c in itertools.combinations(U,k)])) for k in range(0,n+1)]
def ff(x,m):
    r=sp.Integer(1)
    for k in range(m): r*=(x-k)
    return r
def Tmap(f):
    p=sp.Poly(sp.expand(f),*U); out=sp.Integer(0)
    for mo,c in zip(p.monoms(),p.coeffs()):
        out+=c*sp.Mul(*[ff(U[i],mo[i]) for i in range(n)])
    return sp.expand(out)
def Psi(f): return sp.expand(sp.cancel(sp.together(Tmap(sp.expand(f*V))/V)))
def to_E(f):
    from sympy.polys.polyfuncs import symmetrize
    sym,rem,_=symmetrize(sp.expand(f),list(U),formal=True)
    assert sp.expand(rem)==0
    return sp.expand(sym.subs({sp.Symbol('s%d'%(i+1)):Es[i] for i in range(n)},simultaneous=True))
def wmax(P):
    p=sp.Poly(sp.expand(P),*Es)
    return max(sum(a*w for a,w in zip(mo,W)) for mo in p.monoms())
t0=time.time()
for b in range(0,4):
    P=to_E(Psi(e[2]**b))
    print(f"   b={b}:  w(Psi(e_2^b)) = {wmax(P)}   (bound b = {b})   {'OK' if wmax(P)<=b else '*** EXCEEDS'}   [{time.time()-t0:.0f}s]",flush=True)
