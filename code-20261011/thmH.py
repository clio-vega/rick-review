"""Three checks on long-version Theorem H:
 (1) the CONTENT attributed to Macdonald III (3.2): e_k P_rho(x;u) = sum psi_{kap/rho}(u) P_kap(x;u)
     with Rick's psi_{kap/rho}(u) = prod_v qbin(m_v(kap), r_v)_u  -- via engine B, independent of locator.
 (2) eq (5.ncount):  n(kap) - n(rho) = C(k,2) + inv(kap/rho) + sum_v r_v (m_v - r_v).
 (3) Theorem H(3): the explicit L_k formula, against the star-product engine A."""
from fractions import Fraction
from itertools import combinations
from ring import *
from ebasis import e_expand
import hl

def mult(lam, v): return sum(1 for p in lam if p == v)

def vstrips(kap, k):
    """all rho with kap/rho a vertical k-strip, together with r_v data."""
    out = []
    parts = list(kap)
    vals = sorted(set(parts))
    # choose r_v of the m_v parts equal to v, for each v, total k
    def rec(i, chosen, acc):
        if sum(acc.values()) > k: return
        if i == len(vals):
            if sum(acc.values()) != k: return
            rho = []
            for v in vals:
                r = acc.get(v, 0)
                rho += [v-1]*r + [v]*(mult(kap, v)-r)
            rho = tuple(sorted((p for p in rho if p > 0), reverse=True))
            out.append((rho, dict(acc)))
            return
        v = vals[i]
        for r in range(0, mult(kap, v)+1):
            a = dict(acc); a[v] = r
            rec(i+1, chosen, a)
    rec(0, None, {})
    return out

def qbin(m, r):
    """Gaussian binomial as {t_exp: Fraction}"""
    if r < 0 or r > m: return {}
    num = {0: Fraction(1)}
    def mulp(a, b):
        o = {}
        for e1, v1 in a.items():
            for e2, v2 in b.items():
                o[e1+e2] = o.get(e1+e2, Fraction(0)) + v1*v2
        return {k: v for k, v in o.items() if v}
    def divp(a, b):
        a = dict(a); o = {}
        while a:
            ae = max(a); be = max(b); e = ae-be
            c = a[ae]/b[be]; o[e] = o.get(e, Fraction(0))+c
            sub = {k+e: c*v for k, v in b.items()}
            for k, v in sub.items():
                a[k] = a.get(k, Fraction(0)) - v
            a = {k: v for k, v in a.items() if v}
        return {k: v for k, v in o.items() if v}
    def brack(n):   # [n]_t = 1+t+...+t^{n-1}
        return {i: Fraction(1) for i in range(n)}
    top = {0: Fraction(1)}; bot = {0: Fraction(1)}
    for i in range(1, r+1):
        top = mulp(top, brack(m-r+i)); bot = mulp(bot, brack(i))
    return divp(top, bot)

def psi_rick(kap, rdata):
    out = {0: Fraction(1)}
    for v, r in rdata.items():
        q = qbin(mult(kap, v), r)
        o = {}
        for e1, v1 in out.items():
            for e2, v2 in q.items():
                o[e1+e2] = o.get(e1+e2, Fraction(0)) + v1*v2
        out = {k: v for k, v in o.items() if v}
    return out

def inv_strip(kap, rdata):
    vals = sorted(set(kap))
    tot = 0
    for i, v in enumerate(vals):
        for w in vals:
            if w > v: tot += rdata.get(v, 0) * (mult(kap, w) - rdata.get(w, 0))
    return tot

# ---------- (1) content of the cited Pieri rule, via engine B ----------
print("(1) e_k P_rho(x;u) = sum_kap psi_{kap/rho}(u) P_kap(x;u)   [Rick's psi, engine-B HL polys]")
ok = bad = 0; fails = []
for n in range(1, 6):
    m = n
    Ps = {kap: hl.P_HL(kap, m) for kap in partitions(n)}
    for d in range(1, n+1):
        for rho in partitions(n-d):
            if len(rho) > m: continue
            Prho = hl.P_HL(rho, m) if rho else hl.Pone(m)
            for k in range(1, d+1):
                if k != d: continue
                # e_k * P_rho
                E = hl.Pz()
                for A in combinations(range(m), k):
                    a = [0]*m
                    for i in A: a[i] = 1
                    E[tuple(a)] = hl.ac(1)
                lhs = hl.Pmul(E, Prho)
                rhs = hl.Pz()
                for kap in partitions(n):
                    for (r2, rdata) in vstrips(kap, k):
                        if r2 != rho: continue
                        c = psi_rick(kap, rdata)
                        rhs = hl.Padd(rhs, {a: hl.amul(c, cc) for a, cc in Ps[kap].items()})
                if lhs == rhs: ok += 1
                else: bad += 1; fails.append((rho, k))
print(f"    {ok} ok, {bad} bad" + (f"  {fails[:4]}" if fails else ""))

# ---------- (2) eq (5.ncount) ----------
print("(2) n(kap)-n(rho) = C(k,2) + inv(kap/rho) + sum_v r_v(m_v-r_v)")
ok = bad = 0; fails = []
from math import comb
for n in range(1, 10):
    for kap in partitions(n):
        for k in range(1, n+1):
            for (rho, rdata) in vstrips(kap, k):
                lhs = nstat(kap) - nstat(rho)
                rhs = comb(k, 2) + inv_strip(kap, rdata) + sum(r*(mult(kap, v)-r) for v, r in rdata.items())
                if lhs == rhs: ok += 1
                else: bad += 1; fails.append((kap, rho, k, lhs, rhs))
print(f"    {ok} ok, {bad} bad" + (f"  {fails[:3]}" if fails else ""))

# ---------- (3) Theorem H(3): L_k on L/sL, against engine A ----------
print("(3) Theorem H(3): L_k bar_b_mu = sum t^inv prod qbin(m_v(kap),r_v) bar_b_nu  [engine A = star product]")
ok = bad = 0; fails = []
for n in range(1, 6):
    for k in range(1, n+1):
        d = n - k
        m = n; V = vandermonde(m)
        for mu in partitions(d):
            if len(mu) > m: continue
            emu = pone(m)
            for j in mu: 
                E = {}
                for A in combinations(range(m), j):
                    a = [0]*m
                    for i in A: a[i] = 1
                    E[tuple(a)] = cc(1)
                emu = pmul(emu, E)
            res = E_k(emu, k, m, V)
            exp = e_expand(res, n, m)
            # engine A:  L_k coefficient of bar_b_nu  =  [s^{n(nu)-n(mu)}] (coeff of e_nu)
            for nu in partitions(n):
                c = exp.get(nu, {})
                lhsA = {te: v for (se, te), v in c.items() if se == nstat(nu) - nstat(mu)}
                # printed formula: kap = nu', rho = mu'
                kap, rho_t = conj(nu), conj(mu)
                rhsF = {}
                for (r2, rdata) in vstrips(kap, k):
                    if r2 != rho_t: continue
                    iv = inv_strip(kap, rdata); ps = psi_rick(kap, rdata)
                    for e, v in ps.items():
                        rhsF[e+iv] = rhsF.get(e+iv, Fraction(0)) + v
                rhsF = {kk: v for kk, v in rhsF.items() if v}
                if lhsA == rhsF: ok += 1
                else: bad += 1; fails.append((k, mu, nu, lhsA, rhsF))
print(f"    {ok} ok, {bad} bad" + (f"  {fails[:3]}" if fails else ""))
