"""Rick's Q30 (email uid847): does |c_rho| for LG equal the number of strict {even<odd}
fillings of kappa/rho with diagonal entries EVEN?  Test his exact phrasing in BOTH indexings.
Ground truth = BR Cor 5.6 in BR's codimension indexing, already validated against my own
Hilbert polynomials at m<=4 (testZ.py TEST 3).  Clio 2026-10-24."""
from itertools import product
from comb import D, strict_partitions, contains
from testZ import c_BR, dual, is_rim

def strict_fillings(theta, diag_small):
    """count labelings of theta by {0<1} with rows and columns STRICTLY increasing,
    diagonal boxes forced to 0 (if diag_small) or to 1 (otherwise)."""
    boxes = sorted(theta); n = len(boxes); c = 0
    for a in product((0, 1), repeat=n):
        ok = True
        for i, b in enumerate(boxes):
            if b[0] == b[1] and a[i] != (0 if diag_small else 1): ok = False; break
        if not ok: continue
        for i, x in enumerate(boxes):
            for j, y in enumerate(boxes):
                if x[0] == y[0] and x[1] < y[1] and not a[i] < a[j]: ok = False; break
                if x[1] == y[1] and x[0] < y[0] and not a[i] < a[j]: ok = False; break
            if not ok: break
        if ok: c += 1
    return c

variants = {
 "DIM indexing  theta=D(k)\\D(r), diagonal = EVEN (his literal phrasing)": ('dim', True),
 "DIM indexing  theta=D(k)\\D(r), diagonal = ODD": ('dim', False),
 "CODIM indexing theta=D(nu)\\D(lam), diagonal = EVEN": ('cod', True),
 "CODIM indexing theta=D(nu)\\D(lam), diagonal = ODD  (= BR Cor 5.6 verbatim)": ('cod', False),
}
res = {k: [0, 0] for k in variants}   # [agree, disagree]
for m in range(1, 8):
    ks = strict_partitions(m)
    for kap in ks:
        lam = dual(kap, m); Dk = D(kap, m)
        for rho in ks:
            if rho == kap or not contains(kap, rho): continue
            nu = dual(rho, m)
            th_dim = Dk - D(rho, m)
            th_cod = D(nu, m) - D(lam, m)
            if not th_dim or len(th_dim) > 11: continue
            truth = abs(c_BR(lam, nu, m))
            for name, (which, ds) in variants.items():
                th = th_dim if which == 'dim' else th_cod
                got = strict_fillings(th, ds) if is_rim(th) else 0
                res[name][0 if got == truth else 1] += 1
print("Q30, tested over all (kappa,rho) with |theta| <= 11, m <= 7:")
for name, (a, d) in res.items():
    print(f"  {'YES' if d==0 else 'NO '}  agree {a:5d}  disagree {d:5d}   {name}")
