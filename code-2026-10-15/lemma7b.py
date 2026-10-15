"""Lemma 7 (star) + F_n(t^-n), computed in the fraction field QQ(s,t) to avoid
sympy's heuristic-GCD blowup.  Clio 2026-10-15."""
import sympy as sp
from sympy import QQ

ss, tt = sp.symbols('s t')
K = QQ.frac_field(ss, tt)
s, t = K(ss), K(tt)
one, zero = K.one, K.zero

def qpoch(a, q, n):
    r = one
    for i in range(n):
        r *= (one - a*q**i)
    return r

_alpha = {}
def alpha(j):
    if j < 0: return zero
    if j in _alpha: return _alpha[j]
    num = one
    for i in range(1, j+1):
        num *= (s - t**i)
    _alpha[j] = num / qpoch(t, t, j)
    return _alpha[j]

_c = {}
def c(n, j):
    if not (0 <= j <= n): return zero
    if (n,j) in _c: return _c[(n,j)]
    _c[(n,j)] = (qpoch(s,t,n-j)/qpoch(t,t,n-j)) * (alpha(j) - s*t**(n-j)*alpha(j-1))
    return _c[(n,j)]

ti = one/t   # t^{-1}
def tp(e):   # t^e for possibly negative e
    return t**e if e >= 0 else ti**(-e)

print("c(0,0) =", c(0,0), "  [Thm 1 base case Gamma_0 = T_0 needs this = 1]")

def lhs(n,j): return (one - t**n)*c(n,j)
def rhs(n,j,drop_tn=False):
    P = n + 3
    A = sum(((s*tp(-j))**p)*c(n-1-p,j)   for p in range(P+1))
    B = sum(((s*tp(1-j))**p)*c(n-1-p,j-1) for p in range(P+1))
    pre = one if drop_tn else t**n
    return (one - s*tp(-j))*A - pre*(one - s*tp(1-j))*B

print("\n=== Lemma 7 (star): n=1..14, j=0..n+1  (j=n+1 = out-of-range control) ===")
tot=0; fails=[]
for n in range(1,15):
    row=''
    for j in range(0,n+2):
        ok = (lhs(n,j) - rhs(n,j) == zero); tot+=1
        row += '.' if ok else 'X'
        if not ok: fails.append((n,j))
    print(f"  n={ n:2d}: {row}")
print(f"  {tot-len(fails)}/{tot} pairs verified; failures {fails}")

print("\n=== POSITIVE CONTROL (lesion: drop the t^n prefactor on the 2nd sum) ===")
fire=0; tot2=0
for n in range(1,7):
    for j in range(0,n+1):
        tot2+=1
        if lhs(n,j)-rhs(n,j,drop_tn=True) != zero: fire+=1
print(f"  lesioned identity FAILS {fire}/{tot2} -> test non-vacuous"
      if fire else "  CONTROL DID NOT FIRE -> test is vacuous")

print("\n=== SECOND CONTROL (lesion: alpha_{j-1} -> alpha_j in c(n,j)) ===")
def c_bad(n,j):
    if not (0<=j<=n): return zero
    return (qpoch(s,t,n-j)/qpoch(t,t,n-j))*(alpha(j) - s*t**(n-j)*alpha(j))
def lhs_b(n,j): return (one-t**n)*c_bad(n,j)
def rhs_b(n,j):
    P=n+3
    A=sum(((s*tp(-j))**p)*c_bad(n-1-p,j) for p in range(P+1))
    B=sum(((s*tp(1-j))**p)*c_bad(n-1-p,j-1) for p in range(P+1))
    return (one-s*tp(-j))*A - t**n*(one-s*tp(1-j))*B
fire=0; tot3=0
for n in range(1,7):
    for j in range(0,n+1):
        tot3+=1
        if lhs_b(n,j)-rhs_b(n,j)!=zero: fire+=1
print(f"  lesioned c FAILS {fire}/{tot3} -> the specific c(n,j) is load-bearing"
      if fire else "  CONTROL DID NOT FIRE")

print("\n=== F_n(t^{-n}) =?= 0   [what the m=0 branch of Thm 1's induction needs] ===")
for n in range(0,11):
    v = sum(c(n,j)*tp(-n*j) for j in range(0,n+1))
    print(f"  n={n:2d}:  F_n(t^-n) = {v}")

print("\n=== and F_n at a NON-special point, as a control that F_n is not identically 0 ===")
for n in range(0,6):
    v = sum(c(n,j)*tp(-(n+1)*j) for j in range(0,n+1))
    print(f"  n={n}:  F_n(t^-(n+1)) = {sp.factor(sp.sympify(str(v)))}")
