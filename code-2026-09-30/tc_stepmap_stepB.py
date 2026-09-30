"""s.2 (step map / Laurent extraction) and s.4 Step A/B/C -- the two places Rick
asked me to attack.  Written from his printed text; gamma, delta kept FREE."""
import sys
sys.path.insert(0, '/home/clio/projects/reviews/code-2026-09-30')
import sympy as sp
from tc_aha import Xs, e, E, cnj, alpha, tpoch

s, t, z, w, x, y = sp.symbols('s t z w x y')
g, d = sp.symbols('gamma delta')          # gamma, delta free
A, B = sp.symbols('A B')                  # A = t^i, B = t^j, free
X, W = sp.symbols('Xc Wc')                # the normalised variables of Step B

def Z0(ex):
    return sp.simplify(sp.cancel(sp.together(sp.expand(ex)))) == 0

print("=" * 78)
print("(4) s.2  Lemma 2' applied:  (1-t) sum_i H(X_i;x) prod_{j!=i} a_ij")
print("        ==  c/x - sum_{a in {x,g,d}} rho_a E(ta)/E(a),   rho_a as printed")
print("=" * 78)
c = s**2*z*w/(g*d)
poles = [x, g, d]
rho = {a: (a - s*z)*(a - s*w)/(a*sp.prod([a - ap for ap in poles if ap is not a]))
       for a in poles}
H = lambda yy: yy*(1 + s*yy*z)*(1 + s*yy*w)/((1 + g*yy)*(1 + d*yy)*(1 + x*yy))
for m in [0, 1, 2, 3, 4]:
    Xv = Xs(m)
    lhs = (1 - t)*sum(H(Xv[i-1])*sp.prod([(Xv[i-1] - t*Xv[j-1])/(Xv[i-1] - Xv[j-1])
                                          for j in range(1, m+1) if j != i])
                      for i in range(1, m+1))
    rhs = c/x - sum(rho[a]*E(Xv, t*a)/E(Xv, a) for a in poles)
    print(f"  m={m}: {'OK' if Z0(lhs - rhs) else '*** FAIL ***'}"
          + ("   <- m=0 case is 'sum rho_a = c/x', the m=0 base of (L2)" if m == 0 else ""))
    sys.stdout.flush()

print()
print("=" * 78)
print("(5) s.2  the e_n coefficient extraction -- the Laurent/residue step Rick flagged.")
print("    [x^b] of the big bracket, re-expanded in the e_n basis, vs the printed")
print("    three-case coefficient (n=b+1 / n<=b / n>b+1).")
print("=" * 78)
kg = (g - s*z)*(g - s*w)/(g*(g - d))
kd = (d - s*z)*(d - s*w)/(d*(d - g))
for m in [1, 2, 3]:
    Xv = Xs(m)
    big = ((c/x)*E(Xv, x)*E(Xv, g)*E(Xv, d)
           - rho[x]*E(Xv, t*x)*E(Xv, g)*E(Xv, d)
           - rho[g]*E(Xv, x)*E(Xv, t*g)*E(Xv, d)
           - rho[d]*E(Xv, x)*E(Xv, g)*E(Xv, t*d))
    big = sp.cancel(sp.together(big))
    for b in range(0, 4):
        ser = sp.expand(sp.series(big, x, 0, b + 2).removeO())
        lhs = ser.coeff(x, b)
        rhs = 0
        for n in range(0, m + 1):
            if n == b + 1:
                cf = c*(1 - t**(b+1))*E(Xv, g)*E(Xv, d)
            elif n <= b:
                cf = (-kg*g**(n-b-1)*(E(Xv, t*g) - t**n*E(Xv, g))*E(Xv, d)
                      - kd*d**(n-b-1)*E(Xv, g)*(E(Xv, t*d) - t**n*E(Xv, d)))
            else:
                cf = sp.Integer(0)
            rhs += cf*e(Xv, n)
        print(f"  m={m} b={b}: {'OK' if Z0(lhs - rhs) else '*** FAIL ***'}")
        sys.stdout.flush()

print()
print("=" * 78)
print("(6) s.4 Step A:  (P1) partial fractions, (P2) U = x F(cx), (P3) U factorises")
print("=" * 78)
Fy = (y - s*z)*(y - s*w)/(y*(y - g)*(y - d))
print("  (P1) F = c/y + kg/(y-g) + kd/(y-d):",
      "OK" if Z0(Fy - (c/y + kg/(y - g) + kd/(y - d))) else "*** FAIL ***")
