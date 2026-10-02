"""Negative controls, exact rational arithmetic at generic points (fast).
The dictionary check must REFUSE wrong dictionaries and wrong exponents."""
from fractions import Fraction as Fr
from itertools import combinations
N = 4
S, T = Fr(3,7), Fr(-5,2)          # Rick's own test point
XS = [Fr(2,3), Fr(5,11), Fr(-7,4), Fr(9,5)]

def apply(alpha, coeff, shift, F):
    out = Fr(0)
    for I in combinations(range(N), alpha):
        Ic = [j for j in range(N) if j not in I]
        out += coeff(I, Ic)*F([shift*XS[i] if i in I else XS[i] for i in range(N)])
    return out

def Ek(k, F):
    return apply(k, lambda I, Ic: prod([XS[i] for i in I])*prod(
        [(XS[i]-T*XS[j])/(XS[i]-XS[j]) for i in I for j in Ic]), S, F)

def Mk1(k, qD, tD, F):
    return apply(k, lambda I, Ic: prod([XS[i] for i in I])*prod(
        [(tD*XS[i]-XS[j])/(XS[i]-XS[j]) for i in I for j in Ic]), qD, F)

def prod(l):
    r = Fr(1)
    for a in l: r *= a
    return r

# three independent test polynomials
Fs = [lambda v: v[0]**2*v[1] + v[2]*v[3] + 1,
      lambda v: sum(v),
      lambda v: prod(v) + v[0]**3]

dicts = {"(q,t)_DFK=(s,1/t)   [Rick's]": (S, 1/T),
         "(q,t)_DFK=(s,t)     [wrong t]": (S, T),
         "(q,t)_DFK=(1/s,1/t) [wrong q]": (1/S, 1/T),
         "(q,t)_DFK=(t,1/s)   [swapped]": (T, 1/S),
         "(q,t)_DFK=(1/t,s)   [swapped2]": (1/T, S)}
for name, (qD, tD) in dicts.items():
    row = []
    for k in (1, 2, 3):
        ok = all(Ek(k, F) == T**(k*(N-k))*Mk1(k, qD, tD, F) for F in Fs)
        row.append("k=%d:%s" % (k, "MATCH" if ok else "refused"))
    print("%-33s %s" % (name, "  ".join(row)))

print()
for e in (-1, 0, 1, 2):
    k = 2
    ok = all(Ek(k, F) == T**(k*(N-k)+e)*Mk1(k, S, 1/T, F) for F in Fs)
    print("prefactor t^{k(N-k)%+d} : %s" % (e, "MATCH" if ok else "refused"))
