from core import *
import pickle
Psi = {b: sp.sympify(v) for b,v in pickle.load(open('psi.pkl','rb')).items()}
BMAX = 7
N = BMAX+1
# A(T) = sum_k (1/k!) prod_{r=1..k}(E2 - r E1) T^k   -- manifestly polynomial (Rick's series form)
A = sp.Integer(0)
for k in range(N):
    pr = sp.Integer(1)
    for r in range(1,k+1): pr *= (E2s - r*E1s)
    A += sp.Rational(1,sp.factorial(k))*pr*Tv**k
# M(T) = sum_{n>=2} (-1)^{n-1} (n^2-1)/n E1^{n-2} T^n
M = sp.Integer(0)
for n in range(2,N+1):
    M += sp.Integer(-1)**(n-1)*sp.Rational(n*n-1,n)*E1s**(n-2)*Tv**n
# B = exp(E3 M) truncated
B = sp.Integer(0); term = sp.Integer(1)
for j in range(0,N//2+2):
    B += term
    term = sp.expand(term*E3s*M/(j+1))
    term = sp.Poly(term,Tv).as_expr() if term!=0 else term
    # truncate
    term = sum(c*Tv**m[0] for m,c in zip(sp.Poly(term,Tv).monoms(),sp.Poly(term,Tv).coeffs()) if m[0]<=BMAX) if term!=0 else 0
G = sp.expand(A*B)
Gp = sp.Poly(G,Tv)
coef = {m[0]:c for m,c in zip(Gp.monoms(),Gp.coeffs())}
print("b : [T^b/b!] A*B  ==  tops[b] ?")
ok=0
for b in range(N):
    lhs = sp.expand(coef.get(b,0)*sp.factorial(b))
    rhs = sp.expand(top(Psi[b]))
    same = sp.expand(lhs-rhs)==0
    ok += same
    print(f"  b={b}: {same}")
print("PASS" if ok==N else "FAIL", f"{ok}/{N}")

# also check M closed form equals series form (as series)
Mclosed = Tv/(E1s*(1+E1s*Tv)**2) - sp.log(1+E1s*Tv)/E1s**2
ser = sp.series(Mclosed, Tv, 0, N+1).removeO()
print("\nM closed-form vs series, orders 0..%d:"%N)
d = sp.expand(sp.expand(ser) - M)
dp = sp.Poly(sp.expand(d),Tv)
bad=[m[0] for m,c in zip(dp.monoms(),dp.coeffs()) if m[0]<=N and sp.simplify(c)!=0]
print("  mismatching orders:", bad if bad else "none")
