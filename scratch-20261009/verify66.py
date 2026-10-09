"""
Independent implementation of the PRINTED Theorem 6.6 of Rick's FPSAC 2027 draft
(commit 0dcdc5e, p.10), built only from the printed statements of
Prop 3.3, Lemma 3.9, Thm 6.3, Example 6.5, Thm 6.6.  No access to Rick's code.
Target: the two Lead values printed in Example 6.8.
"""
import sympy as sp
from itertools import permutations

t = sp.symbols('t')

def br(n):                      # [n]  = (1-t^n)/(1-t)
    return sp.cancel((1-t**n)/(1-t))

def br_at(n, r):                # [n]_{t^r} = (1-t^{nr})/(1-t^r)
    if r == 0:
        return sp.Integer(n)
    return sp.cancel((1-t**(n*r))/(1-t**r))

def L(a, b):                    # Prop 3.3
    return sp.cancel((1-t**(a+b))*(t**(a*b)-1)/((1-t**a)*(1-t**b)))

# ---- elements of Lambda as dicts: sorted tuple of e-indices (e_0 dropped) -> coeff
def mono(idxs):
    return tuple(sorted(i for i in idxs if i != 0))

def add(D, key, val):
    D[key] = sp.cancel(D.get(key, 0) + val)
    if D[key] == 0:
        del D[key]

def M(k, r):
    """Prop 3.3, extended to all k,r>=0 by the symmetry M_kl=M_lk of Thm 3.2."""
    k, r = max(k, r), min(k, r)
    D = {}
    if r == 0:
        return D                      # M_{k,0}=0, consistent with D_k(1)=0
    add(D, mono([k, r]), sp.Integer(r))
    for j in range(1, r+1):
        add(D, mono([k+j, r-j]), L(k-r+j, j))
    return D

def Dder(a, D):
    """Derivation D_a with D_a(e_j)=M_aj, applied to a dict."""
    out = {}
    for m, co in D.items():
        for pos, j in enumerate(m):
            rest = m[:pos] + m[pos+1:]
            for m2, co2 in M(a, j).items():
                add(out, mono(rest + m2), co*co2)
    return out

def Xi(a, r, q):                # Thm 6.6 display; = lin_e T_a(p_r p_q) by Lemma 3.9
    return sp.cancel((-1)**(r+q) * br(a+r+q)/br(a) * br_at(a, r) * br_at(a, q))

def Xi_via_lemma39(a, r, q):
    """Independent route: Lemma 3.9  lin_e T_k f = (-1)^d [n]/[k] f(1,t,...,t^{k-1})."""
    d = r+q
    n = a+d
    pr = sum(t**(i*r) for i in range(a))      # p_r(1,t,...,t^{a-1})
    pq = sum(t**(i*q) for i in range(a))
    return sp.cancel((-1)**d * br(n)/br(a) * pr * pq)

def Phi(a, b, c, x, y):
    """Thm 6.3 for g = p_b p_c (degree d=b+c, g in Lambda_a)."""
    # G_A(w) = g(1,t,...,t^{A-1}, w,wt,...,wt^{B-1});  p_r -> [A]_{t^r} + w^r [B]_{t^r}
    def Gcoeff(A, B, k):
        pb0, pbw = br_at(A, b), br_at(B, b)
        pc0, pcw = br_at(A, c), br_at(B, c)
        # NB: accumulate, do NOT use a dict literal -- when b==c the keys collide
        terms = [(0, pb0*pc0), (b, pbw*pc0), (c, pb0*pcw), (b+c, pbw*pcw)]
        tot = 0
        for deg, co in terms:
            if deg == k:
                tot += co
        return sp.cancel(tot)
    total = 0
    for A in range(1, a):
        B = a - A
        inner = Gcoeff(A, B, y-B)/((1-t**A)*(1-t**B))
        s = 0
        for m in range(1, y-B+1):           # G_{A,k}=0 for k<0
            s += (t**(-A*m) - t**(B*m))*Gcoeff(A, B, y-B-m)
        inner += s/(1-t**a)
        total += t**(-A*B)*inner
    gspec = sp.cancel(br_at(a, b)*br_at(a, c))   # g(1,t,...,t^{a-1})
    total -= gspec/(1-t**a)*sum(t**(-j*y) for j in range(a))
    return sp.cancel((-1)**a * (1-t**x)*(1-t**y) * total)

def thm66(a, b, c, x, y):
    n = x + y
    m_xy = 2 if x == y else 1
    U = sp.cancel(((-1)**n * Phi(a, b, c, x, y) - Xi(a, b, c))/m_xy)
    tot = (-1)**(b+c) * U
    for r in range(1, b):
        if {b-r, a+r+c} == {x, y}:
            tot += (-1)**(r+c)*Xi(a, r, c)
    for q in range(1, c):
        if {c-q, a+b+q} == {x, y}:
            tot += (-1)**(b+q)*Xi(a, b, q)
    tot += Dder(a, M(b, c)).get(mono([x, y]), 0)     # [e_x e_y] D_a(M_bc)
    return sp.cancel(sp.expand(sp.simplify(tot)))

# ---------------- checks ----------------
ok = 0; bad = 0
def check(name, got, want):
    global ok, bad
    d = sp.simplify(sp.expand(sp.together(got - want)))
    if d == 0:
        ok += 1; print("  PASS  %s" % name)
    else:
        bad += 1; print("  FAIL  %s   diff=%s" % (name, d))

print("== A. Xi_a(r,q) printed form  vs  Lemma 3.9 applied to p_r p_q ==")
for a in range(1, 5):
    for r in range(1, 4):
        for q in range(1, 4):
            check("a=%d r=%d q=%d" % (a, r, q), Xi(a, r, q), Xi_via_lemma39(a, r, q))

print("== B. Example 6.8, first value: (3,3,3) -> (7,2) ==")
want1 = 2*t**13+3*t**12+3*t**11+6*t**10+6*t**9+6*t**8+9*t**7+6*t**6+3*t**5+9*t**4+6*t**3+3*t+4
check("(3,3,3)->(7,2)", thm66(3, 3, 3, 7, 2), want1)

print("== C. Example 6.8, second value: (4,4,2) -> (7,3), ALL orderings of (a,b,c) ==")
want2 = sp.expand((t+1)*(t**2+1)*(2*t**8+t**7+t**6+3*t**4+t**3+t**2-t+2))
seen = set()
for (a, b, c) in set(permutations((4, 4, 2))):
    check("a=%d b=%d c=%d" % (a, b, c), thm66(a, b, c, 7, 3), want2)

print("== D. x<->y symmetry of Thm 6.3 RHS (not manifest in the printed formula) ==")
for (a, b, c, x, y) in [(3,3,3,7,2), (4,4,2,7,3), (2,3,1,4,2), (3,2,2,5,2)]:
    check("Phi a=%d b=%d c=%d (%d,%d)vs(%d,%d)" % (a,b,c,x,y,y,x),
          Phi(a,b,c,x,y), Phi(a,b,c,y,x))

print()
print("TOTAL pass=%d fail=%d" % (ok, bad))
