from core import *
import pickle, time
Psi = {b: sp.sympify(v) for b,v in pickle.load(open('psi.pkl','rb')).items()}
t0=time.time()
for b in [8,9]:
    Psi[b]=to_E(Psi_u(e2**b)); print(f"Psi_{b} done w={wmax(Psi[b])} ({time.time()-t0:.0f}s)",flush=True)
N=10
A = sum(sp.prod([E2s-r*E1s for r in range(1,k+1)])*Tv**k/sp.factorial(k) for k in range(N))
M = sum(sp.Integer(-1)**(n-1)*sp.Rational(n*n-1,n)*E1s**(n-2)*Tv**n for n in range(2,N+1))
B=sp.Integer(0); term=sp.Integer(1)
def trunc(x,n=N):
    x=sp.expand(x)
    if x==0: return x
    p=sp.Poly(x,Tv); return sum(c*Tv**m[0] for m,c in zip(p.monoms(),p.coeffs()) if m[0]<n)
for j in range(0,N//2+2):
    B+=term; term=trunc(sp.expand(term*E3s*M/(j+1)))
G=trunc(sp.expand(A*B)); Gp=sp.Poly(G,Tv)
co={m[0]:c for m,c in zip(Gp.monoms(),Gp.coeffs())}
for b in [8,9]:
    print(f"  b={b}: closed form == tops[b]?",
          sp.expand(co.get(b,0)*sp.factorial(b)-top(Psi[b]))==0, " w<=b?", wmax(Psi[b])<=b, flush=True)
# full recursion at b=7,8
for b in [7,8]:
    rhs=sp.expand((E2s-(b+1)*E1s+(b+1)**2)*Psi[b]-3*b*E3s*sigma_E(Psi[b-1])-b*(b-1)*(E1s-2*b-2)*E3s*sigma_E(Psi[b-2]))
    print(f"  full recursion b={b}->{b+1}:", sp.expand(rhs-Psi[b+1])==0, flush=True)
