"""
Symbol-by-symbol test of Rick's open question (UID 803, item 1):
is Hikita's level-one Y_i the same operator as DFK19's Y_{i,1}?

DFK = Di Francesco-Kedem, arXiv:1704.00154, deformDAHA.tex
  rho(X_i) f            = x_i f                                        (l.125)
  rho(s_i) f            = f with x_i <-> x_{i+1}                        (l.126)
  rho(T_i)              = th*s_i + (th-th^-1)/(x_i x_{i+1}^-1 - 1)*(s_i-1)  (l.127)
  rho(pi) f(x_1..x_N)   = f(x_2,...,x_N, q^-1 x_1)                      (l.132)
  rho(Y_i)              = T_i T_{i+1}...T_{N-1} pi^-1 T_1^-1...T_{i-1}^-1  (l.133)
  Y_{i,n}               = (X_1..X_{i-1})^-n Y_i (X_1..X_i)^n            (Def 2.6, l.184)

Hikita (level one polynomial representation of H_m, /tmp/hikita.txt l.488-499):
  T_i . F = t s_i(F) + (t-1)(F - s_i F)/(1 - X_i X_{i+1}^-1)            (his eq (1))
  Pi  . F = X_1 F(X_2,...,X_m,X_{m+1}),  X_{m+1} = q^-1 X_1             (his eq (2))
  Y^H_i   = same DAHA word as DFK's, in HIS generators.

Dictionary under test: t_Hikita = th_DFK^2.
"""
import sympy as sp

def engine(N):
    x = sp.symbols(f'x1:{N+1}', positive=True)
    q, th = sp.symbols('q theta', positive=True)
    t = th**2                      # the dictionary being tested
    X = list(x)

    def s(i, f):                   # 1-indexed simple transposition
        a, b = X[i-1], X[i]
        return f.subs({a: b, b: a}, simultaneous=True)

    def T_dfk(i, f):
        r = X[i-1]/X[i]
        return sp.together(th*s(i, f) + (th - 1/th)/(r - 1)*(s(i, f) - f))

    def Tinv_dfk(i, f):            # rho(T_i^-1) = rho(T_i) - th + th^-1   (l.130)
        return sp.together(T_dfk(i, f) - th*f + f/th)

    def T_hik(i, f):
        r = X[i-1]/X[i]
        return sp.together(t*s(i, f) + (t - 1)/(r - 1)*(s(i, f) - f))

    def Tinv_hik(i, f):            # from (T_i-t)(T_i+1)=0: T^-1 = (T - (t-1))/t
        return sp.together((T_hik(i, f) - (t-1)*f)/t)

    def pi(f):                     # f |-> f(x_2,...,x_N,q^-1 x_1)
        sub = {X[k]: X[k+1] for k in range(N-1)}
        sub[X[N-1]] = X[0]/q
        return f.subs(sub, simultaneous=True)

    def pi_inv(f):
        sub = {X[k+1]: X[k] for k in range(N-1)}
        sub[X[0]] = q*X[N-1]
        return f.subs(sub, simultaneous=True)

    def Pi_hik_inv(f):             # Pi = mult_{x_1} o pi  =>  Pi^-1 = pi^-1 o (/x_1)
        return pi_inv(sp.cancel(f/X[0]))

    def word(f, i, Tf, Tif, piinv):
        """T_i T_{i+1}...T_{N-1} pi^-1 T_1^-1...T_{i-1}^-1 applied to f (rightmost first)."""
        g = f
        for j in range(i-1, 0, -1):      # T_1^-1...T_{i-1}^-1, rightmost = T_{i-1}^-1
            g = Tif(j, g)
        g = piinv(g)
        for j in range(N-1, i-1, -1):    # T_i...T_{N-1}, rightmost = T_{N-1}
            g = Tf(j, g)
        return sp.cancel(sp.together(g))

    def Y_dfk(i, f):   return word(f, i, T_dfk, Tinv_dfk, pi_inv)
    def Y_hik(i, f):   return word(f, i, T_hik, Tinv_hik, Pi_hik_inv)

    def Y_dfk_n(i, n, f):
        """Y_{i,n} = (X_1..X_{i-1})^-n Y_i (X_1..X_i)^n"""
        pre  = sp.prod(X[:i])            # X_1..X_i
        post = sp.prod(X[:i-1])          # X_1..X_{i-1}
        return sp.cancel(Y_dfk(i, sp.expand(pre**n * f)) / post**n)

    return x, q, th, X, Y_dfk, Y_hik, Y_dfk_n, pi, pi_inv

# sanity: pi o pi^-1 = id, and the two T's differ by exactly the factor theta
print("=== CONTROL 0: instrument sanity ===")
for N in (2, 3):
    x, q, th, X, Y_dfk, Y_hik, Y_dfk_n, pi, pi_inv = engine(N)
    f = sp.prod([X[k]**(k+1) for k in range(N)]) + X[0]
    print(f"  N={N}  pi(pi^-1(f))-f = {sp.simplify(pi(pi_inv(f)) - f)}")

print("\n=== MAIN TEST: Y^H_i  vs  Y^DFK_{i,1} ===")
for N in (2, 3):
    x, q, th, X, Y_dfk, Y_hik, Y_dfk_n, pi, pi_inv = engine(N)
    # test on a basis of Laurent monomials
    tests = []
    if N == 2:
        tests = [(0,0), (1,0), (0,1), (2,1), (1,-1), (3,2)]
    else:
        tests = [(0,0,0), (1,0,0), (0,1,0), (0,0,1), (2,1,0), (1,1,1), (2,-1,1)]
    for i in range(1, N+1):
        ratios = set()
        for e in tests:
            f = sp.prod([X[k]**e[k] for k in range(N)])
            a = sp.cancel(sp.simplify(Y_hik(i, f)))
            b = sp.cancel(sp.simplify(Y_dfk_n(i, 1, f)))
            if b == 0:
                ratios.add('b=0' if a != 0 else 'both0'); continue
            r = sp.simplify(sp.cancel(a/b))
            ratios.add(sp.nsimplify(sp.powsimp(r)))
        print(f"  N={N} i={i}:  Y^H_i / Y^DFK_(i,1) over {len(tests)} monomials -> {ratios}")
