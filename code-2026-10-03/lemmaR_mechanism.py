"""
Lemma R (from Rick's (s,t)-square note, re-used in DS-from-N sec 5 to make
iota = Psi o beta an involution):   Psi_{1/s,1/t} = Psi^{-1}_{s,t}.

The brief flags this as the place a real defect would live, and asks in particular
whether the reflection holds only on a SUBSPACE (both new edges would inherit the
restriction).  I do not need the 6pp note to test the mechanism:

  Psi = N^{-1},  N P_nu = T_nu P_nu,  T_nu = t^{n(nu)} s^{n(nu')}.
  Under (s,t) -> (1/s,1/t):  T_nu -> T_nu^{-1}.
  Rick's P_nu := P_nu(x; q=s, t_Mac=1/t), so (s,t)->(1/s,1/t) is
  (q,t_Mac) -> (1/q, 1/t_Mac).

So Lemma R holds on ALL of Sym iff Macdonald P is invariant under
(q,t) -> (q^{-1},t^{-1}).  That is the single fact to check.
"""
import sympy as sp
from itertools import combinations, permutations

s, t = sp.symbols('s t')

def build(m, NMAX):
    xs = sp.symbols('x1:%d' % (m+1))
    tau = 1/t
    def parts(n):
        def go(n, k, mx):
            if n == 0: yield []; return
            if k == 0: return
            for a in range(min(n, mx), 0, -1):
                for r in go(n-a, k-1, a): yield [a]+r
        return list(go(n, m, n))
    def pad(l): return tuple(list(l)+[0]*(m-len(l)))
    def nstat(l): return sum(i*p for i, p in enumerate(l))
    def conj(l):
        l = [p for p in l if p > 0]
        return [sum(1 for p in l if p > j) for j in range(l[0])] if l else []
    def dom_leq(a, b):
        sa = sb = 0
        for i in range(max(len(a), len(b))):
            sa += a[i] if i < len(a) else 0
            sb += b[i] if i < len(b) else 0
            if sa > sb: return False
        return True
    def mono(l): return {e: sp.Integer(1) for e in set(permutations(pad(l)))}
    def apply_op(d, pairs):
        poly = sum(c*sp.prod([xs[i]**e for i, e in enumerate(ex)]) for ex, c in d.items())
        out = 0
        for coef, I, sh in pairs:
            out += coef*poly.subs({xs[i]: sh*xs[i] for i in I}, simultaneous=True)
        out = sp.cancel(sp.together(out)); num, den = sp.fraction(out)
        P = sp.Poly(sp.expand(num), *xs)
        return {tuple(e): sp.cancel(c/den) for e, c in zip(P.monoms(), P.coeffs())
                if sp.cancel(c/den) != 0}
    D1 = [(sp.prod([(tau*xs[i]-xs[j])/(xs[i]-xs[j]) for j in range(m) if j != i]), (i,), s)
          for i in range(m)]
    def eps(nu): return sp.expand(sum(s**ni*tau**(m-1-i) for i, ni in enumerate(pad(nu))))
    def mcf(d, n): return {tuple(nu): sp.cancel(d.get(pad(nu), 0)) for nu in parts(n)}
    Pm = {}
    for n in range(1, NMAX+1):
        B = [tuple(b) for b in parts(n)]
        Mat = {tuple(sig): mcf(apply_op(mono(list(sig)), D1), n) for sig in B}
        order = sorted(B, key=lambda a: sum(1 for b in B if dom_leq(list(a), list(b))))
        for nu in order:
            u = {nu: sp.Integer(1)}
            for kap in order:
                if kap == nu or not dom_leq(list(kap), list(nu)): continue
                acc = sum(Mat[sig].get(kap, 0)*uv for sig, uv in u.items() if sig != kap)
                u[kap] = sp.cancel(-acc/sp.expand(eps(list(kap))-eps(list(nu))))
            Pm[nu] = {a: sp.cancel(b) for a, b in u.items() if sp.cancel(b) != 0}
    return Pm, parts, nstat, conj

for m, NMAX in [(3, 3), (4, 4)]:
    Pm, parts, nstat, conj = build(m, NMAX)
    print("m = %d, n <= %d" % (m, NMAX))
    ok = True
    for nu, u in Pm.items():
        for mu, v in u.items():
            flipped = sp.cancel(sp.together(v.subs({s: 1/s, t: 1/t}, simultaneous=True)))
            if sp.simplify(sp.cancel(flipped - v)) != 0:
                ok = False
                print("   NOT INVARIANT  P_%s coeff of m_%s : %s  vs flipped %s"
                      % (list(nu), list(mu), sp.factor(v), sp.factor(flipped)))
    print("   P_nu(x; q,t_Mac) invariant under (q,t_Mac)->(1/q,1/t_Mac) : %s" % ok)
    # and therefore Psi_{1/s,1/t} = Psi^{-1}: check the eigenvalue statement directly
    ok2 = all(sp.simplify(sp.cancel(
        (t**nstat(list(nu))*s**nstat(conj(list(nu)))).subs({s: 1/s, t: 1/t}, simultaneous=True)
        - 1/(t**nstat(list(nu))*s**nstat(conj(list(nu)))))) == 0 for nu in Pm)
    print("   T_nu(1/s,1/t) = T_nu(s,t)^{-1} for all nu : %s" % ok2)
    print("   => Lemma R holds on ALL of Sym (not a subspace) : %s\n" % (ok and ok2))

# ---------------------------------------------------------------------------
# Consequence worth stating: because P is (q,t)->(1/q,1/t) invariant,
#   lim_{q->oo} P_lam(x;q,t) = P_lam(x;0,1/t) = Hall-Littlewood P_lam(x;1/t).
# So a q->oo (Rick's s->oo) limit is NOT a fifth degeneration of Macdonald P --
# it is the t=0 HL degeneration composed with the inversion symmetry, the SAME
# symmetry as Lemma R.  Checked directly below.
print("CONSEQUENCE: lim_{q->oo} P_lam(x;q,t) =? P_lam(x;0,1/t)  (HL at 1/t)")
for m, NMAX in [(3, 3)]:
    Pm, parts, nstat, conj = build(m, NMAX)
    ok = True
    for nu, u in Pm.items():
        for mu, v in u.items():
            # Rick's P_nu = P_nu(x; q=s, t_Mac=1/t). q->oo is s->oo.
            lim_s_inf = sp.limit(sp.cancel(v), s, sp.oo)
            # P_lam(x; q=0, t_Mac=t) : set s->0 and t_Mac=1/t -> t_Mac=t means t->1/t
            hl_at_inv = sp.cancel(sp.cancel(v).subs(s, 0))
            hl_at_inv = sp.cancel(hl_at_inv.subs(t, 1/t))
            if sp.simplify(sp.cancel(lim_s_inf - hl_at_inv)) != 0:
                ok = False
                print("   MISMATCH P_%s m_%s : s->oo gives %s ; HL(1/t) gives %s"
                      % (list(nu), list(mu), sp.factor(lim_s_inf), sp.factor(hl_at_inv)))
    print("   m=%d, n<=%d : %s" % (m, NMAX, ok))
