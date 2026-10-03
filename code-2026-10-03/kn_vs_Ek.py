"""
Is Rick's E_k the Kirillov-Noumi raising operator?

KN = Kirillov & Noumi, "q-Difference raising operators for Macdonald polynomials
and the integrality of transition coefficients", arXiv:q-alg/9605005,
CRM Proc. Lecture Notes 22 (1999) 227-243.  Operators (2) of their Introduction,
transcribed from the arXiv LaTeX source (md5 2ee93458dfdc6bf9e57c6eb46aa05cb6):

  K^+_m = sum_{|J|=m} prod_{j in J} x_j sum_{I subset J}
            (-t^{m-n+1})^{|I|} t^{C(|I|,2)}
            prod_{i in I, j in [1,n]\I} (t x_i - x_j)/(x_i - x_j) prod_{i in I} T_{q,x_i}

  K^-_m = sum_{|J|=m} prod_{j in J} x_j sum_{I subset J}
            (-t)^{m-|I|} t^{C(m-|I|,2)}
            prod_{i in I, j notin I} (x_i - t x_j)/(x_i - x_j) prod_{j in [1,n]\I} T_{q,x_j}

KN Theorem A:  K_m J_lam = J_{lam + (1^m)}  for ell(lam) <= m,  J_0 = 1.

Rick's E_k (his sec 0), in HIS parameters (s, t_Rick), with t_Mac = 1/t_Rick, q = s:
  E_k F = sum_{|A|=k} prod_{i in A, j notin A} (x_i - t_R x_j)/(x_i - x_j)
            * X_A * F(X_A -> s X_A)
"""
import sympy as sp
from itertools import combinations

q, tM, tR = sp.symbols('q t_Mac t_Rick')
n = 3
xs = sp.symbols('x1:%d' % (n+1))

def norm(expr):
    expr = sp.cancel(sp.together(sp.expand(expr)))
    return sp.simplify(expr)

def Tq(f, idx, fac):
    return f.subs({xs[i]: fac*xs[i] for i in idx}, simultaneous=True)

def Kplus(f, m, t, qq):
    out = 0
    for J in combinations(range(n), m):
        pref = sp.prod([xs[j] for j in J])
        for r in range(m+1):
            for I in combinations(J, r):
                c = (-t**(m-n+1))**len(I)*t**sp.Rational(len(I)*(len(I)-1), 2)
                for i in I:
                    for j in range(n):
                        if j in I: continue
                        c *= (t*xs[i]-xs[j])/(xs[i]-xs[j])
                out += pref*c*Tq(f, I, qq)
    return norm(out)

def Kminus(f, m, t, qq):
    out = 0
    for J in combinations(range(n), m):
        pref = sp.prod([xs[j] for j in J])
        for r in range(m+1):
            for I in combinations(J, r):
                c = (-t)**(m-r)*t**sp.Rational((m-r)*(m-r-1), 2)
                for i in I:
                    for j in range(n):
                        if j in I: continue
                        c *= (xs[i]-t*xs[j])/(xs[i]-xs[j])
                comp = [j for j in range(n) if j not in I]
                out += pref*c*Tq(f, comp, qq)
    return norm(out)

def E_rick(f, k, t, ss):
    out = 0
    for A in combinations(range(n), k):
        c = sp.prod([xs[i] for i in A])
        for i in A:
            for j in range(n):
                if j in A: continue
                c *= (xs[i]-t*xs[j])/(xs[i]-xs[j])
        out += c*Tq(f, A, ss)
    return norm(out)

e = {k: sp.expand(sum(sp.prod([xs[i] for i in A]) for A in combinations(range(n), k)))
     for k in range(1, n+1)}
e[0] = sp.Integer(1)

print("n = %d variables.  Dictionary: q = s, t_Mac = 1/t_Rick." % n)
print("Comparing on the SAME parameters: set t_Mac = 1/tR throughout.\n")
sub = {tM: 1/tR}

for k in range(1, n+1):
    Ek1 = E_rick(sp.Integer(1), k, tR, q)
    Kp1 = norm(Kplus(sp.Integer(1), k, 1/tR, q))
    Km1 = norm(Kminus(sp.Integer(1), k, 1/tR, q))
    print("k = %d" % k)
    print("   E_k(1)    = %s" % sp.factor(Ek1))
    print("   K^+_k(1)  = %s" % sp.factor(Kp1))
    print("   K^-_k(1)  = %s" % sp.factor(Km1))
    for nm, V in [("K^+", Kp1), ("K^-", Km1)]:
        if sp.simplify(V) == 0: print("      %s_k(1) = 0" % nm); continue
        r = sp.simplify(sp.cancel(Ek1/V))
        print("      E_k(1)/%s_k(1) = %s  (free of x: %s)"
              % (nm, sp.factor(r), not any(r.has(x) for x in xs)))
    # now on a non-constant test input: e_1
    Eke = E_rick(e[1], k, tR, q)
    Kpe = norm(Kplus(e[1], k, 1/tR, q))
    Kme = norm(Kminus(e[1], k, 1/tR, q))
    for nm, V in [("K^+", Kpe), ("K^-", Kme)]:
        if sp.simplify(V) == 0: print("      %s_k(e_1) = 0" % nm); continue
        r = sp.simplify(sp.cancel(Eke/V))
        print("      E_k(e_1)/%s_k(e_1) = %s  (free of x: %s)"
              % (nm, sp.factor(r), not any(r.has(x) for x in xs)))
    print()
