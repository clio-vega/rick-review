"""
Direct check of the two lemmas of Rick's section 5, and of the generating-function
form of Theorem 1 (Gamma_k = T_k), from his own definitions:

  phi(u)   = u(1+suz)/(1+uz)
  a_ij     = (X_i - t X_j)/(X_i - X_j),   prod^x_A = prod_{i in A, j not in A} a_ij
  Gamma_k  = E(z) * sum_{|A|=k} prod^x_A prod_{a in A} phi(X_a)
  T_k      = sum_{j+b<=k} s^b t^{-kj} c(k-b,j) e_b z^{b-k} E(t^j z)

  Lemma 5 (Recursion R): [k] Gamma_k(X) = sum_i X_i(1+sX_i z) prod_{j!=i} a_ij Gamma_{k-1}(Xhat_i)
  Lemma 6 (Step)       : sum_i X_i(1+sX_i z) prod_{j!=i} a_ij T_{k-1}(Xhat_i) = [k] T_k(X)
  Theorem 1 (GF form)  : Gamma_k = T_k

Series in z truncated at order ZT.  Clio 2026-10-15.
"""
import sympy as sp
from itertools import combinations

s, t = sp.Rational(5,7), sp.Rational(3,5)
z = sp.Symbol('z')
ZT = 7                                  # truncation order in z

def ser(expr):
    """truncate a rational-in-z expression to a polynomial mod z^(ZT+1)"""
    return sp.expand(sp.series(sp.together(expr), z, 0, ZT+1).removeO())

def tools(Xs):
    m = len(Xs)
    def a(i, j): return (Xs[i] - t*Xs[j])/(Xs[i] - Xs[j])
    def prodx(A):
        A = set(A); r = sp.Integer(1)
        for i in A:
            for j in range(m):
                if j not in A: r *= a(i, j)
        return r
    def E(arg): return sp.prod([1 + x*arg for x in Xs])
    def e(r):
        if r < 0 or r > m: return sp.Integer(0)
        return sp.expand(sum(sp.prod([Xs[i] for i in c]) for c in combinations(range(m), r)))
    def phi(u): return u*(1+s*u*z)/(1+u*z)
    return m, a, prodx, E, e, phi

def qp(a_, n):
    r = sp.Integer(1)
    for i in range(n): r *= (1 - a_*t**i)
    return r
A = {-1: sp.Integer(0)}
def al(j):
    if j in A: return A[j]
    num = sp.Integer(1)
    for i in range(1, j+1): num *= (s - t**i)
    A[j] = sp.cancel(num/qp(t, j)); return A[j]
def c(n, j):
    if not (0 <= j <= n): return sp.Integer(0)
    return sp.cancel(qp(s, n-j)/qp(t, n-j)*(al(j) - s*t**(n-j)*al(j-1)))

def Gamma(Xs, k):
    m, a, prodx, E, e, phi = tools(Xs)
    if k > m: return sp.Integer(0)
    tot = sp.Integer(0)
    for A_ in combinations(range(m), k):
        tot += prodx(A_)*sp.prod([phi(Xs[i]) for i in A_])
    return sp.cancel(sp.together(E(z)*tot))

def Tk(Xs, k):
    m, a, prodx, E, e, phi = tools(Xs)
    tot = sp.Integer(0)
    for b in range(k+1):
        for j in range(k-b+1):
            tot += s**b*t**(-k*j)*c(k-b, j)*e(b)*z**(b-k)*E(t**j*z)
    return sp.expand(tot)

bracket = lambda k: sp.cancel((1-t**k)/(1-t))

