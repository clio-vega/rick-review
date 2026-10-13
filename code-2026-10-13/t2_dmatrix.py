"""
TEST 2: Corollary cor:dmatrix (longversion.tex l.537, commit 33526fc)

    d_{lam,mu}(t) = t^{n(mu')-n(lam')} [P_{mu'}(x;t^{-1})] e_lam
                  = t^{-n(lam')} sum_nu K_{nu',lam} Ktilde_{nu,mu'}(t),
    d in N[t],   d_{lam,mu}(1) = # 0-1 matrices with row sums lam, col sums mu'.

FOUR MECHANISMS, no shared code path:
  (a) iterate Theorem H(3) from b_empty  (Rick's explicit weight)
  (b) e -> P transition, with P_kappa(x;u) built by GRAM-SCHMIDT against the
      Hall-Littlewood scalar product <p_l,p_m>_u = delta z_l prod (1-u^{l_i})^{-1}
      (Macdonald III (4.9)).  No Pieri rule, no Kostka-Foulkes.
  (c) t^{-n(lam')} sum_nu K_{nu' lam} Ktilde_{nu mu'}(t), Kostka numbers by
      SSYT count and Kostka-Foulkes by the Lascoux-Schutzenberger CHARGE.
  (d) at t=1 only: brute-force count of 0-1 matrices.

FREE CONTROLS, all of which must FIRE (i.e. detect a deliberate error):
  C1  <P_l,P_l>_u = 1/b_l(u),  b_l = prod_v phi_{m_v(l)}(u)   [Macdonald III (4.9)]
  C2  K_{nu kappa}(1) = K_{nu kappa}                           [charge impl]
  C3  d computed with lam-order permuted (L_k must commute)
  C4  a deliberately corrupted H(3) weight must break agreement
  C5  t -> 1/t substituted BEFORE vs AFTER expansion in (b)
"""
import sys
from itertools import combinations, permutations, product as iproduct
from sympy.polys.fields import field
from sympy.polys.domains import QQ

FF, t = field("t", QQ)
ONE, ZERO = FF.one, FF.zero

# ---------------- partitions ----------------
def partitions(n, maxpart=None):
    if maxpart is None: maxpart = n
    if n == 0: yield (); return
    for k in range(min(n, maxpart), 0, -1):
        for rest in partitions(n-k, k):
            yield (k,) + rest

def conj(lam):
    if not lam: return ()
    return tuple(sum(1 for p in lam if p > j) for j in range(lam[0]))

def nstat(lam): return sum(i*p for i, p in enumerate(lam))
def mult(lam):
    m = {}
    for p in lam:
        if p: m[p] = m.get(p,0)+1
    return m
def dominates(a, b):          # a >= b in dominance (same size)
    sa = sb = 0
    for i in range(max(len(a), len(b))):
        sa += a[i] if i < len(a) else 0
        sb += b[i] if i < len(b) else 0
        if sa < sb: return False
    return True

def qint(n):  return sum(t**i for i in range(n))          # [n]_t
def qfact(n):
    r = ONE
    for i in range(1, n+1): r *= qint(i)
    return r
def qbin(m, r):
    if r < 0 or r > m: return ZERO
    return qfact(m) / (qfact(r)*qfact(m-r))

# ---------------- (a) Theorem H(3) ----------------
def vstrips_up(rho, k):
    """all kappa with kappa/rho a vertical k-strip, plus the data (r_v) and inv,
    using Rick's parametrisation read in the UP direction: raise k parts of rho
    by one (and/or append 1's), no two in the same row... i.e. kappa_i-rho_i<=1."""
    out = []
    L = len(rho) + k
    r = list(rho) + [0]*(L-len(rho))
    for S in combinations(range(L), k):
        kap = list(r)
        for i in S: kap[i] += 1
        if any(kap[i] < kap[i+1] for i in range(L-1)): continue
        kap_t = tuple(p for p in kap if p > 0)
        mk = mult(kap_t)
        rv = {}
        for i in S:
            v = kap[i]
            rv[v] = rv.get(v,0)+1
        inv = sum(rv.get(v,0)*(mk.get(w,0)-rv.get(w,0)) for v in mk for w in mk if v < w)
        w = t**inv
        for v in mk: w *= qbin(mk[v], rv.get(v,0))
        out.append((kap_t, w))
    # merge duplicates (different S giving same kappa: impossible for vertical
    # strips given (r_v) determines kappa, but equal-length rows make S non-unique)
    merged = {}
    for kap, w in out:
        merged[kap] = merged.get(kap, ZERO) + w
    return merged

def L_op(vec, k, corrupt=False):
    """vec: dict mu -> coeff (coefficients of bbar_mu).  Returns L_k vec."""
    out = {}
    for mu, c in vec.items():
        rho = conj(mu)
        for kap, w in vstrips_up(rho, k).items():
            if corrupt: w = w + t   # C4: deliberate corruption
            nu = conj(kap)
            out[nu] = out.get(nu, ZERO) + c*w
    return {k_: v for k_, v in out.items() if v}

