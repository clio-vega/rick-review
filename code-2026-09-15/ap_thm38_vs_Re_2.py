"""Parts (B) and (C): AP Thm 38 statement vs Rick's (Re), as a RING identity in free e_i."""
import sympy as sp
q, z = sp.symbols('q z')
NMAX = 9
e = sp.symbols('e0:%d' % (NMAX+1))          # e_0..e_N as FREE commuting indeterminates
def bracket(i):                              # [i]_q = 1+q+...+q^{i-1}
    return sum(q**j for j in range(i))

# ---- AP Thm 38 statement, verbatim structure ----
#   H(z) = F(z) / (1 - q * sum_{i>=2} [i-1]_q e_i z^i),   F(z) = sum_{i>=0} e_i z^i
F  = sum(e[i]*z**i for i in range(NMAX+1)).subs(e[0], 1)
D  = q*sum(bracket(i-1)*e[i]*z**i for i in range(2, NMAX+1))
H  = sp.series(F/(1-D), z, 0, NMAX+1).removeO()
X_AP = [sp.expand(H.coeff(z, n)) for n in range(NMAX+1)]

# ---- Rick's (Re): X_n = e_n + q sum_{k=2}^n [k-1]_q e_k X_{n-k},  X_0 = 1 ----
X_Re = [sp.Integer(1)]
for n in range(1, NMAX+1):
    val = e[n] + q*sum(bracket(k-1)*e[k]*X_Re[n-k] for k in range(2, n+1))
    X_Re.append(sp.expand(val))

print("="*74)
print("(C) Is Rick's (Re) the coefficient extraction of AP Thm 38's STATEMENT?")
print("    (free e_i: this is a ring identity, no chromatic input)")
print("="*74)
allok = True
for n in range(NMAX+1):
    ok = sp.simplify(sp.expand(X_AP[n] - X_Re[n])) == 0
    allok &= ok
    print("   n=%d : AP-Thm38 coeff of z^n  ==  (Re)  ?  %s" % (n, "YES" if ok else "NO"))
print("   -> identical for all n<=%d : %s" % (NMAX, allok))

# ---- (B) both against the ground truth of part (A) ----
print()
print("="*74)
print("(B) AP Thm 38 / (Re) against ground truth from the colouring definition")
print("="*74)
truth = {   # from ap_thm38_vs_Re.py part (A), e-basis expansions
 1: {(1,): 1},
 2: {(2,): q+1},
 3: {(2,1): q, (3,): q**2+q+1},
 4: {(2,2): q*(q+1), (3,1): q*(q+1), (4,): (q+1)*(q**2+1)},
 5: {(2,2,1): q**2, (3,2): q*(2*q**2+3*q+2), (4,1): q*(q**2+q+1),
     (5,): q**4+q**3+q**2+q+1},
}
def to_edict(expr, n):
    """expr is a polynomial in the free e_i; collect as {partition: coeff}."""
    expr = sp.expand(expr)
    out = {}
    for term in sp.Add.make_args(expr):
        c, lam = sp.Integer(1), []
        for f in sp.Mul.make_args(term):
            b, ex = (f.base, f.exp) if f.is_Pow else (f, 1)
            if b in e:
                lam += [e.index(b)]*int(ex)
            else:
                c *= f
        lam = tuple(sorted(lam, reverse=True))
        out[lam] = sp.expand(out.get(lam, 0) + c)
    return {k: v for k, v in out.items() if sp.expand(v) != 0}

for n in range(1, 6):
    got = to_edict(X_Re[n], n)
    want = {k: sp.expand(v) for k, v in truth[n].items()}
    ok = (set(got) == set(want)) and all(sp.simplify(got[k]-want[k]) == 0 for k in want)
    print("   n=%d : (Re) reproduces the colouring-definition value ? %s" % (n, "YES" if ok else "NO"))

# ---- Rick's (GF) form vs the display inside AP's proof of Thm 38 ----
print()
print("="*74)
print("(D) Rick's (GF) form  F(z)[E(qz) - qE(z)] = (1-q)E(z)")
print("    vs AP proof display  H_m(z) = (q-1) F_m(z) / ( -F_m(qz) + q F_m(z) )")
print("    [Rick's F = AP's H (chromatic GF); Rick's E = AP's F (elementary GF)]")
print("="*74)
E     = sum(e[i]*z**i for i in range(NMAX+1)).subs(e[0], 1)      # Rick's E(z) = AP's F(z)
E_qz  = sum(e[i]*(q*z)**i for i in range(NMAX+1)).subs(e[0], 1)
# Rick's LHS - RHS, with F(z) = H(z) the AP Thm 38 generating function:
lhs = sp.series(sp.expand(H*(E_qz - q*E) - (1-q)*E), z, 0, NMAX).removeO()
print("   residual of Rick's (GF) when F := AP Thm 38's H :", sp.simplify(sp.expand(lhs)))
# AP's proof display rearranged:  H*(-F(qz) + qF(z)) = (q-1)F(z)
ap  = sp.series(sp.expand(H*(-E_qz + q*E) - (q-1)*E), z, 0, NMAX).removeO()
print("   residual of AP's proof display                :", sp.simplify(sp.expand(ap)))
print("   -> the two equations are the same equation multiplied by -1:",
      sp.simplify(sp.expand((E_qz - q*E) + (-E_qz + q*E))) == 0)
