"""Lemma 7 (star) and F_n(t^-n), verified ONE VARIABLE SYMBOLIC at a time
(univariate GCD in sympy is reliable; multivariate heugcd blows up).
For each exact rational value of s we verify the identity symbolically in t,
and vice versa.  Clio 2026-10-15."""
import sympy as sp
from sympy import Rational as R

def make(sval, tval):
    """sval/tval: exact Rational, or a sympy Symbol to keep symbolic."""
    s, t = sval, tval
    def qpoch(a, q, n):
        r = sp.Integer(1)
        for i in range(n): r *= (1 - a*q**i)
        return r
    A = {}
    def alpha(j):
        if j < 0: return sp.Integer(0)
        if j in A: return A[j]
        num = sp.Integer(1)
        for i in range(1, j+1): num *= (s - t**i)
        A[j] = sp.cancel(num/qpoch(t,t,j)); return A[j]
    C = {}
    def c(n,j):
        if not (0 <= j <= n): return sp.Integer(0)
        if (n,j) in C: return C[(n,j)]
        C[(n,j)] = sp.cancel(qpoch(s,t,n-j)/qpoch(t,t,n-j)*(alpha(j)-s*t**(n-j)*alpha(j-1)))
        return C[(n,j)]
    return s, t, c

def star_diff(c, s, t, n, j, lesion=None):
    P = n+3
    A = sum((s*t**(-j))**p * c(n-1-p,j)   for p in range(P+1))
    B = sum((s*t**(1-j))**p * c(n-1-p,j-1) for p in range(P+1))
    pre = sp.Integer(1) if lesion=='drop_tn' else t**n
    rhs = (1-s*t**(-j))*A - pre*(1-s*t**(1-j))*B
    return sp.cancel(sp.expand((1-t**n)*c(n,j) - rhs))

print("="*74)
print("LEMMA 7 (star):  t SYMBOLIC, s at exact rational values")
print("="*74)
tsym = sp.Symbol('t')
for sval in [sp.Integer(2), sp.Integer(-3), R(5,7), R(1,3), R(-11,4)]:
    s,t,c = make(sval, tsym)
    bad=[]; tot=0
    for n in range(1,13):
        for j in range(0,n+2):
            tot+=1
            if sp.simplify(star_diff(c,s,t,n,j)) != 0: bad.append((n,j))
    print(f"  s={sval}:  {tot-len(bad)}/{tot} (n<=12, j<=n+1) verified; fails={bad}")

print("\n"+"="*74)
print("LEMMA 7 (star):  s SYMBOLIC, t at exact rational values")
print("="*74)
ssym = sp.Symbol('s')
for tval in [sp.Integer(2), R(3,5), R(-1,2)]:
    s,t,c = make(ssym, tval)
    bad=[]; tot=0
    for n in range(1,13):
        for j in range(0,n+2):
            tot+=1
            if sp.simplify(star_diff(c,s,t,n,j)) != 0: bad.append((n,j))
    print(f"  t={tval}:  {tot-len(bad)}/{tot} verified; fails={bad}")

print("\n"+"="*74)
print("POSITIVE CONTROL  (lesion: drop t^n on the second sum)")
print("="*74)
s,t,c = make(sp.Integer(2), tsym)
fire=0; tot=0
for n in range(1,8):
    for j in range(0,n+1):
        tot+=1
        if sp.simplify(star_diff(c,s,t,n,j,lesion='drop_tn')) != 0: fire+=1
print(f"  lesioned identity FAILS {fire}/{tot}  -> "
      + ("test is NON-VACUOUS" if fire else "*** CONTROL DID NOT FIRE ***"))

print("\n"+"="*74)
print("F_n(t^-n) =?= 0    <-- Theorem 1 at m=0 IS this statement")
print("="*74)
s,t,c = make(sp.Symbol('s'), sp.Symbol('t'))
for n in range(0,10):
    v = sp.simplify(sp.cancel(sum(c(n,j)*t**(-n*j) for j in range(0,n+1))))
    print(f"  n={n:2d}:  F_n(t^-n)      = {v}")
print()
print("  control -- F_n at a nearby NON-special point (must NOT vanish):")
for n in range(1,6):
    v = sp.factor(sp.cancel(sum(c(n,j)*t**(-(n+1)*j) for j in range(0,n+1))))
    print(f"  n={n:2d}:  F_n(t^-(n+1))  = {v}")
print()
print("  and the conjectured factorisation F_n(w) = (1-t^n w)*G_n(w):  is (1-t^n w) | F_n ?")
w = sp.Symbol('w')
for n in range(1,7):
    Fn = sp.expand(sum(c(n,j)*w**j for j in range(0,n+1)))
    q, rem = sp.div(sp.Poly(Fn, w), sp.Poly(1 - t**n*w, w))
    print(f"  n={n}:  remainder on dividing F_n(w) by (1-t^n w) = {sp.simplify(rem.as_expr())}")
