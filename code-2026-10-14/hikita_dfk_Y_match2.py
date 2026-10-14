"""
Corrected test. Hikita's eq (3) (/tmp/hikita.txt l.541):
    Y^H_i := t^{m-i} T_{i-1}T_{i-2}...T_1 Pi T_{m-1}^-1 T_{m-2}^-1 ... T_i^-1
and his own note (l.543): "our Y_i essentially corresponds to Y_i^{-1} in the
usual convention for DAHA (see e.g. [6])."

DFK (1704.00154) l.80/133:  Y^D_i = T_i T_{i+1}...T_{N-1} pi^-1 T_1^-1...T_{i-1}^-1
         Def 2.6  l.184:    Y^D_{i,n} = (X_1..X_{i-1})^-n Y^D_i (X_1..X_i)^n

Formally  (Y^D_i)^{-1} = T_{i-1}...T_1 . pi . T_{N-1}^-1...T_i^-1, which is Hikita's
word with Pi for pi. So we test  Y^H_i o Y^D_{i,n} = scalar  for n in {0,1}.
Dictionary: t_Hikita = theta_DFK^2.
"""
import sympy as sp

def engine(N):
    x = sp.symbols(f'x1:{N+1}', positive=True)
    q, th = sp.symbols('q theta', positive=True)
    t = th**2
    X = list(x)
    def s(i, f):
        a, b = X[i-1], X[i]
        return f.subs({a: b, b: a}, simultaneous=True)
    def T_dfk(i, f):
        r = X[i-1]/X[i]
        return sp.together(th*s(i,f) + (th - 1/th)/(r-1)*(s(i,f)-f))
    def Tinv_dfk(i, f):
        return sp.together(T_dfk(i,f) - th*f + f/th)
    def T_hik(i, f):
        r = X[i-1]/X[i]
        return sp.together(t*s(i,f) + (t-1)/(r-1)*(s(i,f)-f))
    def Tinv_hik(i, f):
        return sp.together((T_hik(i,f) - (t-1)*f)/t)
    def pi(f):
        sub = {X[k]: X[k+1] for k in range(N-1)}; sub[X[N-1]] = X[0]/q
        return f.subs(sub, simultaneous=True)
    def pi_inv(f):
        sub = {X[k+1]: X[k] for k in range(N-1)}; sub[X[0]] = q*X[N-1]
        return f.subs(sub, simultaneous=True)
    def Pi_hik(f):                      # Pi . F = X_1 * F(X_2,..,X_m,q^-1 X_1)
        return sp.expand(X[0]*pi(f))

    def Y_hik(i, f):
        """t^{m-i} T_{i-1}..T_1 Pi T_{N-1}^-1..T_i^-1  (rightmost acts first)"""
        g = f
        for j in range(i, N):            # T_{N-1}^-1..T_i^-1 : rightmost is T_i^-1
            g = Tinv_hik(j, g)
        g = Pi_hik(g)
        for j in range(1, i):            # T_{i-1}..T_1 : rightmost is T_1
            g = T_hik(j, g)
        return sp.cancel(sp.together(t**(N-i)*g))

    def Y_dfk(i, f):
        g = f
        for j in range(i-1, 0, -1):      # T_1^-1..T_{i-1}^-1 : rightmost T_{i-1}^-1
            g = Tinv_dfk(j, g)
        g = pi_inv(g)
        for j in range(N-1, i-1, -1):    # T_i..T_{N-1} : rightmost T_{N-1}
            g = T_dfk(j, g)
        return sp.cancel(sp.together(g))

    def Y_dfk_n(i, n, f):
        pre, post = sp.prod(X[:i]), sp.prod(X[:i-1])
        return sp.cancel(Y_dfk(i, sp.expand(pre**n*f))/post**n)
    return x, q, th, X, Y_hik, Y_dfk_n

print("=== Y^H_i  o  Y^D_{i,n}  =?  scalar * identity ===")
for N in (2, 3):
    x, q, th, X, Y_hik, Y_dfk_n = engine(N)
    tests = [tuple(0 for _ in range(N)), tuple(1 if k==0 else 0 for k in range(N)),
             tuple(1 for _ in range(N))]
    if N == 2: tests += [(2,1), (1,-1), (3,2)]
    else:      tests += [(2,1,0), (0,1,2), (2,-1,1)]
    for n in (0, 1):
        for i in range(1, N+1):
            vals = set()
            for e in tests:
                f = sp.prod([X[k]**e[k] for k in range(N)])
                comp = Y_hik(i, Y_dfk_n(i, n, f))
                r = sp.simplify(sp.cancel(comp/f))
                vals.add(sp.powsimp(sp.nsimplify(r)))
            ok = len(vals) == 1 and all(len(v.free_symbols & set(x)) == 0 for v in vals)
            print(f"  N={N} n={n} i={i}: {'SCALAR ' if ok else 'not scalar'} -> {vals if len(vals)<=2 else str(len(vals))+' distinct'}")
