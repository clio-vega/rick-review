"""
Symbolic derivation for the spine question, half two.

Claim A (model-free identity): if every row of R sums to zero and G = R^T R,
then the mean off-diagonal of G normalised by the MEAN diagonal is exactly
-1/(J-1).  No model, no sampling error.

Claim B (dead-instrument): if conditional on the item the error vector has
exchangeable covariance s^2[(1-rho)I + rho 11^T], then the per-item-demeaned
residual covariance is s^2(1-rho)C.  rho enters only as a SCALE, so the
residual CORRELATION matrix does not depend on rho at all.
"""
import numpy as np
import sympy as sp

print("="*72)
print("CLAIM A -- model-free identity, checked on random matrices")
print("="*72)
rng = np.random.default_rng(20261007)
for (I, J) in [(995, 32), (50, 9), (7, 4), (1000, 3)]:
    # arbitrary data, then row-centre (per item) AND column-centre (what
    # np.corrcoef does internally).  Row-centring is what makes R 1 = 0.
    X = rng.standard_normal((I, J)) * rng.uniform(0.3, 3.0, size=J)  # heteroscedastic
    X += rng.standard_normal((I, 1)) * 2.0                          # item effect
    R = X - X.mean(axis=1, keepdims=True)    # per-item demeaning
    R = R - R.mean(axis=0, keepdims=True)    # corrcoef's own centring
    G = R.T @ R
    off = G[~np.eye(J, dtype=bool)]
    arith = off.mean() / np.diag(G).mean()          # pooled normalisation
    P = np.corrcoef(R, rowvar=False)                # Pearson (geometric norm.)
    pear = P[~np.eye(J, dtype=bool)].mean()
    print(f"  I={I:5d} J={J:3d}  pooled-norm mean off-diag = {arith:+.15f}"
          f"   -1/(J-1) = {-1/(J-1):+.15f}   Pearson = {pear:+.9f}"
          f"   slack = {pear + 1/(J-1):+.2e}")
print("  -> pooled normalisation reproduces -1/(J-1) to machine precision,")
print("     for ANY data.  Pearson differs only by AM-GM slack in judge variances.")

print()
print("="*72)
print("CLAIM B -- symbolic: C Sigma C = s^2 (1-rho) C")
print("="*72)
for J in [3, 4, 5, 9]:
    s2, rho = sp.symbols('s2 rho', positive=True)
    one = sp.ones(J, 1)
    Id = sp.eye(J)
    C = Id - one*one.T/J
    Sigma = s2*((1-rho)*Id + rho*one*one.T)
    lhs = sp.simplify(C*Sigma*C)
    rhs = sp.simplify(s2*(1-rho)*C)
    print(f"  J={J}: C.Sigma.C - s^2(1-rho)C == 0 ?  {sp.simplify(lhs-rhs) == sp.zeros(J,J)}")

print()
print("  Residual correlation entries (symbolic, J=5):")
J = 5
s2, rho = sp.symbols('s2 rho', positive=True)
one = sp.ones(J,1); Id = sp.eye(J)
C = Id - one*one.T/J
Sigma = s2*((1-rho)*Id + rho*one*one.T)
V = sp.simplify(C*Sigma*C)
corr = sp.simplify(V[0,1]/sp.sqrt(V[0,0]*V[1,1]))
print(f"    rho_resid(1,2) = {corr}        (target -1/(J-1) = {sp.Rational(-1,J-1)})")
print(f"    free of rho?  {sp.simplify(sp.diff(corr, rho)) == 0}")
print(f"    free of s2?   {sp.simplify(sp.diff(corr, s2)) == 0}")
