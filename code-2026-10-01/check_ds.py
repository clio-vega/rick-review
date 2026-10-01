from ds_engine import *
import sys, itertools

def run(n, tval=t, verbose=True):
    m = n
    X = xs(m)
    allp = [p for p in partitions(n) if len(p) <= m]
    for lam in allp:
        P = eqt(lam, X, sval=s, tval=tval)
        c = e_expand(P, n, m, X)
        nz = {mu: v for mu, v in c.items() if sp.simplify(v) != 0}
        # (S) support contained in up-set
        bad = [mu for mu in nz if not dom_geq(mu, lam)]
        # exact up-set?
        upset = [mu for mu in allp if dom_geq(mu, lam)]
        missing = [mu for mu in upset if mu not in nz]
        # (L) leading
        lead = sp.simplify(nz.get(lam, 0) - s**n_stat(lam))
        # (V) vanish at s=1
        vanish = [mu for mu in nz if mu != lam and sp.simplify(sp.cancel(nz[mu].subs(s,1))) != 0]
        # valuation in s and lowest coeff at t=0
        valrep = []
        for mu in sorted(nz, key=n_stat):
            poly = sp.Poly(sp.simplify(sp.cancel(nz[mu])), s)
            mons = sorted(mm[0] for mm in poly.monoms())
            v = mons[0]
            low = sp.simplify(poly.coeff_monomial(s**v))
            low0 = sp.simplify(low.subs(t,0)) if tval is t else low
            valrep.append((mu, v, n_stat(mu), low, low0))
        valbad = [r for r in valrep if r[1] != r[2]]
        lowbad = [r for r in valrep if tval is t and sp.simplify(r[4]-1) != 0]
        print('lam=%-12s |supp|=%d upset=%d  S_viol=%s missing=%s  lead_ok=%s  s=1_viol=%s  val_ok=%s  d(0)@t=0_ok=%s'
              % (str(lam), len(nz), len(upset), bad or 'none', missing or 'none',
                 lead == 0, vanish or 'none', not valbad, not lowbad))
        if valbad: print('    VAL MISMATCH:', valbad)
        if lowbad: print('    LOW COEFF != 1:', [(r[0], r[3]) for r in lowbad])
    # order independence
    for lam in allp:
        if len(set(lam)) <= 1 or len(lam) < 2: continue
        base = eqt(lam, X, sval=s, tval=tval)
        for perm in set(itertools.permutations(lam)):
            d = sp.simplify(sp.expand(eqt(lam, X, sval=s, tval=tval, order=perm) - base))
            if d != 0: print('  ORDER DEP at', lam, perm); break
        else:
            print('  order-independent:', lam)

for n in (1,2,3,4):
    print('=== n =', n, '(symbolic in s,t) ===')
    run(n)
