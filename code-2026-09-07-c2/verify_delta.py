"""Clio 2026-09-07 c2 — verification half.  Fast truncated-series arithmetic."""
import sympy as sp
from enum_delta_diagonal import (CELLS, enumerate_delta, Hf, Kf, Lf, Mf, T, s, p)

N = 12
SV, PV = sp.Rational(2), sp.Rational(3)

def trunc(e):
    e = sp.expand(e)
    return sp.expand(sum(e.coeff(T, k)*T**k for k in range(N+1)))

Ys = [sp.S(0)]*(N+3)
for n in range(1, N+3):
    acc = sp.S(1) if n == 1 else sp.S(0)
    acc += SV*Ys[n-1] + sum(PV*Ys[k]*Ys[n-1-k] for k in range(n))
    Ys[n] = acc
Yp = trunc(sum(Ys[n]*T**n for n in range(N+3)))

def inv(f):
    c = [f.coeff(T, k) for k in range(N+1)]
    g = [sp.S(0)]*(N+1); g[0] = 1/c[0]
    for n in range(1, N+1):
        g[n] = -sum(c[k]*g[n-k] for k in range(1, n+1))/c[0]
    return sum(g[k]*T**k for k in range(N+1))

qp = trunc(1 - SV*T - 2*PV*T*Yp)
Hp = trunc(sum(PV*Ys[m+1]*T**m for m in range(N+1)))
Kp = trunc(-PV*Yp*inv(trunc(qp**2)))

L_tab = [0, 0, -10*p, -49*s*p, -145*s**2*p - 95*p**2, -335*s**3*p - 658*s*p**2,
         -665*s**4*p - 2611*s**2*p**2 - 644*p**3,
         -1190*s**5*p - 7784*s**3*p**2 - 5758*s*p**3,
         -1974*s**6*p - 19362*s**4*p**2 - 28638*s**2*p**3 - 3777*p**4,
         -3090*s**7*p - 42420*s**5*p**2 - 104550*s**3*p**3 - 41360*s*p**4,
         -4620*s**8*p-84546*s**6*p**2-312510*s**4*p**3-247225*s**2*p**4-20416*p**5]
Lp = trunc(sum(sp.expand(L_tab[m]).subs({s: SV, p: PV})*T**m for m in range(len(L_tab))))

def dd(f):
    return trunc(sum((k+1)*f.coeff(T, k+1)*T**k for k in range(N+1)))

SER = {Hf: Hp, Kf: Kp, Lf: Lp, Mf: sp.S(0)}

def evaluate(expr, upto=10):
    e = sp.expand(sp.expand(expr).subs({s: SV, p: PV}))
    for f in (Hf, Kf, Lf, Mf):
        for order in (3, 2, 1):
            d = SER[f]
            for _ in range(order):
                d = dd(d)
            e = e.subs(sp.Derivative(f, (T, order)), d)
        e = e.subs(f, SER[f])
    e = sp.expand(e)
    return [e.coeff(T, k) for k in range(upto+1)]

print("#"*74)
print("# CALIBRATION -- same enumerator at delta=0 and delta=1 (known results)")
print("#"*74)
for delta in (0, 1):
    hits, total = enumerate_delta(delta)
    cf = evaluate(total, 8)
    print(f"delta={delta}: {len(hits)} tuples, max e={max(h['e'] for h in hits)}, "
          f"identically zero on closed-form H,K: {all(c == 0 for c in cf)}")

print("\n" + "#"*74)
print("# delta = 2")
print("#"*74)
hits, total = enumerate_delta(2)
Lop = sp.expand(sp.diff(sp.expand(total), Lf))
src = sp.expand(total - Lop*Lf)
print(f"tuples: {len(hits)}   max layer e: {max(h['e'] for h in hits)}"
      "   (>2 would mean the equation does not close on H,K,L)")
print(f"L'  present in the delta=2 equation ? {sp.expand(total).has(sp.Derivative(Lf, T))}")
print(f"L'' present in the delta=2 equation ? {sp.expand(total).has(sp.Derivative(Lf,(T,2)))}")
print(f"K'' present in the delta=2 equation ? {sp.expand(total).has(sp.Derivative(Kf,(T,2)))}")
print(f"SOURCE free of L ? {not src.has(Lf)}")
print("\nmy L-operator  =", sp.factor(Lop))

cf = evaluate(total, 10)
print("\nL-op*L + SOURCE  on tabulated L_{-1}, coeffs [T^0..T^10]:")
print("   ", cf, "\n    ALL ZERO:", all(c == 0 for c in cf))

# ---- group my 37 tuples into (parent, X, e) items and match Rick's (a)-(m)
print("\n" + "#"*74)
print("# GROUPING: my tuples -> items, vs Rick's list (a)-(m)")
print("#"*74)
groups = {}
for h in hits:
    groups.setdefault((h['i'], h['X'], h['e']), []).append(h)
per_parent = {1: 0, 2: 0, 3: 0}
for (i, X, e), hs in sorted(groups.items(), key=lambda kv: (-kv[0][0], kv[0][1], kv[0][2])):
    pref = sp.expand(sum(h['coef']*T**h['d'] for h in hs))
    pureL = (X == 'G' and e == 2)
    per_parent[i] += 0 if pureL else 1
    tag = "L-op only" if pureL else ("non-L item + L-op part" if e == 2 and X in ('G^3','G^2')
                                     else "non-L item")
    print(f"  P_{i} * {X:4s} e={e}  prefactor = {sp.factor(pref)}   [{tag}]")
print(f"\n  non-L items per parent:  P_3={per_parent[3]}  P_2={per_parent[2]}  P_1={per_parent[1]}"
      f"   total={sum(per_parent.values())}")
print("  Rick's PDF says: P_3 '(7 slots)', P_2 '(4 slots)', P_1 '(2 slots)', 13 terms")

# ---- what the PDF's PRINTED support table alone yields
print("\n" + "#"*74)
print("# RE-RUN using ONLY the (w,d) supports as PRINTED in the PDF")
print("#"*74)
printed = {3: {(0,2),(0,3),(0,4),(1,3),(2,4)},
           2: {(0,0),(1,1),(2,2),(2,3),(3,3)},
           1: {(0,0),(1,1),(2,0),(2,2),(3,1),(4,2)}}
for i in (3, 2, 1):
    missing = sorted(set(CELLS[i]) - printed[i])
    contrib = sorted(c for c in missing
                     if any(c in {(h['w'],h['d']) for h in hits if h['i']==i} for _ in [0]))
    print(f"  P_{i}: printed {len(printed[i])} cells, actual {len(CELLS[i])}; "
          f"omitted = {missing}")
restricted = {i: {k: v for k, v in CELLS[i].items() if k in printed[i]} for i in (1,2,3)}
hits_p, _ = enumerate_delta(2, cell_table=restricted)
gp = {}
for h in hits_p:
    gp.setdefault((h['i'], h['X'], h['e']), []).append(h)
print("\n  items recoverable from the printed table alone:")
for key in sorted(groups, key=lambda k: (-k[0], k[1], k[2])):
    full = sp.expand(sum(h['coef']*T**h['d'] for h in groups[key]))
    got  = sp.expand(sum(h['coef']*T**h['d'] for h in gp.get(key, [])))
    status = "FULL" if got == full else ("MISSING ENTIRELY" if got == 0 else "PARTIAL")
    print(f"    P_{key[0]} * {key[1]:4s} e={key[2]}:  {status:16s} "
          f"printed-gives={sp.factor(got)}  true={sp.factor(full)}")
