"""Macdonald P_nu in m variables with (q,t)_Macdonald = (s, t^{-1}),
built from Macdonald VI (3.4) -- the book's operator D_n^1 -- by triangularisation.
This is deliberately NOT Rick's Y^o route."""
import itertools, functools
import engine as E
from sympy import symbols, simplify, expand, cancel, Poly, Integer, Matrix, zeros, eye
s,t = E.s, E.t

def D1(f, X):
    """Macdonald VI (3.4): D_n^1 = sum_i prod_{j!=i} (t_M x_i - x_j)/(x_i-x_j) * T_{q,x_i},
       here t_M = t^{-1}, q = s."""
    m=len(X); tot=0
    for i in range(m):
        pref=1
        for j in range(m):
            if j!=i: pref *= (X[i]/t - X[j])/(X[i]-X[j])
        tot += pref * f.subs({X[i]: s*X[i]}, simultaneous=True)
    return cancel(expand(cancel(tot)))

def ev_D1(nu, m):
    """eigenvalue sum_i q^{nu_i} t_M^{m-i} = sum_i s^{nu_i} t^{i-m}  (i=1..m)"""
    nu = tuple(nu)+(0,)*(m-len(nu))
    return sum(s**nu[i]*t**(i+1-m) for i in range(m))

@functools.lru_cache(maxsize=None)
def Pbasis(m, d):
    """returns (parts, {nu: {lam: coeff}}) : P_nu = sum_lam coeff * m_lam, monic at nu"""
    X = E.xs(m)
    parts = [p for p in E.partitions(d, maxlen=m)]
    # linear extension of dominance, biggest first
    parts.sort(key=lambda p: tuple(E.psum(p, m)), reverse=True)
    idx = {p:i for i,p in enumerate(parts)}
    # matrix of D1 in m_lam basis:  D1 m_lam = sum_mu Mat[mu][lam] m_mu
    Mat = {}
    for lam in parts:
        img = E.to_mono_dict(D1(E.mono_sym(lam, X), X), X, d)
        Mat[lam] = img
    out = {}
    for nu in parts:
        ev = ev_D1(nu, m)
        # solve (D1 - ev) v = 0, v[nu]=1, v supported on lam <|= nu
        supp = [p for p in parts if E.dominates(nu, p)]
        v = {p: None for p in supp}
        v[nu] = Integer(1)
        # back-substitute down the linear extension
        for lam in supp:
            if lam == nu: continue
            # coefficient of m_lam in (D1 - ev) (sum v_p m_p) = 0
            # = sum_p v_p * (Mat[p][lam] - ev*delta_{p,lam})
            num = 0
            for p in supp:
                if v[p] is None: continue
                c = Mat[p].get(lam, 0)
                if p == lam: c = c - ev
                num += v[p]*c
            den = Mat[lam].get(lam, 0) - ev
            v[lam] = cancel(-num/den) if den != 0 else None
        out[nu] = {k: (val if val is not None else Integer(0)) for k, val in v.items()}
    return tuple(parts), out

def P_poly(nu, m):
    X=E.xs(m); d=sum(nu)
    parts, basis = Pbasis(m,d)
    return E.from_mono_dict(basis[tuple(nu)], X)

def expand_in_P(f, m, d):
    """expand symmetric homogeneous f (degree d, in m vars) in the P_nu basis"""
    X=E.xs(m)
    parts, basis = Pbasis(m,d)
    target = E.to_mono_dict(f, X, d)
    coeffs = {}
    # triangular solve, biggest dominance first
    rem = dict(target)
    for nu in parts:
        c = rem.get(nu, 0)
        c = cancel(c)
        coeffs[nu] = c
        if c != 0:
            for lam, b in basis[nu].items():
                rem[lam] = cancel(rem.get(lam,0) - c*b)
    resid = {k: cancel(v) for k,v in rem.items()}
    bad = {k:v for k,v in resid.items() if v != 0}
    return coeffs, bad