def d_by_H3(lam, corrupt=False):
    vec = {(): ONE}
    for k in lam:
        vec = L_op(vec, k, corrupt)
    return vec

# ---------------- symmetric functions in N variables ----------------
def e_poly(r, N):
    out = {}
    for S in combinations(range(N), r):
        b = [0]*N
        for i in S: b[i] = 1
        out[tuple(b)] = ONE
    return out
def mul(A, B):
    out = {}
    for e1,c1 in A.items():
        for e2,c2 in B.items():
            b = tuple(x+y for x,y in zip(e1,e2))
            v = out.get(b, ZERO)+c1*c2
            if v: out[b]=v
            elif b in out: del out[b]
    return out
def add(A,B,c=ONE):
    C=dict(A)
    for e,v in B.items():
        w=C.get(e,ZERO)+c*v
        if w: C[e]=w
        elif e in C: del C[e]
    return C
def scal(c,A): return {} if not c else {e:c*v for e,v in A.items()}
def e_lambda(lam,N):
    out={tuple([0]*N):ONE}
    for p in lam: out=mul(out,e_poly(p,N))
    return out
def m_lambda(lam,N):
    """monomial symmetric polynomial"""
    pad = tuple(list(lam)+[0]*(N-len(lam)))
    return {e:ONE for e in set(permutations(pad))}
def p_poly(r,N):
    out={}
    for i in range(N):
        b=[0]*N; b[i]=r; out[tuple(b)]=ONE
    return out
def p_lambda(lam,N):
    out={tuple([0]*N):ONE}
    for r in lam: out=mul(out,p_poly(r,N))
    return out

def expand_in_basis(A, basis_polys, keys):
    """solve A = sum c_k basis[k] by triangular elimination on leading monomials."""
    lead = []
    for k_, B in zip(keys, basis_polys):
        lm = max(B.keys())
        lead.append(lm)
    order = sorted(range(len(keys)), key=lambda i: lead[i], reverse=True)
    R = dict(A); co = {}
    for i in order:
        lm = lead[i]
        c = R.get(lm, ZERO)/basis_polys[i][lm]
        if c:
            co[keys[i]] = c
            R = add(R, basis_polys[i], -c)
    assert not R, "residual nonzero (%d monomials)" % len(R)
    return co

# ---------------- (b) Gram-Schmidt Hall-Littlewood ----------------
def zlam(lam):
    m = mult(lam); z = 1
    import math
    for v,c in m.items(): z *= (v**c)*math.factorial(c)
    return QQ(z)

_E2P = {}
def e_to_p(r):
    """e_r = sum_{l |- r} eps_l / z_l * p_l,   eps_l = (-1)^{|l|-len(l)}."""
    if r in _E2P: return _E2P[r]
    out = {}
    for l in partitions(r):
        eps = (-1)**(r-len(l))
        out[l] = QQ(eps)/zlam(l)
    if r == 0: out = {(): QQ(1)}
    _E2P[r] = out
    return out

def elam_to_p(lam):
    """e_lam in the p-basis, as dict partition -> QQ."""
    cur = {(): QQ(1)}
    for r in lam:
        nxt = {}
        for l1, c1 in cur.items():
            for l2, c2 in e_to_p(r).items():
                key = tuple(sorted(l1+l2, reverse=True))
                nxt[key] = nxt.get(key, QQ(0)) + c1*c2
        cur = nxt
    return cur

def hl_ip_factory(N, u):
    """<f,g>_u for symmetric POLYNOMIALS in N vars of degree n:
       expand in the e-basis (triangular, unambiguous), then e -> p (Newton),
       then <p_l,p_m>_u = delta_{lm} z_l prod_i (1-u^{l_i})^{-1}  [Macdonald III (4.4)]."""
    cache = {}
    def to_p(A, n):
        key = tuple(sorted(A.items()))
        if key in cache: return cache[key]
        lams = [l for l in partitions(n) if l[0] <= N]
        basis = [e_lambda(l, N) for l in lams]
        co = expand_in_basis(A, basis, lams)
        acc = {}
        for l, c in co.items():
            for pl, q in elam_to_p(l).items():
                acc[pl] = acc.get(pl, ZERO) + c*q
        cache[key] = acc
        return acc
    def ip(A, B, n):
        ca, cb = to_p(A, n), to_p(B, n)
        s = ZERO
        for l, x in ca.items():
            y = cb.get(l, ZERO)
            if y:
                f = FF.one
                for part in l: f *= (FF.one - u**part)
                s += x*y*zlam(l)/f
        return s
    return ip

def HL_P(n, N, u):
    """P_kappa(x_1..x_N; u) for all kappa |- n, by Gram-Schmidt in dominance order."""
    ip = hl_ip_factory(N, u)
    lams = [l for l in partitions(n) if l[0] <= N]
    # linear extension of dominance, ascending
    order = sorted(lams, key=lambda l: (nstat(l),), reverse=True)
    order = sorted(order, key=lambda l: sum(1 for o in lams if dominates(l, o)))
    P = {}; norms = {}
    for lam in order:
        cur = m_lambda(lam, N)
        for mu in order:
            if mu == lam: break
            c = ip(cur, P[mu], n)
            if c: cur = add(cur, P[mu], -c/norms[mu])
        P[lam] = cur
        norms[lam] = ip(cur, cur, n)
    return P, norms

