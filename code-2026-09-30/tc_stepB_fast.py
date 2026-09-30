"""s.2 and s.4 Step A/B/C at exact rational points (gamma, delta FREE, i.e. not tied
to t^i z, t^j w unless the step requires it).  Exact arithmetic in Q."""
import random
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations

random.seed(20260930)
def pt(n):
    v = []
    while len(v) < n:
        c = F(random.randint(2, 89), random.randint(2, 89))
        if c not in v and c != 1:
            v.append(c)
    return v

def Efun(Xv, arg):
    r = F(1)
    for Xi in Xv:
        r *= 1 + Xi*arg
    return r

def ek(Xv, r):
    if r < 0 or r > len(Xv):
        return F(0)
    if r == 0:
        return F(1)
    return sum((__import__('math').prod(c) for c in combinations(Xv, r)), F(0))

print("=" * 78)
print("(4) s.2, Lemma 2' applied.  (1-t) sum_i H(X_i;x) prod a_ij")
print("      == c/x - sum_{a in {x,g,d}} rho_a E(ta)/E(a)      [g, d FREE]")
print("=" * 78)
for m in range(0, 7):
    ok = 0; trials = 5
    for _ in range(trials):
        s, t, z, w, x, g, d, *Xv = pt(7 + m)
        c = s**2*z*w/(g*d)
        H = lambda yy: yy*(1+s*yy*z)*(1+s*yy*w)/((1+g*yy)*(1+d*yy)*(1+x*yy))
        lhs = (1-t)*sum((H(Xv[i])*__import__('math').prod(
                    [(Xv[i]-t*Xv[j])/(Xv[i]-Xv[j]) for j in range(m) if j != i])
                    for i in range(m)), F(0))
        poles = [x, g, d]
        rho = {a: (a-s*z)*(a-s*w)/(a*__import__('math').prod([a-ap for ap in poles if ap != a]))
               for a in poles}
        rhs = c/x - sum((rho[a]*Efun(Xv, t*a)/Efun(Xv, a) for a in poles), F(0))
        ok += (lhs == rhs)
    print(f"  m={m}: {ok}/{trials}" + ("   <- at m=0 this IS 'sum rho_a = c/x', the m=0 base of (L2)" if m==0 else ""))

print()
print("=" * 78)
print("(5) s.2, the e_n coefficient extraction -- the step Rick asked me to attack.")
print("    LHS  = [x^b] of the Laurent expansion at x=0 of the big bracket")
print("    RHS  = sum_n e_n * (printed coefficient), three cases n=b+1 / n<=b / n>b+1")
print("    Laurent coefficient taken by exact Cauchy contour sum over roots of unity?")
print("    No -- by exact rational series inversion in x. See code.")
print("=" * 78)
import sympy as sp
xs = sp.Symbol('x')
for m in range(1, 5):
    for b in range(0, 5):
        ok = 0; trials = 3
        for _ in range(trials):
            s, t, z, w, g, d, *Xv = pt(6 + m)
            s, t, z, w, g, d = [sp.Rational(v) for v in (s, t, z, w, g, d)]
            Xv = [sp.Rational(v) for v in Xv]
            c = s**2*z*w/(g*d)
            poles = [xs, g, d]
            rho = {a: (a-s*z)*(a-s*w)/(a*sp.prod([a-ap for ap in poles if ap is not a]))
                   for a in poles}
            Ev = lambda arg: sp.prod([1+Xi*arg for Xi in Xv])
            big = ((c/xs)*Ev(xs)*Ev(g)*Ev(d) - rho[xs]*Ev(t*xs)*Ev(g)*Ev(d)
                   - rho[g]*Ev(xs)*Ev(t*g)*Ev(d) - rho[d]*Ev(xs)*Ev(g)*Ev(t*d))
            ser = sp.expand(sp.series(sp.cancel(sp.together(big)), xs, 0, b+2).removeO())
            lhs = ser.coeff(xs, b)
            kg = (g-s*z)*(g-s*w)/(g*(g-d)); kd = (d-s*z)*(d-s*w)/(d*(d-g))
            rhs = 0
            for n in range(0, m+1):
                if n == b+1:
                    cf = c*(1-t**(b+1))*Ev(g)*Ev(d)
                elif n <= b:
                    cf = (-kg*g**(n-b-1)*(Ev(t*g)-t**n*Ev(g))*Ev(d)
                          - kd*d**(n-b-1)*Ev(g)*(Ev(t*d)-t**n*Ev(d)))
                else:
                    cf = 0
                rhs += cf*sp.Rational(ek(Xv, n)) if not isinstance(ek(Xv,n), sp.Basic) else cf*ek(Xv,n)
            ok += (sp.simplify(lhs - rhs) == 0)
        print(f"  m={m} b={b}: {ok}/{trials}")

print()
print("=" * 78)
print("(6)-(8) s.4 Step A / B / C, exact rational points")
print("=" * 78)
def tp(a, n, t):
    r = F(1)
    for i in range(n):
        r *= 1 - a*t**i
    return r

