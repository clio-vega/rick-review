"""
Clio, 2026-10-02 peer review of Rick's (N) / DFK novelty note.
Symbolic check of the Di Francesco-Kedem dictionary Rick asks me to verify.

INSTRUMENT VALIDATION FIRST (standing discipline): each block below must
reproduce a value established independently before any of its zeros are believed.
"""
import sympy as sp

s, t, z = sp.symbols('s t z', positive=True)
N = 4
x = sp.symbols('x1:%d' % (N+1))

# ---- DFK (1.5), generalized Macdonald operator M_{alpha;n}, as Rick quotes it:
#   M_{a;n} = sum_{|I|=a} x_I^n prod_{i in I, j notin I} (t_DFK x_i - x_j)/(x_i - x_j) Gamma_I
# Gamma_i : x_i -> q_DFK x_i.
# Represented as a list of (coefficient, shift-set) pairs acting on polynomials.
from itertools import combinations

def M(alpha, n, qD, tD):
    terms = []
    for I in combinations(range(N), alpha):
        Ic = [j for j in range(N) if j not in I]
        c = sp.prod([x[i] for i in I])**n
        for i in I:
            for j in Ic:
                c *= (tD*x[i] - x[j])/(x[i] - x[j])
        terms.append((sp.together(c), I, qD))
    return terms

# ---- Rick's E_k (his (N) paper, Section 1):
#   E_k F = sum_{|A|=k} prodx_A * X_A * F(X_{A^c}, s X_A),  a_ij = (x_i - t x_j)/(x_i - x_j)
def E(k):
    terms = []
    for A in combinations(range(N), k):
        Ac = [j for j in range(N) if j not in A]
        c = sp.prod([x[i] for i in A])
        for i in A:
            for j in Ac:
                c *= (x[i] - t*x[j])/(x[i] - x[j])
        terms.append((sp.together(c), A, s))
    return terms

def apply(terms, F):
    out = 0
    for c, I, shift in terms:
        sub = {x[i]: shift*x[i] for i in I}
        out += c*F.subs(sub, simultaneous=True)
    return sp.simplify(sp.together(out))

# ===== CHECK 0 (instrument validation): E_1 must reproduce Macdonald's D_1 =====
# Rick: a_ij = t*(tau x_i - x_j)/(x_i - x_j) with tau = 1/t, so E_1 = t^{N-1} sum_i A_i x_i T_{s,i}.
tau = 1/t
D1 = []
for i in range(N):
    c = sp.prod([(tau*x[i] - x[j])/(x[i] - x[j]) for j in range(N) if j != i])
    D1.append((sp.together(c), (i,), s))
testF = x[0]**2*x[1] + x[2]*x[3] + 1
lhs = apply(E(1), testF)
rhs = sp.simplify(t**(N-1)*apply([(c*x[i], (i,), s) for (c,(i,),_), i in zip(D1, range(N))], testF))
print("CHECK 0  E_1 == t^(N-1) * sum_i A_i x_i T_{s,i}   :", sp.simplify(lhs - rhs) == 0)

# ===== CHECK 1: Rick's dictionary  E_k = t^{k(N-k)} M_{k;1}|_{(q,t)_DFK=(s,1/t)} =====
print()
for k in range(1, N):
    Mk = M(k, 1, s, 1/t)
    lhs = apply(E(k), testF)
    rhs = sp.simplify(t**(k*(N-k))*apply(Mk, testF))
    ok = sp.simplify(sp.expand(lhs - rhs)) == 0
    print("CHECK 1  k=%d  E_k == t^{k(N-k)} M_{k;1}|_{(q,t)=(s,1/t)} : %s" % (k, ok))

# ===== CHECK 2: eigenvalue dictionary =====
# DFK Rem 2.14 / (4.14):  nabla^{(N)} P_lam = C_N * u_lam * P_lam,
#   u_lam = tD^{(N-1)|lam|/2 - n(lam)} * qD^{|lam|/2 + n(lam')}
# Rick: N P_nu = t^{n(nu)} s^{n(nu')} P_nu, claimed to be the "pure eigenvalue part".
print()
def n_lam(lam):  return sum(i*p for i, p in enumerate(lam))
def conj(lam):
    return [sum(1 for p in lam if p > j) for j in range(max(lam))] if lam and max(lam) else []
for lam in [[1],[2],[1,1],[3],[2,1],[1,1,1],[3,2,1],[4,2,2,1]]:
    u = (1/t)**(sp.Rational(N-1,2)*sum(lam) - n_lam(lam)) * s**(sp.Rational(1,2)*sum(lam) + n_lam(conj(lam)))
    pure = t**n_lam(lam) * s**n_lam(conj(lam))
    grading = ((1/t)**sp.Rational(N-1,2) * s**sp.Rational(1,2))**sum(lam)
    print("CHECK 2  lam=%-12s u_lam == (grading)*(t^n(lam) s^n(lam')) : %s"
          % (lam, sp.simplify(u - grading*pure) == 0))

# ===== CHECK 3: the t^{-C(k,2)} prefactor in (N) is exactly N's eigenvalue on e_k =====
# e_k = P_{1^k}, so N e_k = t^{n(1^k)} s^{n((1^k)')} e_k = t^{C(k,2)} e_k.
print()
for k in range(1, 7):
    lam = [1]*k
    ev_t, ev_s = n_lam(lam), n_lam(conj(lam))
    print("CHECK 3  k=%d  N e_k = t^%d s^%d e_k   (want t^C(k,2)=t^%d, s^0) : %s"
          % (k, ev_t, ev_s, k*(k-1)//2, (ev_t == k*(k-1)//2 and ev_s == 0)))
