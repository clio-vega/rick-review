from core import *
def fac_schur(mu):
    mu=list(mu)+[0]*(3-len(mu))
    return sp.expand(sp.cancel(sp.Matrix(3,3,lambda i,j: ff(U[i],mu[j]+2-j)).det()/V))
def d_mu(mu):
    mu=list(mu)+[0]*(3-len(mu))
    return mu[0] + (mu[1]+mu[2])//2
print(" mu            w(s*_mu)   d_mu = mu1+floor((mu2+mu3)/2)   equal?")
agree=0; tot=0
sup = {2:[(2,2,0),(2,1,1)], 3:[(3,3,0),(3,2,1),(2,2,2)],
       4:[(4,4,0),(4,3,1),(4,2,2),(3,3,2)], 5:[(5,5,0),(5,4,1),(5,3,2),(4,4,2),(4,3,3)]}
allmu=sorted({m for v in sup.values() for m in v} | {(1,1,0),(1,0,0),(2,0,0),(2,1,0),(3,1,1)})
for mu in allmu:
    w = wmax(to_E(fac_schur(mu))); d = d_mu(mu); tot+=1; agree += (w==d)
    print(f"  {str(mu):14s}  {w:>3}        {d:>3}                         {w==d}")
print(f"\n  agreement: {agree}/{tot}")
print("\n  b : max_mu d_mu over the Schur support of e_2^b   vs   w(Psi_b)=b")
for b,mus in sup.items():
    print(f"   b={b}:  max d_mu = {max(d_mu(m) for m in mus)}   w(Psi_b) = {b}   gap = {max(d_mu(m) for m in mus)-b}  (floor(b/2)={b//2})")
