"""POSITIVE CONTROLS on the instrument, before trusting any negative result.
 C1: Hikita l.544 "the elements Y_1,...,Y_m mutually commute"  -> must hold.
 C2: DFK Lemma 2.7 (commuYin): {Y_{i,n}} commute for fixed n   -> must hold.
 C3: DFK l.189 "Y_{1,n} = Y_1 X_1^n"                           -> must hold.
 C4: DFK l.196 "Y_{N,n} = q^n X_N^n Y_N"                       -> must hold.
 C5 (NEGATIVE): a deliberately wrong word order must BREAK C1.
"""
import sympy as sp
exec(open('hikita_dfk_Y_match2.py').read().split('print("=== Y^H')[0])

for N in (2, 3):
    x, q, th, X, Y_hik, Y_dfk_n = engine(N)
    tests = [tuple(1 if k == 0 else 0 for k in range(N)), tuple(1 for _ in range(N))]
    if N == 2: tests += [(2, 1), (1, -1)]
    else:      tests += [(2, 1, 0), (0, 1, 2)]
    print(f"--- N={N} ---")
    # C1
    bad = 0
    for e in tests:
        f = sp.prod([X[k]**e[k] for k in range(N)])
        for i in range(1, N+1):
            for j in range(i+1, N+1):
                d = sp.simplify(sp.cancel(Y_hik(i, Y_hik(j, f)) - Y_hik(j, Y_hik(i, f))))
                if d != 0: bad += 1
    print(f"  C1 Hikita Y_i commute: {'PASS' if bad==0 else f'FAIL ({bad})'}")
    # C2
    for n in (0, 1):
        bad = 0
        for e in tests:
            f = sp.prod([X[k]**e[k] for k in range(N)])
            for i in range(1, N+1):
                for j in range(i+1, N+1):
                    a = Y_dfk_n(i, n, Y_dfk_n(j, n, f)); b = Y_dfk_n(j, n, Y_dfk_n(i, n, f))
                    if sp.simplify(sp.cancel(a-b)) != 0: bad += 1
        print(f"  C2 DFK Y_(i,{n}) commute: {'PASS' if bad==0 else f'FAIL ({bad})'}")
    # C3 / C4
    for n in (1, 2):
        bad3 = bad4 = 0
        for e in tests:
            f = sp.prod([X[k]**e[k] for k in range(N)])
            lhs3 = Y_dfk_n(1, n, f); rhs3 = Y_dfk_n(1, 0, sp.expand(X[0]**n*f))
            if sp.simplify(sp.cancel(lhs3-rhs3)) != 0: bad3 += 1
            lhs4 = Y_dfk_n(N, n, f); rhs4 = sp.expand(q**n*X[N-1]**n*Y_dfk_n(N, 0, f))
            if sp.simplify(sp.cancel(lhs4-rhs4)) != 0: bad4 += 1
        print(f"  C3 Y_(1,{n})=Y_1 X_1^{n}: {'PASS' if bad3==0 else f'FAIL ({bad3})'}"
              f"   C4 Y_(N,{n})=q^{n}X_N^{n}Y_N: {'PASS' if bad4==0 else f'FAIL ({bad4})'}")

# C5 negative control: reverse Hikita's left T-block -> commutation must break
print("--- C5 NEGATIVE CONTROL (wrong word order must break C1) ---")
N = 3
x, q, th, X, _, _ = engine(N)
def engine_bad(N):
    import sympy as sp
    g = engine(N)
    return g
x, q, th, X, Y_hik, Y_dfk_n = engine(3)
t = th**2
def s(i,f):
    a,b = X[i-1], X[i]; return f.subs({a:b,b:a}, simultaneous=True)
def T_hik(i,f):
    r = X[i-1]/X[i]; return sp.together(t*s(i,f)+(t-1)/(r-1)*(s(i,f)-f))
def Tinv_hik(i,f): return sp.together((T_hik(i,f)-(t-1)*f)/t)
def pi(f):
    sub={X[k]:X[k+1] for k in range(N-1)}; sub[X[N-1]]=X[0]/q
    return f.subs(sub, simultaneous=True)
def Pi(f): return sp.expand(X[0]*pi(f))
def Y_bad(i,f):           # left block ASCENDING instead of descending
    g=f
    for j in range(i,N): g=Tinv_hik(j,g)
    g=Pi(g)
    for j in range(i-1,0,-1): g=T_hik(j,g)
    return sp.cancel(sp.together(t**(N-i)*g))
bad=0
for e in [(1,0,0),(1,1,1),(2,1,0)]:
    f=sp.prod([X[k]**e[k] for k in range(N)])
    for i in range(1,N+1):
        for j in range(i+1,N+1):
            if sp.simplify(sp.cancel(Y_bad(i,Y_bad(j,f))-Y_bad(j,Y_bad(i,f))))!=0: bad+=1
print(f"  C5 wrong-order Y commute: {'BROKE as required' if bad>0 else 'DID NOT BREAK -- control is vacuous!'} ({bad} noncommuting pairs)")
