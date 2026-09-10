"""Independent re-derivation of Rick's three OEIS sequences (Day 183).
Everything from scratch: b_k from the algebraic equation by iteration,
a_k by INVERTi, p_k by graded Witt.  No use of Rick's numbers as input.
"""
import sympy as sp

N = 14
th = sp.symbols('theta')

# ---- b_k : solve F(1-F)^3(3-4F) = theta (3-2F)^2 as a power series -------
# Iterate F <- theta (3-2F)^2 / ((1-F)^3 (3-4F))  -- fixed point, F = O(theta)
F = sp.Integer(0)
for _ in range(N + 2):
    F = sp.series(th * (3 - 2*F)**2 / ((1 - F)**3 * (3 - 4*F)), th, 0, N + 1).removeO()
    F = sp.expand(F)
    F = sum(sp.nsimplify(sp.expand(F).coeff(th, k)) * th**k for k in range(1, N + 1))
b = [sp.Integer(0)] + [sp.nsimplify(F.coeff(th, k)) for k in range(1, N)]
print("b_k =", [int(x) for x in b[1:13]])

# sanity: plug back into the defining equation
lhs = sp.expand(F*(1-F)**3*(3-4*F)); rhs = sp.expand(th*(3-2*F)**2)
resid = sp.expand(lhs - rhs)
low = min([k for k in range(0, 40) if sp.expand(resid.coeff(th,k)) != 0] or [999])
print("defining eqn residual: lowest nonzero order theta^%s (should exceed 12)" % low)

# ---- a_k : INVERTi.  B(x) = 1 + sum b_k x^k,  A(x) = 1 - 1/B(x) --------
x = sp.symbols('x')
B = 1 + sum(b[k]*x**k for k in range(1, N))
A = sp.series(1 - 1/B, x, 0, N).removeO()
a = [sp.Integer(0)] + [sp.nsimplify(sp.expand(A).coeff(x, k)) for k in range(1, N)]
print("a_k =", [int(v) for v in a[1:13]])

# ---- p_k : graded Witt,  sum p_k t^k = sum_d mu(d)/d log B(t^d) --------
t = sp.symbols('t')
Bt = 1 + sum(b[k]*t**k for k in range(1, N))
S = sp.Integer(0)
for d in range(1, N):
    mu = sp.mobius(d)
    if mu == 0: continue
    Bd = 1 + sum(b[k]*t**(d*k) for k in range(1, N//d + 1) if d*k < N)
    S += sp.Rational(mu, d) * sp.series(sp.log(Bd), t, 0, N).removeO()
S = sp.expand(S)
p = [sp.Integer(0)] + [sp.nsimplify(S.coeff(t, k)) for k in range(1, N)]
print("p_k =", [int(v) for v in p[1:13]])
print("p_k all integers:", all(v.is_Integer for v in p[1:13]))

# ---- PBW check: B(t) = prod (1-t^k)^{-p_k} mod t^13 ---------------------
P = sp.Integer(1)
for k in range(1, 13):
    P = sp.expand(P * sp.series((1-t**k)**(-int(p[k])), t, 0, 13).removeO())
    P = sum(sp.expand(P).coeff(t, j)*t**j for j in range(0, 13))
diff = sp.expand(P - sum(b[k]*t**k for k in range(0, 13)) - 1 + 1)
diff = sp.expand(P - (1 + sum(b[k]*t**k for k in range(1, 13))))
print("PBW residual mod t^13:", sp.simplify(diff))

# ---- Rick's stated data, compared ---------------------------------------
rick_b = [3,27,417,7851,164124,3661389,85384566,2056373739,50751637140,1276862920140,32626363346505,844375375808301]
rick_a = [3,18,282,5268,109647,2438928,56758176,1364824620,33643660620,845633502606,21590775239850,558411335278644]
rick_p = [3,21,344,6447,134571,2995655,69761697,1678307754,41386815905,1040573158494,26574621911472,687454232433863]
print("b matches Rick:", [int(v) for v in b[1:13]] == rick_b)
print("a matches Rick:", [int(v) for v in a[1:13]] == rick_a)
print("p matches Rick:", [int(v) for v in p[1:13]] == rick_p)
for nm, mine, his in [("b",b,rick_b),("a",a,rick_a),("p",p,rick_p)]:
    for k in range(1,13):
        if int(mine[k]) != his[k-1]:
            print("  MISMATCH %s_%d: mine=%d rick=%d" % (nm,k,int(mine[k]),his[k-1]))
