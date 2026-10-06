import sympy as sp
from kostka_d_matrix import *

def laurent_coeffs(v):
    """Return (min_exponent, coeff list) treating v as Laurent poly in t."""
    v = sp.expand(v)
    if v == 0: return 0, [0]
    d = sp.collect(v, t, evaluate=False)
    exps = []
    for term in sp.Add.make_args(v):
        p = sp.degree(sp.together(term*1), t) if False else None
    # robust: use as_coeff_exponent on each additive term
    pairs=[]
    for term in sp.Add.make_args(v):
        c, e = term.as_coeff_exponent(t)
        pairs.append((sp.Integer(e), c))
    mn = min(e for e,_ in pairs)
    return mn, pairs

def d_variant(n, conj_first=True, conj_second=True):
    parts = list(partitions(n)); out={}
    cache={}
    for lam in parts:
        for mu in parts:
            s = sp.Integer(0)
            for nu in parts:
                a = kostka(conj(nu), lam) if conj_first else kostka(nu, lam)
                if not a: continue
                second = conj(mu) if conj_second else mu
                key=(nu,second)
                if key not in cache: cache[key]=kostka_foulkes_tilde(*key)
                s += a * cache[key]
            out[(lam,mu)] = sp.expand(sp.simplify(s * t**(-n_stat(conj(lam)))))
    return parts, out

print("=== RANK / NON-VACUITY of the 209-pair check (Rick's actual formula) ===")
for n in range(2,7):
    parts, D = d_variant(n)
    nz=nonconst=0; maxdeg=0
    for v in D.values():
        if v==0: continue
        nz+=1
        mn,pairs = laurent_coeffs(v)
        dg = max(e for e,_ in pairs)
        maxdeg=max(int(maxdeg),int(dg))
        if dg>0 or len(pairs)>1: nonconst+=1
    dom = sum(1 for lam in parts for mu in parts if dominates(mu,lam))
    distinct = len({sp.srepr(sp.expand(v)) for v in D.values()})
    print(f" n={n}: pairs={len(parts)**2:4d} nonzero={nz:4d} nonconstant={nonconst:4d} "
          f"dominance-pairs={dom:4d} maxdeg={maxdeg:2d} distinct-values={distinct}")

print("\n=== NEGATIVE CONTROLS at n=5: break a conjugate, checks MUST fail ===")
for label, cf, cs in [("drop ' on nu  -> K_{nu,lam}", False, True),
                      ("drop ' on mu  -> Ktilde_{nu,mu}", True, False),
                      ("drop both conjugates", False, False)]:
    parts, D = d_variant(5, cf, cs)
    neg=negexp=bad1=0; tot=0
    for lam in parts:
        for mu in parts:
            v=D[(lam,mu)]; tot+=1
            if v!=0:
                mn,pairs=laurent_coeffs(v)
                if mn<0: negexp+=1
                if any(c<0 for _,c in pairs): neg+=1
            if sp.simplify(sp.expand(v).subs(t,1) - count_01_matrices(lam, conj(mu))) != 0: bad1+=1
    fired = (neg or bad1 or negexp)
    print(f"  [{label}]: negcoeff={neg}/{tot} negexponent={negexp}/{tot} d(1)!=M={bad1}/{tot}"
          f"  => {'CONTROL FIRED' if fired else 'PASSES -- CHECK IS BLIND'}")
