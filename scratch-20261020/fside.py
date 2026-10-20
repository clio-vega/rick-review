"""Does Day 248's Lemma A collapse the *lambda-side* (F) consecutive block too?

F_kappa(M) = prod_M w^{2r} * Psi_{kappa, theta} with theta_j = kappa_j - 2j.
On a consecutive block kappa_j = s+j-1 this gives theta_j = s-1-j: NOT constant,
so Lemma P (which needs constant twist) does not apply.  BUT j-1+theta_j = s-2 IS
constant, and that is what the alternant actually sees.

CLAIM (mine).  For kappa = (s,...,s+r-1) and ANY arithmetic twist of slope -1,
   theta_j = t0 - (j-1),
we have    Psi_{kappa,theta}(M) = C_{s,r} * Psi_{kappa,(e,...,e)}(M),
   e = t0 - (r-1),   C_{s,r} = prod_{m=0}^{r-2} w_{s+m}^{r-1-m},
independent of M.  The F-twist is the case t0 = s-2.
Rick's Theorem B identity Psi_{(s,s+1),(1,0)} = w_s Psi_{(s,s+1),(0,0)} is t0=1, r=2.
"""
from psi import *
from functools import reduce

def C_pred(s, r, w):
    v = F(1)
    for m in range(0, r-1): v *= w[s+m]**(r-1-m)
    return v

w = randw(9, 4242)
print("CLAIM: Psi_{consec kappa, slope -1 twist} = C_{s,r} * Psi_{same kappa, constant twist e}")
print(f"{'s':>2}{'r':>3}{'t0':>4}  {'M':<18}{'theta (slope -1)':<20}{'e':>3}  ratio==C_pred?")
bad = 0
for (s, r, t0, M) in [(2,2,1,(2,3,4)), (2,2,1,(2,3,4,5)),            # Rick's Thm B case
                      (3,2,1,(3,4,5)), (2,2,0,(2,3,4,5)),
                      (2,2,0,(2,3,4)),                                # F-twist s=2,r=2 (t0=s-2=0)
                      (3,2,1,(3,4,5,6)),                              # F-twist s=3,r=2
                      (1,2,-1,(1,2,3,4)),                             # F-twist s=1,r=2
                      (2,3,0,(2,3,4,5)), (2,3,0,(2,3,4,5,6)),         # F-twist s=2,r=3
                      (1,3,-1,(1,2,3,4,5)),                           # F-twist s=1,r=3
                      (3,3,1,(3,4,5,6,7)),                            # F-twist s=3,r=3
                      (2,3,2,(2,3,4,5,6)), (1,4,-2,(1,2,3,4,5,6))]:
    kappa = tuple(range(s, s+r))
    theta = tuple(t0-(j) for j in range(r))      # t0-(j-1), j 1-indexed
    e = t0-(r-1)
    lhs = Psi(kappa, theta, M, w)
    rhs = Psi(kappa, (e,)*r, M, w)
    Cp = C_pred(s, r, w)
    if rhs == 0:
        print(f"{s:>2}{r:>3}{t0:>4}  {str(M):<18}{str(theta):<20}{e:>3}  rhs==0 skip"); continue
    ratio = lhs/rhs
    ok = (ratio == Cp); bad += (not ok)
    ftag = " <- F-twist" if t0 == s-2 else ""
    print(f"{s:>2}{r:>3}{t0:>4}  {str(M):<18}{str(theta):<20}{e:>3}  {'OK' if ok else 'MISMATCH'}{ftag}")
    if not ok: print(f"      ratio={ratio}  C_pred={Cp}")
print()
print("RESULT:", "claim CONFIRMED on all cases" if not bad else f"{bad} MISMATCHES")
