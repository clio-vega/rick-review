"""Exact-rational-point audit of Day 209 internals.  Fast, and still exact:
every quantity is evaluated in Q at random rational (s,t,z,w), so a nonzero
residual is a genuine refutation, and zero at many independent points is strong.
"""
import sys, random
from fractions import Fraction as F
from functools import lru_cache

random.seed(20260930)

def rnd():
    while True:
        s = F(random.randint(2, 97), random.randint(2, 97))
        t = F(random.randint(2, 97), random.randint(2, 97))
        z = F(random.randint(2, 97), random.randint(2, 97))
        w = F(random.randint(2, 97), random.randint(2, 97))
        if len({s, t, z, w}) == 4 and t != 1 and s != 1 and z != w and s != t:
            return s, t, z, w

POINTS = [rnd() for _ in range(6)]


def make(s, t, z, w):
    def tp(a, n):
        r = F(1)
        for i in range(n):
            r *= 1 - a * t ** i
        return r

    @lru_cache(maxsize=None)
    def alpha(j):
        if j < 0:
            return F(0)                 # 207b s.0:  alpha_{-1} := 0
        num = F(1)
        for i in range(1, j + 1):
            num *= (s - t ** i)
        return num / tp(t, j)

    @lru_cache(maxsize=None)
    def c(n, j):
        if j < 0 or n < 0 or j > n:
            return F(0)
        return tp(s, n - j) / tp(t, n - j) * (alpha(j) - s * t ** (n - j) * alpha(j - 1))

    def N(n, j):
        return t ** (-n * j) * c(n, j)

    def K(i, j):
        r = F(1)
        for p in range(i):
            r *= (t ** p * z - s * w) / (t ** p * z - t ** j * w)
        for rr in range(j):
            r *= (s * z - t ** rr * w) / (t ** i * z - t ** rr * w)
        return r

    @lru_cache(maxsize=None)
    def V(n, i, j):
        if i < 0 or j < 0 or n < 0:
            return F(0)
        tot = F(0)
        for n1 in range(n + 1):
            n2 = n - n1
            if c(n1, i) == 0 or c(n2, j) == 0:
                continue
            tot += (s ** ((n1 - i) + (n2 - j)) * t ** (-(n1 - i) * j - (n2 - j) * i)
                    * N(n1, i) * N(n2, j) * z ** (-n1) * w ** (-n2))
        return K(i, j) * tot
    return alpha, c, N, K, V


print("=" * 78)
print("(1) c(n,j) = 0 for n < j   [s.0 asserts this makes n1>=i, n2>=j automatic]")
print("=" * 78)
bad = 0
for (s, t, z, w) in POINTS:
    _, c, _, _, _ = make(s, t, z, w)
    bad += sum(1 for n in range(0, 10) for j in range(n + 1, 12) if c(n, j) != 0)
print(f"  n<=9, n<j<=11, {len(POINTS)} points: {bad} nonzero -> {'OK' if bad==0 else 'FAIL'}")

print()
print("=" * 78)
print("(2) THE m=0 BASE CASE of the s.3 induction.")
print("    At m=0: Gamma_k = 0 and T_k = sum_{i,j} V^{(k)}_{ij}.")
print("    So (TC) at m=0 IS the identity  sum_{i,j} V^{(k)}_{ij} = 0  for k>=1,")
print("    which the writeup discharges in one clause ('(L2) with its empty left side').")
print("=" * 78)
for k in range(0, 10):
    vals = []
    for (s, t, z, w) in POINTS:
        _, _, _, _, V = make(s, t, z, w)
        vals.append(sum(V(k, i, j) for i in range(k + 1) for j in range(k - i + 1)))
    allzero = all(v == 0 for v in vals)
    tag = f"0 at all {len(POINTS)} points" if allzero else str(vals[0])
    print(f"  k={k}: sum_(i,j) V^({k})_ij = {tag}"
          f"   {'OK' if (allzero or k == 0) else '*** NONZERO ***'}")

print()
print("=" * 78)
print("(3) (★2), the closing identity, at exact rational points.")
print("    Range deliberately includes the vacuous i+j>n, where both sides must be 0.")
print("=" * 78)
tot = okc = vac = vacok = 0
for (s, t, z, w) in POINTS:
    _, _, _, _, V = make(s, t, z, w)
    for n in range(0, 9):
        for i in range(0, 6):
            for j in range(0, 6):
                g, d = t ** i * z, t ** j * w
                cc = s ** 2 * t ** (-i - j)
                if g == d:
                    continue
                kg = (g - s * z) * (g - s * w) / (g * (g - d))
                kd = (d - s * z) * (d - s * w) / (d * (d - g))
                gp, dp = t ** (i - 1) * z, t ** j * w
                g2, d2 = t ** i * z, t ** (j - 1) * w
                if gp == dp or g2 == d2:
                    continue
                kgp = (gp - s*z) * (gp - s*w) / (gp * (gp - dp))
                kdp = (d2 - s*z) * (d2 - s*w) / (d2 * (d2 - g2))
                S = F(0)
                for p in range(0, max(n, 1)):
                    S += cc ** p * (V(n-1-p, i, j) * (kg*g**(-p-1) + kd*d**(-p-1))
                                    - t**p * V(n-1-p, i-1, j) * kgp * (t**(i-1)*z)**(-p-1)
                                    - t**p * V(n-1-p, i, j-1) * kdp * (t**(j-1)*w)**(-p-1))
                good = (S == (1 - t ** n) * V(n, i, j))
                tot += 1; okc += good
                if i + j > n:
                    vac += 1; vacok += good
                if not good:
                    print(f"  *** FAIL n={n} i={i} j={j} at s={s},t={t},z={z},w={w}")
print(f"  {okc}/{tot} instances (n<=8, i,j<=5, {len(POINTS)} exact points);"
      f" {vacok}/{vac} of them in the vacuous range i+j>n")