# ---------------- (c) Kostka and charge ----------------
def ssyt(shape, content):
    """all semistandard Young tableaux of given shape and content, as row lists."""
    shape = list(shape); nrow = len(shape)
    cells = [(i,j) for i in range(nrow) for j in range(shape[i])]
    T = [[0]*shape[i] for i in range(nrow)]
    letters = []
    for i,c in enumerate(content): letters += [i+1]*c
    res = []
    def rec(idx, avail):
        if idx == len(cells):
            res.append([row[:] for row in T]); return
        i,j = cells[idx]
        for v in sorted(set(avail)):
            if j > 0 and T[i][j-1] > v: continue
            if i > 0 and T[i-1][j] >= v: continue
            T[i][j] = v
            a = list(avail); a.remove(v)
            rec(idx+1, a)
            T[i][j] = 0
    rec(0, letters)
    return res

def reading_word(T):
    w = []
    for row in reversed(T): w += row
    return w

def charge(word):
    """Lascoux-Schutzenberger charge of a word of partition content.
    Standard algorithm: repeatedly extract a standard subword and sum charges."""
    w = list(word)
    total = 0
    while w:
        mx = max(w)
        # extract one standard subword: read right-to-left cyclically picking 1,2,...,mx
        # standard procedure (Macdonald III (6) / LS): choose rightmost 1, then the
        # first 2 to its LEFT cyclically, etc.
        idxs = []
        pos = len(w)          # start scanning leftwards from the end
        n_distinct = mx
        # pick 1
        cand = [i for i in range(len(w)) if w[i] == 1]
        if not cand: break
        i1 = cand[-1]
        idxs.append(i1)
        cur = i1
        for val in range(2, mx+1):
            # first occurrence of val strictly to the left of cur, cyclically
            found = None
            for i in range(cur-1, -1, -1):
                if w[i] == val: found = i; break
            if found is None:
                for i in range(len(w)-1, cur, -1):
                    if w[i] == val: found = i; break
            if found is None: break
            idxs.append(found); cur = found
        sub_vals = [w[i] for i in idxs]
        if sorted(sub_vals) != list(range(1, len(sub_vals)+1)):
            raise RuntimeError("subword extraction failed: %r" % (sub_vals,))
        # charge index of the standard subword: index(1)=0; index(r+1)=index(r)+1
        # if r+1 is to the RIGHT of r, else index(r).
        ind = {1: 0}
        posmap = {w[i]: i for i in idxs}
        for r in range(1, len(idxs)):
            ind[r+1] = ind[r] + (1 if posmap[r+1] > posmap[r] else 0)
        total += sum(ind.values())
        for i in sorted(idxs, reverse=True): w.pop(i)
    return total

_KF = {}
def kostka_foulkes_dict(nu, kappa):
    """K_{nu,kappa}(t) as dict {exponent: integer coefficient}, via charge."""
    key = (nu, kappa)
    if key in _KF: return _KF[key]
    d = {}
    for T in ssyt(nu, kappa):
        c = charge(reading_word(T))
        d[c] = d.get(c, 0) + 1
    _KF[key] = d
    return d

def kostka(nu, kappa): return len(ssyt(nu, kappa))

def dict_to_FF(d):
    s = ZERO
    for e, c in d.items(): s += QQ(c)*t**e
    return s

def d_by_KK(lam, mu):
    """t^{-n(lam')} sum_nu K_{nu',lam} Ktilde_{nu,mu'}(t),
       Ktilde_{nu,kappa}(t) = t^{n(kappa)} K_{nu,kappa}(1/t)."""
    n = sum(lam)
    lp, mp = conj(lam), conj(mu)
    nmp = nstat(mp)
    acc = {}
    for nu in partitions(n):
        a = kostka(conj(nu), lam)
        if not a: continue
        kf = kostka_foulkes_dict(nu, mp)
        for e, c in kf.items():
            ex = nmp - e
            acc[ex] = acc.get(ex, 0) + a*c
    assert all(e >= 0 for e in acc), ("Ktilde has a negative power", lam, mu, acc)
    return dict_to_FF(acc) / t**nstat(lp)

# ---------------- (d) 0-1 matrices ----------------
def count01(rows, cols):
    rows = list(rows); cols = list(cols)
    if sum(rows) != sum(cols): return 0
    ncol = len(cols)
    from functools import lru_cache
    def rec(i, rem):
        if i == len(rows):
            return 1 if all(c == 0 for c in rem) else 0
        tot = 0
        for S in combinations(range(ncol), rows[i]):
            r = list(rem); ok = True
            for j in S:
                r[j] -= 1
                if r[j] < 0: ok = False; break
            if ok: tot += rec(i+1, tuple(r))
        return tot
    return rec(0, tuple(cols))
