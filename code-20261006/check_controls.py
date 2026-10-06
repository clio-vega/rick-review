import sympy as sp
from kostka_d_matrix import *

print("=== CONTROL BLOCK: validate Kostka-Foulkes against known values ===")
ctrl = [
    (( 3,), (1,1,1), t**3,        "K_{(3),(111)} = t^3"),
    ((1,1,1),(1,1,1), sp.Integer(1), "K_{(111),(111)} = 1"),
    ((2,1),(1,1,1), t + t**2,     "K_{(21),(111)} = t+t^2"),
    ((2,1),(2,1), sp.Integer(1),  "K_{(21),(21)} = 1"),
    ((2,2),(1,1,1,1), t**2+t**3+t**4, "K_{(22),(1^4)} = t^2+t^3+t^4"),
]
ok = fail = 0
for lam, mu, expect, name in ctrl:
    got = sp.expand(kostka_foulkes(lam, mu))
    good = sp.simplify(got - expect) == 0
    print(f"  {'OK  ' if good else 'FAIL'} {name:34s} got {got}")
    ok += good; fail += (not good)
print(f"  controls: OK {ok} FAIL {fail}")

print("\n=== CONTROL: K_{lam mu}(1) == Kostka number, all n<=6 ===")
bad = 0; tot = 0
for n in range(1, 7):
    for lam in partitions(n):
        for mu in partitions(n):
            tot += 1
            if sp.expand(kostka_foulkes(lam, mu)).subs(t, 1) != kostka(lam, mu):
                bad += 1; print("   MISMATCH", lam, mu)
print(f"  {tot-bad}/{tot} agree at t=1")

print("\n=== NEGATIVE CONTROL: a deliberately wrong statistic must FAIL ===")
# charge+1 per tableau would break K_{lam lam}=1
wrongs = 0
for lam in partitions(4):
    w = sum(t**(charge(T)+1) for T in ssyt(lam, lam))
    if sp.simplify(w - 1) != 0: wrongs += 1
print(f"  perturbed statistic violates K_lam,lam=1 in {wrongs}/{len(list(partitions(4)))} cases (want >0)")

print("\n=== CONTROL: Ktilde(t) = t^{n(mu)} K(1/t) is a polynomial in N[t] ===")
bad = 0
for n in range(1, 7):
    for lam in partitions(n):
        for mu in partitions(n):
            Kt = kostka_foulkes_tilde(lam, mu)
            p = sp.Poly(Kt, t) if Kt != 0 else None
            if p is not None and any(c < 0 for c in p.all_coeffs()): bad += 1
print(f"  Ktilde negative-coefficient violations: {bad} (want 0)")
