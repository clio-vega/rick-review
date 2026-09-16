import sympy as sp
q, t, u = sp.symbols('q t u')   # u := t^r, making [r+j]_t rational in (u,t)
def qs(j):   # [r+j]_t = (1 - u t^j)/(1-t)
    return (1 - u*t**j)/(1-t)
def qc(n):   # [n]_t for integer n
    return sp.together((1-t**n)/(1-t))

print("=== (A) [2][r-1][r+1] = [r+2][r-1] + t[r+1][r-2] + t^{r-1}[2]  (u = t^r) ===")
L = qc(2)*qs(-1)*qs(1)
R = qs(2)*qs(-1) + t*qs(1)*qs(-2) + (u/t)*qc(2)
print("   identity holds for ALL r:", sp.simplify(sp.together(L-R)) == 0)

print("\n=== (B) P_3 = ([r+1]q - t[r-1])([r+2]q - t^2[r-2]) - t^r [2] q ===")
P3 = qs(1)*qs(2)*q**2 - t*qc(2)*qs(-1)*qs(1)*q + t**3*qs(-2)*qs(-1)
F  = (qs(1)*q - t*qs(-1))*(qs(2)*q - t**2*qs(-2)) - u*qc(2)*q
print("   identity holds for ALL r:", sp.simplify(sp.together(sp.expand(P3 - F))) == 0)

print("\n=== (F) Rick's c_0 top-coefficient decomposition G, D_1, D_0 ===")
G  = qs(1)*qs(2)*qs(3)/(qc(2)*qc(3))
D1 = qs(-1)*qs(1)*qs(3)/qc(3)
D0 = qs(-2)*qs(-1)*qs(3)/(qc(2)*qc(3))
c0q = qs(3)/(qc(2)*qc(3)) * (qs(1)*qs(2)*q**2 - t*qc(2)*qs(-1)*qs(1)*q + t**3*qs(-2)*qs(-1))
target = G*q**2 - t*D1*q + t**3*D0
print("   c_0*q^3/(q-1) = G q^2 - t D_1 q + t^3 D_0 :",
      sp.simplify(sp.together(sp.expand(c0q - target))) == 0)
print("   D_0 = binom(r-1,2)_t * [r+3]/[3] :",
      sp.simplify(sp.together(D0 - (qs(-2)*qs(-1)/qc(2))*(qs(3)/qc(3)))) == 0)