print(f"s={s} t={t}, z-series truncated at order {ZT}\n")
for m in (1, 2, 3):
    Xs = list(sp.symbols(f'X1:{m+1}'))
    print(f"--- m = {m} ---")
    for k in range(1, m+2):
        # Theorem 1, generating-function form
        G = Gamma(Xs, k); T = Tk(Xs, k)
        d = sp.expand(sp.cancel(sp.together((G - T)*z**k)))
        okT1 = sp.simplify(ser(d)) == 0 if d != 0 else True
        # Lemma 5 (Recursion)
        rec = sp.Integer(0)
        for i in range(m):
            Xh = [x for jj, x in enumerate(Xs) if jj != i]
            w = sp.prod([(Xs[i]-t*Xs[j])/(Xs[i]-Xs[j]) for j in range(m) if j != i])
            rec += Xs[i]*(1+s*Xs[i]*z)*w*(Gamma(Xh, k-1) if k >= 1 else 0)
        d5 = sp.cancel(sp.together(bracket(k)*Gamma(Xs, k) - rec))
        ok5 = sp.simplify(ser(d5)) == 0 if d5 != 0 else True
        # Lemma 6 (Step)
        stp = sp.Integer(0)
        for i in range(m):
            Xh = [x for jj, x in enumerate(Xs) if jj != i]
            w = sp.prod([(Xs[i]-t*Xs[j])/(Xs[i]-Xs[j]) for j in range(m) if j != i])
            stp += Xs[i]*(1+s*Xs[i]*z)*w*Tk(Xh, k-1)
        d6 = sp.expand(sp.cancel(sp.together((stp - bracket(k)*Tk(Xs, k))*z**k)))
        ok6 = sp.simplify(d6) == 0
        print(f"   k={k}:  Thm1(GF) {'OK ' if okT1 else 'FAIL'}   "
              f"Lemma5(Recursion) {'OK ' if ok5 else 'FAIL'}   "
              f"Lemma6(Step) {'OK ' if ok6 else 'FAIL'}")

print("\n--- m = 0 (the branch handled by one sentence in the note) ---")
for k in (1,2,3,4):
    T = sp.expand(sum(s**b*t**(-k*j)*c(k-b,j)*(1 if b==0 else 0)*z**(b-k)
                      for b in range(k+1) for j in range(k-b+1)))
    print(f"   k={k}:  T_k(no variables) = {sp.simplify(T)}    Gamma_k = 0   "
          f"-> {'equal' if sp.simplify(T)==0 else 'NOT EQUAL'}")

print("\n--- F2's quantification: sum_i prod_{j!=i} a_ij =?= [m]_t  (the g=1 failure) ---")
for m in (1,2,3,4):
    Xs = list(sp.symbols(f'X1:{m+1}'))
    v = sp.simplify(sum(sp.prod([(Xs[i]-t*Xs[j])/(Xs[i]-Xs[j]) for j in range(m) if j!=i])
                        for i in range(m)))
    print(f"   m={m}: {v}   [m]_t = {sp.cancel((1-t**m)/(1-t))}  -> "
          f"{'match' if sp.simplify(v-(1-t**m)/(1-t))==0 else 'MISMATCH'}")

print("\n--- Macdonald III (2.9) residue lemma, n>=1, and its n=0 failure ---")
for m in (2,3):
    Xs = list(sp.symbols(f'X1:{m+1}'))
    def R(n):
        return sp.simplify((1-t)*sum(Xs[i]**n*sp.prod([(Xs[i]-t*Xs[j])/(Xs[i]-Xs[j])
                           for j in range(m) if j!=i]) for i in range(m)))
    Q = sp.series(sp.prod([(1-t*x*sp.Symbol('y'))/(1-x*sp.Symbol('y')) for x in Xs]),
                  sp.Symbol('y'), 0, 5).removeO()
    for n in range(0,4):
        qn = sp.simplify(sp.expand(Q).coeff(sp.Symbol('y'), n))
        print(f"   m={m} n={n}: (1-t)sum = {R(n)} ;  q_{n} = {qn} ; "
              f"{'EQUAL' if sp.simplify(R(n)-qn)==0 else 'DIFFER  <-- expected at n=0'}")