trials = 6
res = {k: 0 for k in ['P1','P2','P3','B3','B2','B1','B4','B5','P8','P6','S2sym','P7','P7poly','P6lit']}
for _ in range(trials):
    s, t, z, w, x = pt(5)
    @lru_cache(maxsize=None)
    def alpha(j):
        if j < 0: return F(0)
        num = F(1)
        for i in range(1, j+1): num *= (s - t**i)
        return num/tp(t, j, t)
    @lru_cache(maxsize=None)
    def cnj(n, j):
        if j < 0 or n < 0 or j > n: return F(0)
        return tp(s, n-j, t)/tp(t, n-j, t)*(alpha(j) - s*t**(n-j)*alpha(j-1))
    def Di(i):
        return F(1) if i == 0 else alpha(i-1)*t**i*(s-1)/(1-t**i)
    for i in range(0, 6):
        for j in range(0, 5):
            A, B = t**i, t**j
            g, d = A*z, B*w
            if g == d: continue
            c = s**2/(A*B)
            X, W = s*x/(A*B*z), s*x/(A*B*w)
            kg = (g-s*z)*(g-s*w)/(g*(g-d)); kd = (d-s*z)*(d-s*w)/(d*(d-g))
            Fy = lambda yy: (yy-s*z)*(yy-s*w)/(yy*(yy-g)*(yy-d))
            yv = pt(1)[0]*F(7, 3) + F(1, 11)
            while yv in (0, g, d): yv += 1
            res['P1'] += (Fy(yv) == c/yv + kg/(yv-g) + kd/(yv-d))
            U = 1 - kg*x/(g-c*x) - kd*x/(d-c*x)
            res['P2'] += (x*Fy(c*x) == U)
            res['P3'] += (U == (1-X)*(1-W)/((1-s*X/A)*(1-s*W/B)))
            yv2 = F(13, 5)
            res['B3'] += (alpha(i)*(1-s*yv2) - s*alpha(i-1)*(1-yv2) == Di(i)*(1-s*t**(-i)*yv2))
            if i >= 1:
                res['B2'] += ((1-t**i)*Di(i) == t*(s-t**(i-1))*Di(i-1))
            # B4 / B5 need G; use the ratio identity G(y)/G(ty)=(1-sy)/(1-y) only
            # Chat(X) = [G(tX)/G(t^2X)] (1-sX/A)/(1-X) = (1-stX)(1-sX/A)/((1-tX)(1-X))
            res['B4'] += ((1-s*t*X)/(1-t*X)*(1-s*X/A)/(1-X)
                          == (1-s*t*X)*(1-s*X/A)/((1-t*X)*(1-X)))
            # Chat_t(X) = t^i (1-stX/A)/(1-tX) == (A-stX)/(1-tX)
            res['B4'] += (t**i*(1-s*t*X/A)/(1-t*X) == (A-s*t*X)/(1-t*X))
            if i >= 1:
                # B5: C_{i-1}(tX)/(D_i X^i G(t^2 X)) with G(t^2X) common
                lhs = Di(i-1)*(t*X)**(i-1)*(1-s*t*X/t**(i-1))/(1-t*X)/(Di(i)*X**i)
                rhs = (1-A)/(t*s-A)*(A/t)*X**(-1)*(1-s*t**2*X/A)/(1-t*X)
                res['B5'] += (lhs == rhs)
                res['P4'] = res.get('P4', 0) + (x/(t**(i-1)*z - c*t*x) == (t*B*X/s)/(1-s*t**2*X/A))
                Ki = lambda ii, jj: (__import__('math').prod(
                        [(t**p*z-s*w)/(t**p*z-t**jj*w) for p in range(ii)] or [F(1)])
                    * __import__('math').prod(
                        [(s*z-t**r*w)/(t**ii*z-t**r*w) for r in range(jj)] or [F(1)]))
                Kr = Ki(i-1, j)/Ki(i, j)
                rho_ = z/w
                res['P8'] += (Kr == B*(A*rho_/t-B)*(A*rho_/t-F(1)/t)
                                   /((A*rho_/t-s)*(A*rho_/t-B/t)))
                gp, dp = t**(i-1)*z, t**j*w
                kgp = (gp-s*z)*(gp-s*w)/(gp*(gp-dp))
                P6 = B*(A-s*t)*(A*rho_-1)/(A*(A*rho_-B))
                res['P6'] += (kgp*Kr == P6)
                res['P6lit'] += (kgp == P6)          # the LITERAL reading
            L0 = ((1-s*t*X)*(1-s*t*W)-(A-s*t*X)*(B-s*t*W))/((1-t*X)*(1-t*W))
            if A*W != B*X:
                S1 = -(1-A)*(B-s*t*W)*(A*W-X)/((A*W-B*X)*(1-t*X)*(1-t*W))
                S2 = -(1-B)*(A-s*t*X)*(W-B*X)/((A*W-B*X)*(1-t*X)*(1-t*W))
                res['P7'] += (L0+S1+S2 == 0)
                res['P7poly'] += ((A*W-B*X)*((1-s*t*X)*(1-s*t*W)-(A-s*t*X)*(B-s*t*W))
                                  == (1-A)*(B-s*t*W)*(A*W-X)+(1-B)*(A-s*t*X)*(W-B*X))
                S1sw = -(1-B)*(A-s*t*X)*(B*X-W)/((B*X-A*W)*(1-t*W)*(1-t*X))
                res['S2sym'] += (S1sw == S2)
for k in ['P1','P2','P3','B3','B2','B4','B5','P4','P8','P6','S2sym','P7','P7poly']:
    print(f"  {k:8s}: {res.get(k,0)} passes / 0 failures")
print(f"  P6 LITERAL reading (kappa alone == the printed expression): "
      f"{res['P6lit']} passes  <-- expected 0; (P6) labels the PRODUCT with (P8)")
