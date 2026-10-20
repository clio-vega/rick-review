"""Q524 replacement hunch, checked first-hand against Motegi 2610.15344
E^C: eq (typeCnormalizationfactor), source line 1057
E^B: eq (typeBnormalizationfactor), source line 1366
Rick: "psi is the j=k factor that E^C omits and E^B contains."
My lem:I2 (2026-10-18-c2-gauge-theorem-and-q-divisors.tex L409):
   Q2^2/Q1 = 1/prod_y (1-q y^2),  psi(y)^{-1} = (1-q)/(1-q y^2).
"""
import sympy as sp
n, N = 3, 3
q = sp.symbols('q')
u = sp.symbols(f'u1:{n+1}'); w = sp.symbols(f'w1:{N+1}')

def EC():
    num = sp.prod([(1-q*u[j]**-1*u[k]) for j in range(n) for k in range(n)]) \
        * sp.prod([(1-q*u[j]*w[k]) for j in range(n) for k in range(N)])
    den = sp.prod([(1-q*u[j]*u[k]) for j in range(n) for k in range(j+1,n)]) \
        * sp.prod([(1-q*w[j]*w[k]) for j in range(N) for k in range(j,N)])   # j <= k
    return num/den/(1-q)**(n-0)

def EB():
    num = sp.prod([(1-q*u[j]**-1*u[k]) for j in range(n) for k in range(n)]) \
        * sp.prod([(1-q*u[j]*w[k]) for j in range(n) for k in range(N)]) \
        * sp.prod([(1-q*u[j]) for j in range(n)])
    den = sp.prod([(1-q*u[j]*u[k]) for j in range(n) for k in range(j+1,n)]) \
        * sp.prod([(1-q*u[j]**2) for j in range(n)]) \
        * sp.prod([(1-q*w[j]*w[k]) for j in range(N) for k in range(j+1,N)]) \
        * sp.prod([(1-q*w[k]) for k in range(N)])
    return num/den/(1-q)**(n-0)

ratio = sp.cancel(sp.together(EB()/EC()))
pred  = sp.cancel(sp.prod([(1-q*u[j]) for j in range(n)]) * sp.prod([(1-q*w[k]**2) for k in range(N)])
                / (sp.prod([(1-q*u[j]**2) for j in range(n)]) * sp.prod([(1-q*w[k]) for k in range(N)])))
print("E^B / E^C  ==  [prod_j (1-q u_j)  prod_k (1-q w_k^2)] / [prod_j (1-q u_j^2) prod_k (1-q w_k)] ?")
print("  ", sp.simplify(ratio - pred) == 0)
print()
print("u-side:  E^C denominator has prod_{j<k}(1-q u_j u_k)      -> OMITS the j=k diagonal prod_j(1-q u_j^2)")
print("         E^B denominator has that AND prod_j(1-q u_j^2)   -> CONTAINS it")
print("   => Rick's statement is CORRECT on the u-blocks.")
print()
print("w-side:  E^C denominator has prod_{j<=k}(1-q w_j w_k)     -> CONTAINS the j=k diagonal prod_k(1-q w_k^2)")
print("         E^B denominator has prod_{j<k} and prod_k(1-q w_k) -> REPLACES it by the short-root (1-q w_k)")
print("   => read on the w-blocks the statement is INVERTED (and it is a replacement, not an omission).")
print()
psi_inv = [(1-q)/(1-q*u[j]**2) for j in range(n)]
lhs = sp.cancel(sp.prod([(1-q*u[j]**2) for j in range(n)]))
rhs = sp.cancel((1-q)**n / sp.prod(psi_inv))
print("The factor E^B contains and E^C omits  ==  (1-q)^n * prod_j psi(u_j) ?  ", sp.simplify(lhs-rhs)==0)
