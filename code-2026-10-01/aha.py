"""Independent AHA implementation: T_i, pi, Y_i from Hikita's conventions as quoted in
Rick's 207b note; verify (A_k) Prop 3, (K_k) Prop 4, (C1)-(C3), and (0.1)."""
import itertools, sympy as sp
from sympy import symbols, simplify, cancel, expand, together, Rational
s, t, z = symbols('s t z')

def xs(m): return list(symbols('x1:%d'%(m+1)))

def act_si(F, X, i):
    """swap X[i], X[i+1]  (0-indexed i means s_{i+1} in 1-indexed)"""
    a, b = X[i], X[i+1]
    return F.subs({a: b, b: a}, simultaneous=True)

def T(F, X, i):
    """T_i, i 1-indexed: T_i F = t s_i F + (t-1) X_{i+1} (s_i F - F)/(X_i - X_{i+1})"""
    j = i-1
    sF = act_si(F, X, j)
    return sp.cancel(sp.together(t*sF + (t-1)*X[j+1]*(sF-F)/(X[j]-X[j+1])))

def Tinv(F, X, i):
    """T_i^{-1} = (1/t)(T_i - (t-1))"""
    return sp.cancel((T(F,X,i) - (t-1)*F)/t)

def pi(F, X):
    """pi F = X_1 F(X_2,...,X_m, s X_1)"""
    m = len(X)
    sub = {X[i]: X[i+1] for i in range(m-1)}
    sub[X[m-1]] = s*X[0]
    return sp.cancel(X[0]*F.subs(sub, simultaneous=True))

def Y(F, X, i):
    """Y_i = t^{m-i} T_{i-1}...T_1 pi T_{m-1}^{-1}...T_i^{-1}"""
    m = len(X)
    G = F
    for j in range(i, m):           # T_{m-1}^{-1}...T_i^{-1}: rightmost T_i^{-1} acts FIRST
        G = Tinv(G, X, j)
    G = pi(G, X)
    for j in range(1, i):           # T_{i-1} ... T_1 : rightmost is T_1
        G = T(G, X, j)              # apply T_1 first, then T_2, ... T_{i-1}
    return sp.cancel(t**(m-i)*G)

def ek_Y(k, F, X):
    """e_k(Y) F = sum_{b_1<...<b_k} Y_{b_1}...Y_{b_k} F (increasing product, leftmost = smallest)"""
    m = len(X)
    tot = 0
    for b in itertools.combinations(range(1, m+1), k):
        G = F
        for i in reversed(b):       # rightmost operator acts first
            G = Y(G, X, i)
        tot += G
    return sp.cancel(sp.together(tot))

def e_poly(r, X):
    if r == 0: return sp.Integer(1)
    return sum(sp.prod(c) for c in itertools.combinations(X, r))

def kernel_A(A, X):
    m = len(X); As = set(A); out = sp.Integer(1)
    for i in A:
        for j in range(m):
            if j in As: continue
            out *= (X[i]-t*X[j])/(X[i]-X[j])
    return out

def subset_formula(k, F, X):
    """(0.1):  sum_{|A|=k} prodx_A * X_A * F(x_a -> s x_a, a in A)"""
    m = len(X); tot = 0
    for A in itertools.combinations(range(m), k):
        mon = sp.prod([X[a] for a in A])
        sub = {X[a]: s*X[a] for a in A}
        tot += kernel_A(A, X)*mon*F.subs(sub, simultaneous=True)
    return sp.cancel(sp.together(tot))

def w_of_D(D, m):
    """word (s_{d1-1}..s_1)(s_{d2-1}..s_2)...  as list of 1-indexed generator indices,
    leftmost first. D is 1-indexed sorted."""
    word = []
    for l, d in enumerate(D, start=1):
        word += list(range(d-1, l-1, -1))
    return word

def T_word(F, X, word):
    """apply T_{word[0]} ... T_{word[-1]} ; rightmost acts first"""
    G = F
    for i in reversed(word):
        G = T(G, X, i)
    return G

def sigma_k(k, F, X):
    """sigma^{(k)} = sum_{|D|=k} T_{w(D)}"""
    m = len(X); tot = 0
    for D in itertools.combinations(range(1, m+1), k):
        tot += T_word(F, X, w_of_D(list(D), m))
    return sp.cancel(sp.together(tot))

def pi_pow(k, F, X):
    G = F
    for _ in range(k): G = pi(G, X)
    return G
