from psi import *
print("=== Lemma A: Psi (from T0 definition) == alternant form ?  ===")
w = randw(8, 20261020)
cases = [((2,),(0,),(2,3,4)), ((1,2),(0,0),(2,3,4)), ((2,3),(1,0),(2,3,4,5)),
         ((2,3),(1,1),(2,3,4,5)), ((1,2,3),(0,1,2),(1,2,3,4,5)),
         ((3,5),(2,-1),(3,4,5,6)), ((2,3,4),(0,0,0),(2,3,4,5,6)),
         ((1,3),(-1,2),(1,2,3,4))]
bad = 0
for kappa, theta, M in cases:
    a = Psi(kappa, theta, M, w); b = Psi_alt(kappa, theta, M, w)
    ok = (a == b)
    bad += (not ok)
    print(f"  kappa={kappa} theta={theta} M={M}: {'OK' if ok else 'MISMATCH'}"
          f"{'' if ok else f'  {a} vs {b}'}")
print("Lemma A:", "CONFIRMED on all cases" if not bad else f"{bad} MISMATCHES")

print()
print("=== Cor A1: consecutive kappa, constant twist t -> single product ===")
bad = 0
for (s, r, t, M) in [(2,2,0,(2,3,4)), (2,2,1,(2,3,4,5)), (1,3,0,(1,2,3,4)),
                     (3,2,-1,(3,4,5,6)), (2,3,2,(2,3,4,5,6)), (1,2,3,(1,2,3,4))]:
    kappa = tuple(range(s, s+r)); theta = (t,)*r
    lhs = Psi(kappa, theta, M, w)
    rhs = sum(S0(H, M, w) * prodv(H, t, s, w) if False else
              S0(H, M, w) * __import__('functools').reduce(
                  lambda acc, h: acc * w[h]**t * rho(s, w[h], w), H, F(1))
              for H in combinations(sorted(M), r))
    ok = (lhs == rhs); bad += (not ok)
    print(f"  s={s} r={r} t={t} M={M}: {'OK' if ok else 'MISMATCH'}")
print("Cor A1:", "CONFIRMED" if not bad else f"{bad} MISMATCHES")
