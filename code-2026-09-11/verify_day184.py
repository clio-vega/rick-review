"""Day 184 review — all verifications, one file. Clio, 2026-09-11.

(1) b_k solved from the defining algebraic equation F(1-F)^3(3-4F) = theta(3-2F)^2
(2) which of the two candidate b_k sequences satisfies it  (Rick's day184 script vs OEIS draft)
(3) log-convexity D_k = b_{k-1}b_{k+1} - b_k^2 on the VERIFIED b_k
(4) p_k via graded Witt; p_21; the mod-3 counterexamples
(5) C_m with and without carries -> the defect in UID 707's step (b)
"""
from fractions import Fraction as Fr

N = 60
def mul(f, g, n=N): return [sum(f[i]*g[k-i] for i in range(k+1)) for k in range(n)]
def inv(f, n=N):
    g = [Fr(1,1)/f[0]] + [Fr(0)]*(n-1)
    for k in range(1, n): g[k] = -sum(f[i]*g[k-i] for i in range(1, k+1))/f[0]
    return g

# (1) solve F = theta(3-2F)^2 / [(1-F)^3(3-4F)] by iteration
F = [Fr(0)]*N
for _ in range(N+5):
    t3m2F = [Fr(3)-2*F[0]] + [-2*x for x in F[1:]]
    omF   = [Fr(1)-F[0]]   + [-x   for x in F[1:]]
    t3m4F = [Fr(3)-4*F[0]] + [-4*x for x in F[1:]]
    th    = [Fr(0), Fr(1)] + [Fr(0)]*(N-2)
    F = mul(mul(th, mul(t3m2F, t3m2F)), inv(mul(mul(omF, mul(omF, omF)), t3m4F)))
assert all(F[i].denominator == 1 for i in range(1, N)), "b_k must be integers"
b = [1] + [int(x) for x in F[1:]]

# (2) residual test on both candidate sequences
def residual(bs, label):
    n = min(N, len(bs))
    G = [Fr(x) for x in bs[:n]]; G[0] = Fr(0)
    omF   = [Fr(1)-G[0]] + [-x   for x in G[1:n]]
    t3m4F = [Fr(3)-4*G[0]] + [-4*x for x in G[1:n]]
    t3m2F = [Fr(3)-2*G[0]] + [-2*x for x in G[1:n]]
    th    = [Fr(0), Fr(1)] + [Fr(0)]*(n-2)
    lhs = mul(mul(mul(G, omF, n), mul(omF, omF, n), n), t3m4F, n)
    rhs = mul(th, mul(t3m2F, t3m2F, n), n)
    d = [lhs[i]-rhs[i] for i in range(n)]
    first = next((i for i, x in enumerate(d) if x != 0), None)
    print(f"  {label:22s} first nonzero residual: "
          + (f"theta^{first} = {d[first]}" if first is not None else "NONE (exact)"))

draft  = [1,3,27,417,7851,164124,3661389,85384566,2056373739,50751637140,
          1276862920140,32626363346505,844375375808301]
day184 = [1,3,27,417,7851,164124,3663984,85498458,2058089283,50705502591,
          1272084879132,32365470683334]
print("(2) F(1-F)^3(3-4F) - theta(3-2F)^2 == 0 ?")
residual(draft,  "OEIS draft / mine"); residual(day184, "day184 script")
print("  my solve == OEIS draft:", b[:13] == draft)

# (3) log-convexity on verified b_k
print("\n(3) D_k = b_{k-1}b_{k+1} - b_k^2 on verified b_k:")
D = [b[k-1]*b[k+1] - b[k]**2 for k in range(1, N-1)]
print("  D_1..D_6 :", D[:6])
print(f"  all D_k > 0 for k=1..{N-2} (strictly LOG-CONVEX): {all(x > 0 for x in D)}")

# (4) p_k by graded Witt, via log B and Mobius-free l_n recursion
l = [0]*N
for n in range(1, N): l[n] = n*b[n] - sum(l[k]*b[n-k] for k in range(1, n))
p = [0]*N
for n in range(1, N):
    s = l[n] - sum(d*p[d] for d in range(1, n) if n % d == 0)
    assert s % n == 0; p[n] = s//n
print("\n(4) p_1..p_6:", p[1:7])
print("  p_21 =", p[21], "  p_21 mod 3 =", p[21] % 3)
M = N-1
print("  counterexamples (3|m, p_m mod 3 != 2):",
      [(m, p[m] % 3) for m in range(3, M+1, 3) if p[m] % 3 != 2])
print("  THEOREM p_m = 0 mod 3 for 3 nmid m, m<=%d: %s"
      % (M, all(p[m] % 3 == 0 for m in range(1, M+1) if m % 3)))

# (5) the UID 707 step-(b) defect: gamma_m := C_m mod 3 (no carry) vs carried gamma
def dig3(x, j):
    for _ in range(j): x //= 3
    return x % 3
C_raw = [0]*(3*N)
for m in range(1, N):
    j = 0
    while 3**j <= m:
        if m % (3**j) == 0: C_raw[m] += dig3(p[m//(3**j)], j)
        j += 1
C = C_raw[:]; gamma = [0]*(3*N)
for m in range(1, N):                      # carry upward, increasing m
    gamma[m] = C[m] % 3
    if 3*m < 3*N: C[3*m] += C[m]//3
bad = [m for m in range(1, M+1) if C_raw[m] % 3 != 0]
print("\n(5) UID 707 step (b): 'gamma_m := C_m mod 3 = 0 for ALL m'")
print("  m <= %d with C_m mod 3 != 0 :" % M, bad, "-> claim is", "TRUE" if not bad else "FALSE")
print("  all such m divisible by 9 :", all(m % 9 == 0 for m in bad))
print("  C_m values there          :", [C_raw[m] for m in bad])
print("  carried gamma_m all zero  :", all(gamma[m] == 0 for m in range(1, M+1)))
print("  for 3 nmid m, C_m == p_m mod 3 as integers:",
      all(C_raw[m] == p[m] % 3 for m in range(1, M+1) if m % 3))
