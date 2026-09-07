"""Rick's two shipped scripts use DIFFERENT closed forms for the layer-1 series K.
  step13/PDF:  K = -p Y / q^2
  step16/step18: K = (p Y (2q+1) + s q)/q^2 + q'/q
Are they the same series?  (an-instrument-reports-on-its-referent)"""
import sympy as sp
T = sp.symbols("T"); N = 16
SV, PV = sp.Rational(2), sp.Rational(3)
Ys = [sp.S(0)]*(N+3)
for n in range(1, N+3):
    a = sp.S(1) if n == 1 else sp.S(0)
    a += SV*Ys[n-1] + sum(PV*Ys[k]*Ys[n-1-k] for k in range(n))
    Ys[n] = a
def tr(e): 
    e = sp.expand(e); return sp.expand(sum(e.coeff(T,k)*T**k for k in range(N+1)))
def inv(f):
    c=[f.coeff(T,k) for k in range(N+1)]; g=[sp.S(0)]*(N+1); g[0]=1/c[0]
    for n in range(1,N+1): g[n]=-sum(c[k]*g[n-k] for k in range(1,n+1))/c[0]
    return sum(g[k]*T**k for k in range(N+1))
def dd(f): return tr(sum((k+1)*f.coeff(T,k+1)*T**k for k in range(N+1)))
Y = tr(sum(Ys[n]*T**n for n in range(N+3)))
q = tr(1 - SV*T - 2*PV*T*Y)
K13 = tr(-PV*Y*inv(tr(q**2)))
K16 = tr(tr(PV*Y*(2*q+1) + SV*q)*inv(tr(q**2))) + tr(dd(q)*inv(q))
K16 = tr(K16)
print("K (step13 / PDF)  :", [K13.coeff(T,k) for k in range(7)])
print("K (step16/step18) :", [K16.coeff(T,k) for k in range(7)])
print("identical:", sp.expand(K13-K16) == 0)