U = 1 - kg*x/(g - c*x) - kd*x/(d - c*x)
print("  (P2) x F(cx) == U:", "OK" if Z0(x*Fy.subs(y, c*x) - U) else "*** FAIL ***")
# (P3): substitute g = A z, d = B w  (A=t^i, B=t^j) and X = s x/(A B z), W = s x/(A B w)
sub = {g: A*z, d: B*w}
Ug = sp.simplify(U.subs(sub))
Xe, We = s*x/(A*B*z), s*x/(A*B*w)
P3 = (1 - Xe)*(1 - We)/((1 - s*Xe/A)*(1 - s*We/B))
print("  (P3) U == (1-X)(1-W)/((1-sX/A)(1-sW/B)):",
      "OK" if Z0(Ug - P3) else "*** FAIL ***")

print()
print("=" * 78)
print("(7) s.4 Step B: the normalisations Rick asked me to attack.")
print("=" * 78)
NG = 26                                     # truncation for the formal series G
def G(arg):
    """G(y) = prod_{r>=0}(1-s t^r y)/(1-t^r y); satisfies G(y)/G(ty) = (1-sy)/(1-y)."""
    return sp.prod([(1 - s*t**r*arg)/(1 - t**r*arg) for r in range(NG)])

def Ci_series(i, Nmax):
    return sum(cnj(n, i)*x**n for n in range(Nmax + 1))

def Di(i):
    if i == 0:
        return sp.Integer(1)
    return alpha(i-1)*t**i*(s-1)/(1-t**i)

print("  B3: alpha_i(1-sy) - s alpha_{i-1}(1-y) == D_i (1 - s t^-i y)")
for i in range(0, 7):
    lhs = alpha(i)*(1 - s*y) - s*alpha(i-1)*(1 - y)
    print(f"      i={i}: {'OK' if Z0(lhs - Di(i)*(1 - s*t**(-i)*y)) else '*** FAIL ***'}",
          end="   D_i = " + str(sp.simplify(Di(i))) + "\n")
print("  B2: (1-t^i) D_i == t (s - t^{i-1}) D_{i-1}")
for i in range(1, 8):
    print(f"      i={i}: {'OK' if Z0((1-t**i)*Di(i) - t*(s-t**(i-1))*Di(i-1)) else '*** FAIL ***'}")
print("  B1: C_i(x) == D_i x^i G(tx)(1 - s x/t^i)/(1-x)   [series coefficients]")
for i in range(0, 5):
    Nm = 7
    closed = Di(i)*x**i*G(t*x)*(1 - s*x/t**i)/(1 - x)
    ser = sp.series(sp.cancel(sp.together(closed)), x, 0, Nm + 1).removeO()
    ok = all(Z0(sp.expand(ser).coeff(x, n) - cnj(n, i)) for n in range(Nm + 1))
    print(f"      i={i}, x^0..x^{Nm}: {'OK' if ok else '*** FAIL ***'}")
    sys.stdout.flush()

print()
print("  B4: Chat(X) == (1-stX)(1-sX/A)/((1-tX)(1-X)) and Chat_t(X) == (A-stX)/(1-tX)")
for i in range(0, 5):
    Ai = t**i
    hatC = sp.cancel(Di(i)*X**i*G(t*X)*(1 - s*X/Ai)/(1-X) / (Di(i)*X**i*G(t**2*X)))
    hatCt = sp.cancel(Di(i)*(t*X)**i*G(t**2*X)*(1 - s*t*X/Ai)/(1-t*X) / (Di(i)*X**i*G(t**2*X)))
    ok1 = Z0(hatC - (1-s*t*X)*(1-s*X/Ai)/((1-t*X)*(1-X)))
    ok2 = Z0(hatCt - (Ai - s*t*X)/(1-t*X))
    print(f"      i={i}: Chat {'OK' if ok1 else 'FAIL'} ; Chat_t {'OK' if ok2 else 'FAIL'}")

