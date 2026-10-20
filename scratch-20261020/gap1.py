"""Direct test on the sharp-file section 6 Gap 1 examples.
Rick: 'when the block ends at n-1 ... the coefficient is prod w^2 (F_{lambda^-} + beta F_{lambda^(r-1)})
       ... For blocks not ending at n-1, e.g. (1,2), (2,3), (1,2,3), there is no two-term fit.
       That is the obstruction.'
Test: in the CONSTANT-twist representative, is the u->infinity leading coefficient a SINGLE child?
Lemma T (u->inf): head j has degree theta_j-(r-j), tail has degree -r.
Constant twist e  =>  head degrees e-(r-j) strictly increasing in j => unique max at j=r.
F-twist          =>  head degrees kappa_j-j-r = const on a consecutive block => |B|-fold TIE.
"""
import sympy as sp
from itertools import permutations
from sympy import Rational as Q

def Psi_sym(kappa, theta, M, wv):
    r = len(kappa); tot = 0
    for h in permutations(M, r):
        x = [wv[hj] for hj in h]; tails = [t for t in M if t not in h]
        term = sp.Integer(1)
        for j in range(r):
            term *= (1 - 1/x[j]**2)
            for k in range(1, kappa[j]): term *= (1 - wv[k]/x[j])
        if term == 0: continue
        for j in range(r):
            for k in range(j+1, r): term *= (1-1/(x[j]*x[k]))/(1-x[j]/x[k])
        for t in tails:
            for j in range(r): term *= (1-1/(wv[t]*x[j]))/(1-wv[t]/x[j])
        for j in range(r): term *= x[j]**theta[j]
        tot += term
    return sp.cancel(sp.together(tot))

u = sp.symbols('u', positive=True)

def deg_and_lead(expr, u):
    e = sp.cancel(sp.together(expr))
    num, den = sp.fraction(e)
    pn, pd = sp.Poly(sp.expand(num), u), sp.Poly(sp.expand(den), u)
    return pn.degree()-pd.degree(), sp.cancel(pn.LC()/pd.LC())

print("block kappa   twist         deg_u  #heads at max degree (Lemma T)   leading coeff = single child?")
wvals = {1:Q(3,2), 2:Q(5,3), 3:Q(7,4), 4:Q(9,5), 5:Q(11,6), 6:Q(13,7)}
for (s, r, n, M) in [(3,2,5,(3,4,5)), (3,2,5,(3,4,5,6)),      # lambda=(3,4), block ends at n-1=4
                     (1,2,5,(1,2,3,5)), (1,2,4,(1,2,4)),      # lambda=(1,2): 'no two-term fit'
                     (2,2,5,(2,3,5)),                          # lambda=(2,3)
                     (1,3,5,(1,2,3,5))]:                       # lambda=(1,2,3)
    kappa = tuple(range(s, s+r))
    wv = dict(wvals); wv[n] = u
    thF = tuple(kappa[j]-2*(j+1) for j in range(r))   # F-twist
    e   = thF[0]-(r-1)                                 # constant-twist representative
    thC = (e,)*r
    # head degrees at u->inf
    degF = [thF[j]-(r-(j+1)) for j in range(r)]
    degC = [thC[j]-(r-(j+1)) for j in range(r)]
    tieF = sum(1 for d in degF if d == max(degF))
    tieC = sum(1 for d in degC if d == max(degC))
    PF = Psi_sym(kappa, thF, M, wv)
    PC = Psi_sym(kappa, thC, M, wv)
    dF, lF = deg_and_lead(PF, u); dC, lC = deg_and_lead(PC, u)
    # predicted single child for the constant-twist rep: head j=r, child Psi_{kappa minus top, (e,..,e)}
    Mm = tuple(m for m in M if m != n)
    child = Psi_sym(kappa[:-1], (e,)*(r-1), Mm, wv) if r > 1 else sp.Integer(1)
    ratio = sp.cancel(lC/child) if child != 0 else None
    print(f"  {str(kappa):<10} F:{str(thF):<12} deg={dF:<4} heads tied: F={tieF}  C={tieC}"
          f"   lead/child = {ratio}  (u-free: {ratio.free_symbols == set() if ratio is not None else '-'})")
