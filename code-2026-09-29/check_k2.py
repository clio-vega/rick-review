import sympy as sp
from sympy import symbols, Integer as I
q,t=symbols('q t'); s=1/q
u=symbols('u', positive=True)   # u = t^r, symbolic in r

def poch(a,n): return sp.prod([1-a*t**i for i in range(n)]) if n>0 else I(1)
def alpha(j):
    if j<0: return I(0)
    return sp.cancel(sp.prod([s-t**i for i in range(1,j+1)])/poch(t,j))
def c(n,j):
    if j<0 or j>n or n<0: return I(0)
    return sp.cancel(poch(s,n-j)/poch(t,n-j)*(alpha(j)-s*t**(n-j)*alpha(j-1)))
def F(n,w): return sp.cancel(sum(c(n,j)*w**j for j in range(n+1)))

# ---- k=2 of UID 732, with t^r -> u ----
# coefficient of e_b e_{r+2-b}:  s^b F_{2-b}(t^{r-b})
co = {b: sp.simplify(sp.cancel(s**b*F(2-b, u*t**(-b)))) for b in range(3)}
print("UID 732 at k=2, written with u = t^r:")
for b in range(3): print(f"   coeff of e_{b} e_{{r+{2-b}}}  = {sp.factor(sp.simplify(co[b]))}")

# ---- W_r of UID 728, with [n] = (1-t^n)/(1-t), t^r -> u ----
br  = (1-u)/(1-t)          # [r]
br1 = (1-t*u)/(1-t)        # [r+1]
br2 = (1-t**2*u)/(1-t)     # [r+2]
br_2= (1-t**2)/(1-t)       # [2]
Wco = {0: sp.cancel((1-s)*(br2/br_2)*(br1 - s*(br-1))),   # e_0 e_{r+2}  = e_{r+2}
       1: sp.cancel(s*(1-s)*br),                          # e_1 e_{r+1}
       2: sp.cancel(s**2)}                                # e_2 e_r
print("\nUID 728 W_r, same normalisation:")
for b in range(3): print(f"   coeff of e_{b} e_{{r+{2-b}}}  = {sp.factor(sp.simplify(Wco[b]))}")

print("\nDifferences (must be 0):")
ok=True
for b in range(3):
    d=sp.simplify(sp.cancel(co[b]-Wco[b]))
    print(f"   b={b}: {d}")
    ok &= (d==0)
print("MATCH" if ok else "MISMATCH")

# ---- k=1 vs Hikita Thm 3.12:  e_1(Y).e_r = (1-s)[r+1] e_{r+1} + s e_1 e_r
print("\nk=1 vs Hikita Thm 3.12:")
h = {0: sp.cancel((1-s)*br1), 1: sp.cancel(s)}
for b in range(2):
    d=sp.simplify(sp.cancel(sp.simplify(s**b*F(1-b,u*t**(-b)))-h[b]))
    print(f"   b={b}: F-form={sp.factor(sp.simplify(s**b*F(1-b,u*t**(-b))))}   Hikita={sp.factor(h[b])}   diff={d}")

# ---- r=0 must recover Hikita Lemma 3.3: e_k(Y).1 = t^{C(k,2)} e_k, i.e. RHS reduces to e_k ----
print("\nr=0 (Hikita Lemma 3.3): coefficients s^b F_{k-b}(t^{-b}) for b<k must vanish, b=k must be 1:")
for k in range(1,8):
    vals=[sp.simplify(sp.cancel(s**b*F(k-b, t**(-b)))) for b in range(k+1)]
    print(f"   k={k}: {[sp.simplify(v) for v in vals]}")

# ---- t=0 collapse claimed in his email P.S.:  sum_{b<k}(1-s)s^b e_b e_{r+k-b} + s^k e_k e_r
print("\nt -> 0 collapse of the general coefficient s^b F_{k-b}(t^{r-b}):")
for k in range(1,6):
    for r in [0,1,2,k-1,k,k+1,k+2]:
        if r<0: continue
        row=[]
        for b in range(k+1):
            v=s**b*F(k-b, t**(r-b))
            row.append(sp.simplify(sp.limit(sp.cancel(v), t, 0)))
        pred=[sp.cancel((1-s)*s**b) for b in range(k)]+[s**k]
        agree = all(sp.simplify(row[b]-pred[b])==0 for b in range(k+1))
        print(f"   k={k} r={r}: t=0 coeffs={row}  matches-P.S.={agree}")
