import sympy as sp
q,t,u = sp.symbols('q t u')       # u := t^r
def qs(j): return (1-u*t**j)/(1-t)      # [r+j]_t
def qc(n): return sp.together((1-t**n)/(1-t))

print("=== A cleaner form for P_2 = q[r]_t - t[r-2]_t ===")
P2 = q*qs(0) - t*qs(-2)
claim = ((q-t) + (u/t)*(1-q*t))/(1-t)
print("   (1-t) P_2 = (q-t) + t^{r-1}(1 - q t)   :",
      sp.simplify(sp.together(P2-claim))==0)

print("\n=== same treatment for P_3 = [r+2][r+1]q^2 - t[2][r-1][r+1]q + t^3[r-2][r-1] ===")
P3 = qs(2)*qs(1)*q**2 - t*qc(2)*qs(-1)*qs(1)*q + t**3*qs(-2)*qs(-1)
P3e = sp.simplify(sp.expand(sp.together(P3*(1-t)**2)))
P3e = sp.factor(sp.expand(P3e))
print("   (1-t)^2 P_3 =", P3e)
# try the two-factor Baxterized ansatz
for cand,name in [(((q-t)+(u/t)*(1-q*t))*((q-t**2)+(u/t**2)*(1-q*t**2)), "(q-t + t^{r-1}(1-qt))(q-t^2 + t^{r-2}(1-qt^2))")]:
    d = sp.simplify(sp.expand(sp.together(P3*(1-t)**2 - cand)))
    print("   (1-t)^2 P_3 - [%s] = %s" % (name, sp.factor(d)))

print("\n=== so define  B_j(r) := (q - t^j) + t^{r-j}(1 - q t^j).  Then: ===")
def B(j): return (q-t**j) + (u/t**j)*(1-q*t**j)
print("   (1-t)  P_2 = B_1                :", sp.simplify(sp.together(P2*(1-t)-B(1)))==0)
d3 = sp.simplify(sp.together(sp.expand(P3*(1-t)**2 - B(1)*B(2))))
print("   (1-t)^2 P_3 = B_1 B_2 - ?       : remainder =", sp.factor(sp.simplify(d3)))
print("   is remainder = -(1-t)^2 t^r [2]_t q  (Rick's 4.4 correction term)? :",
      sp.simplify(sp.together(d3 + (1-t)**2*u*qc(2)*q))==0)
