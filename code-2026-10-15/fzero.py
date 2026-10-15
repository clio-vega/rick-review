"""Is F_n(t^-n) = 0?   Theorem 1 at m=0 IS exactly this statement, because at m=0
   T_k = z^-k * F_k(t^-k)  while Gamma_k = 0 for k>=1.
   Exact rational arithmetic -- no floating point.  Clio 2026-10-15."""
from fractions import Fraction as Fr

def build(s, t):
    def qp(a, n):            # (a;t)_n
        r = Fr(1)
        for i in range(n): r *= (1 - a*t**i)
        return r
    A = {-1: Fr(0)}
    def al(j):
        if j in A: return A[j]
        num = Fr(1)
        for i in range(1, j+1): num *= (s - t**i)
        A[j] = num/qp(t, j); return A[j]
    def c(n, j):
        if not (0 <= j <= n): return Fr(0)
        return qp(s, n-j)/qp(t, n-j) * (al(j) - s*t**(n-j)*al(j-1))
    return c

pts = [(Fr(2),Fr(3)), (Fr(-3),Fr(5)), (Fr(5,7),Fr(3,5)), (Fr(1,3),Fr(-1,2)),
       (Fr(11,4),Fr(7,9)), (Fr(-2,5),Fr(13,3)), (Fr(9,2),Fr(-4,7)), (Fr(1,11),Fr(6,5))]

print("F_n(t^-n)  at 8 exact rational (s,t) points,  n = 0..16")
print("  n | " + " | ".join(f"(s,t)=({s},{t})" for s,t in pts[:3]) + " | all 8 zero?")
allz = True
for n in range(0, 17):
    c = None
    vals = []
    for (s,t) in pts:
        c = build(s,t)
        vals.append(sum(c(n,j)*t**(-n*j) for j in range(n+1)))
    z = all(v == 0 for v in vals)
    allz &= z
    print(f" {n:2d} | " + " | ".join(f"{v}".ljust(15) for v in vals[:3]) + f" | {'YES' if z else '*** NO ***'}")
print("\nVERDICT: F_n(t^-n) = 0 for all n=0..16 at all 8 points:", allz)

print("\nCONTROL -- F_n must NOT vanish at a nearby non-special point t^-(n+1):")
s,t = pts[0]; c = build(s,t)
for n in range(0,7):
    v = sum(c(n,j)*t**(-(n+1)*j) for j in range(n+1))
    print(f"  n={n}: F_n(t^-(n+1)) = {v}   {'(zero -- CONTROL FAILED)' if v==0 and n>0 else ''}")

print("\nCONTROL -- is F_n identically zero as a polynomial? print all coeffs c(n,j), n=3:")
print("  ", [str(c(3,j)) for j in range(4)])

print("\n--- k=1 calibration against Hikita Thm 3.12:  F_1(t^r) =?= (1-s)[r+1]_t ---")
for (s,t) in pts:
    c = build(s,t)
    ok = all(sum(c(1,j)*t**(r*j) for j in range(2)) == (1-s)*(1-t**(r+1))/(1-t) for r in range(0,8))
    print(f"  (s,t)=({s},{t}): r=0..7 -> {'match' if ok else '*** MISMATCH ***'}")