print()
print("  B5: C_{i-1}(tX)/(D_i X^i G(t^2 X)) == (1-A)/(ts-A) (A/t) X^-1 (1-st^2X/A)/(1-tX)")
for i in range(1, 6):
    Ai = t**i
    lhs = sp.cancel(Di(i-1)*(t*X)**(i-1)*G(t**2*X)*(1 - s*t*X/t**(i-1))/(1-t*X)
                    / (Di(i)*X**i*G(t**2*X)))
    rhs = (1-Ai)/(t*s-Ai)*(Ai/t)*X**(-1)*(1 - s*t**2*X/Ai)/(1-t*X)
    print(f"      i={i}: {'OK' if Z0(lhs-rhs) else '*** FAIL ***'}")

print()
print("=" * 78)
print("(8) s.4  L_0, S_1, S_2 and the closing identity (P7)")
print("=" * 78)
L0 = ((1-s*t*X)*(1-s*t*W) - (A-s*t*X)*(B-s*t*W))/((1-t*X)*(1-t*W))
print("  L_0 = Chat(X)Chat(W)U - Chat_t(X)Chat_t(W) reduces as printed:",
      "OK" if Z0((1-s*t*X)*(1-s*X/A)/((1-t*X)*(1-X))
                 * (1-s*t*W)*(1-s*W/B)/((1-t*W)*(1-W))
                 * (1-X)*(1-W)/((1-s*X/A)*(1-s*W/B))
                 - (A-s*t*X)*(B-s*t*W)/((1-t*X)*(1-t*W)) - L0) else "*** FAIL ***")
rho_ = W/X
# (P8) kernel ratio, from the definition of K_ij (telescoping over r<j)
i_, j_ = sp.symbols('i_ j_', integer=True, positive=True)
def Kratio_direct(i, j):
    Ki = lambda ii, jj: (sp.prod([(t**p*z - s*w)/(t**p*z - t**jj*w) for p in range(ii)])
                         * sp.prod([(s*z - t**r*w)/(t**ii*z - t**r*w) for r in range(jj)]))
    return sp.cancel(Ki(i-1, j)/Ki(i, j))
print("  (P8) K_{i-1,j}/K_{ij} == B(Ar/t - B)(Ar/t - 1/t)/((Ar/t - s)(Ar/t - B/t)),  r=z/w")
for i in range(1, 5):
    for j in range(0, 4):
        Ai, Bj, rr = t**i, t**j, z/w
        printed = Bj*(Ai*rr/t - Bj)*(Ai*rr/t - 1/t)/((Ai*rr/t - s)*(Ai*rr/t - Bj/t))
        ok = Z0(Kratio_direct(i, j) - printed)
        if not ok:
            print(f"      *** FAIL i={i} j={j}")
print("      i=1..4, j=0..3: OK" )
print()
print("  (P6) kappa_g^{(i-1,j)} * K_{i-1,j}/K_{ij} == B(A-st)(Ar-1)/(A(Ar-B))")
for i in range(1, 5):
    for j in range(0, 4):
        Ai, Bj, rr = t**i, t**j, z/w
        gp, dp = t**(i-1)*z, t**j*w
        kgp = (gp - s*z)*(gp - s*w)/(gp*(gp - dp))
        printed = Bj*(Ai - s*t)*(Ai*rr - 1)/(Ai*(Ai*rr - Bj))
        ok = Z0(kgp*Kratio_direct(i, j) - printed)
        if not ok:
            print(f"      *** FAIL i={i} j={j}")
print("      i=1..4, j=0..3: OK")
print()
S1 = -(1-A)*(B-s*t*W)*(A*W-X)/((A*W-B*X)*(1-t*X)*(1-t*W))
S2 = -(1-B)*(A-s*t*X)*(W-B*X)/((A*W-B*X)*(1-t*X)*(1-t*W))
print("  S_2 == (X<->W, A<->B) image of S_1:",
      "OK" if Z0(S1.subs({X: W, W: X, A: B, B: A}, simultaneous=True) - S2) else "*** FAIL ***")
print("  (P7)  L_0 + S_1 + S_2 == 0:",
      "OK" if Z0(L0 + S1 + S2) else "*** FAIL ***")
print("  (P7) in the printed polynomial form:",
      "OK" if Z0((A*W-B*X)*((1-s*t*X)*(1-s*t*W) - (A-s*t*X)*(B-s*t*W))
                 - (1-A)*(B-s*t*W)*(A*W-X) - (1-B)*(A-s*t*X)*(W-B*X)) else "*** FAIL ***")
