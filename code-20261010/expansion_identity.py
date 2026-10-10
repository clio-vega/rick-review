"""
The structural question the proof idea leaves implicit:
expanding E_a E_b E_c(1) by (2.1), HOW MANY terms does order (s-1)^2 produce,
and are they the three the proof idea names?

Claim under test (my reading):
  E_c^{(r)}(1)=0 for r>=1 forces r=0, so
  [u^2] e*_lambda = E_a^{(2)}(e_b e_c) + e_a E_b^{(2)}(e_c) + E_a^{(1)}E_b^{(1)}(e_c)
                     (p,q)=(2,0)          (0,2)                (1,1)
as an EXACT polynomial identity (not merely modulo kappa>=2).
"""
import sys; sys.path.insert(0,'/home/clio/projects/reviews/code-20261010')
import star
from star import *
from symfun import e_poly
from fractions import Fraction

star.set_t(Fraction(5,3))
for (a,b,c) in [(2,2,1),(2,1,2),(1,2,2),(3,2,1),(2,2,2),(3,1,2)]:
    n=a+b+c; N=n
    ec=e_poly(c,N); eb=e_poly(b,N)
    # LHS: genuine [u^2] of E_a E_b E_c(1), summing over ALL (p,q,r)
    lhs=p_zero(); terms=[]
    for r in range(4):
        Fr = E_k_p(p_one(N), c, r, N)
        if p_is_zero(Fr): continue
        for q in range(4):
            Fq = E_k_p(Fr, b, q, N)
            if p_is_zero(Fq): continue
            for p_ in range(4):
                if p_+q+r != 2: continue
                G = E_k_p(Fq, a, p_, N)
                if p_is_zero(G): continue
                terms.append((p_,q,r)); lhs=p_add(lhs,G)
    rhs = p_add(p_add(E_k_p(p_mul(eb,ec),a,2,N),
                      p_mul(e_poly(a,N), E_k_p(ec,b,2,N))),
                E_k_p(E_k_p(ec,b,1,N),a,1,N))
    print(f"  (a,b,c)=({a},{b},{c}): surviving (p,q,r) at order 2 = {sorted(terms)}  "
          f"-> exactly {len(terms)} terms;  LHS==RHS: {p_is_zero(p_sub(lhs,rhs))}")
