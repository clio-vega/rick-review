"""Exact census of the universal slack for the fresh-pair cyclic cell (Prop. 1).

T(p_i,p_j) = (1/n) sum_r p_i[r] (p_j[r] - p_j[(r+1)%n]) is the null drift of the
cell mean of U - V before the slack is subtracted.  T is bilinear, so its max over
the cube [0,1]^n x [0,1]^n is attained at a vertex; enumerate {0,1}^n x {0,1}^n.
Also: max T under a common range bound R_i, R_j <= 2 eps (affine rescaling of a
vertex), to compare the tight slack 2 eps^2 with the paper's delta = 2 eps.
"""
import itertools
from fractions import Fraction as F

def T(pi, pj):
    n = len(pi)
    return sum(F(pi[r]) * (F(pj[r]) - F(pj[(r + 1) % n])) for r in range(n)) / n

print("n  max_T_over_cube  floor(n/2)/n  argmax(p_i ; p_j)")
for n in range(2, 8):
    best, arg = None, None
    for pi in itertools.product((0, 1), repeat=n):
        for pj in itertools.product((0, 1), repeat=n):
            t = T(pi, pj)
            if best is None or t > best:
                best, arg = t, (pi, pj)
    assert best == F(n // 2, n), (n, best)
    print(f"{n}  {str(best):>6}           {str(F(n//2,n)):>6}        {arg}")
print("=> universal tight slack = 1/2 (all even n); delta = 1 is twice the need.")

# Positive control: a slack below 1/2 is beaten by the n=2 vertex.
assert T((1, 0), (1, 0)) == F(1, 2)
# Natural (clipped DGP) instance: one easy, one impossible item in one bin.
lo, hi = F(2, 100), F(98, 100)
print("clipped-DGP n=2 cell T =", float(T((hi, lo), (hi, lo))), "= (1/2)(0.96)^2 =", 0.5 * 0.96**2)

# Common range bound 2*eps: the max of T is (1/2)(2eps)^2 = 2 eps^2.
for eps in (F(1, 2), F(1, 4), F(1, 20), F(1, 320)):
    a, b = F(1, 2) - eps, F(1, 2) + eps
    t = T((b, a), (b, a))
    assert t == 2 * eps * eps
    print(f"eps={str(eps):>6}: tight slack 2eps^2={float(t):.6f}   paper delta=2eps={float(2*eps):.6f}"
          f"   ratio={float(2*eps/t):.1f}")

# Sure bound: U - V <= 1, so with delta = 1 the increment X <= 0 surely.
print("max over outcomes of U-V =", max(wi*wj - wi*wt for wi in (0,1) for wj in (0,1) for wt in (0,1)))
