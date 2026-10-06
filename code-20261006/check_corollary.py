import sympy as sp
from kostka_d_matrix import *

print("Rick Theorem H Corollary, independent check (pure Python, no Sage).")
print("d_{lam mu}(t) = t^{-n(lam')} sum_nu K_{nu' lam} Ktilde_{nu mu'}(t)\n")

def d_matrix(n):
    parts = list(partitions(n))
    Kt = {}
    for nu in parts:
        for kap in parts:
            Kt[(nu, kap)] = kostka_foulkes_tilde(nu, kap)
    out = {}
    for lam in parts:
        for mu in parts:
            s = sp.Integer(0)
            for nu in parts:
                c = kostka(conj(nu), lam)
                if c: s += c * Kt[(nu, conj(mu))]
            out[(lam, mu)] = sp.expand(sp.simplify(s * t**(-n_stat(conj(lam)))))
    return parts, out

tot_pos = neg = 0
tot_one = bad_one = 0
tot_zero = bad_zero = 0
nonpoly = 0
for n in range(1, 7):
    parts, D = d_matrix(n)
    for lam in parts:
        for mu in parts:
            d = sp.expand(D[(lam, mu)])
            # (a) in N[t]?
            if d == 0:
                pass
            else:
                try:
                    p = sp.Poly(d, t)
                except sp.PolynomialError:
                    nonpoly += 1; print(f"  n={n} NOT POLY lam={lam} mu={mu}: {d}"); continue
                if any(c < 0 for c in p.all_coeffs()):
                    neg += 1
                    print(f"  n={n} NEGATIVE COEFF lam={lam} mu={mu}: {d}")
                # negative exponent check
                if d.has(1/t) or (d.as_powers_dict() and any(
                        isinstance(e, sp.Integer) and e < 0
                        for b, e in d.as_powers_dict().items() if b == t)):
                    nonpoly += 1; print(f"  n={n} NEG EXPONENT lam={lam} mu={mu}: {d}")
            tot_pos += 1
            # (b) d(1) = M_{lam mu'}
            tot_one += 1
            lhs = sp.simplify(d.subs(t, 1))
            rhs = count_01_matrices(lam, conj(mu))
            if sp.simplify(lhs - rhs) != 0:
                bad_one += 1
                print(f"  n={n} d(1) MISMATCH lam={lam} mu={mu}: d(1)={lhs} M={rhs}")
            # (c) d(0) = 1 iff mu |>= lam
            tot_zero += 1
            d0 = sp.simplify(sp.limit(d, t, 0)) if d != 0 else sp.Integer(0)
            want = 1 if dominates(mu, lam) else None
            if want == 1 and sp.simplify(d0 - 1) != 0:
                bad_zero += 1
                print(f"  n={n} d(0)!=1 though mu|>=lam lam={lam} mu={mu}: d(0)={d0}")
    print(f"n={n}: {len(parts)**2} pairs checked")

print(f"\nSUMMARY over n=1..6")
print(f"  pairs total                      : {tot_pos}")
print(f"  negative coefficients (want 0)   : {neg}")
print(f"  non-polynomial / neg exponent    : {nonpoly}")
print(f"  d(1) != M_{{lam mu'}} (want 0)     : {bad_one}/{tot_one}")
print(f"  d(0) != 1 on dominance (want 0)  : {bad_zero}/{tot_zero}")
