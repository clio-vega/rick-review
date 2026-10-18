"""Rick's §6 labelled HUNCHES -- does a lemma he already has force them?
(The 10-17 precedent: his self-labelled Koncki hunch was a corollary of his own Lemma QC.)"""
import sympy as sp
q, v, k = sp.symbols('q v'), None, None
q, v = sp.symbols('q v')
psi = lambda V, Q: (1 - Q*V**2)/(1 - Q)
h1 = sp.simplify(psi(v, 1/q) - v**2*psi(1/v, q))
print("H1  psi(v;1/q) = v^2 psi(1/v;q)          difference:", h1, " =>", "IDENTITY" if h1==0 else "FALSE")
h2 = sp.limit(psi(v, q), q, sp.oo)
print("H2  psi -> v^2 as q -> oo                limit   :", sp.simplify(h2), " =>", "IDENTITY" if sp.simplify(h2-v**2)==0 else "FALSE")
chi = v**2
h3a = sp.simplify(chi.subs(v,v)*chi.subs(v,1/v) - 1)
h3b = sp.simplify(chi.subs(v,1)-1), sp.simplify(chi.subs(v,-1)-1)
print("H3  chi=v^2 admissible: chi(x)chi(1/x)-1 =", h3a, "  chi(+-1)-1 =", h3b,
      " =>", "ADMISSIBLE" if h3a==0 and h3b==(0,0) else "NOT")
# controls: the same three tests must REJECT a near-miss gauge
bad = lambda V,Q: (1 - Q*V**3)/(1 - Q)
print("control (psi -> (1-qv^3)/(1-q)):  H1 difference:",
      sp.simplify(bad(v,1/q) - v**2*bad(1/v,q)), "(must be nonzero)")
print("control (chi = v^3):              chi(x)chi(1/x)-1 =", sp.simplify(v**3*v**-3-1),
      "; chi(-1)-1 =", sp.simplify((-1)**3-1), "(must reject via chi(-1))")
