"""Verify Rick's structural explanation of the 4 misses in the 213/217 control
(UID 804 (b)).  Claim: for 'pure' c = A(t) s^{n(mu)} (s-1)^v with v = l(lambda)-kappa,
writing eps = s-1 we have [eps^{v+1}]c / [eps^v]c = n(mu); so a control that shifts the
(s-1)-valuation by 1 (kappa=1: |C|-1 -> |C| in the single block) is blind iff n(mu)=1."""
import sympy as sp
s, eps, t = sp.symbols('s epsilon t', positive=True)

def n_mu(mu):   # n(mu) = sum (i-1) mu_i
    return sum(i*m for i, m in enumerate(mu))
def br(k):      # [k]_t
    return sum(t**j for j in range(k))

print("=== general algebra: [eps^(v+1)]c / [eps^v]c  ==  n(mu)? ===")
for nm in range(0, 4):
    for v in range(0, 3):
        A = sp.Symbol('A')
        c = A*(1+eps)**nm*eps**v
        p = sp.Poly(sp.expand(c), eps)
        cv, cv1 = p.coeff_monomial(eps**v), p.coeff_monomial(eps**(v+1))
        ratio = sp.simplify(cv1/cv) if cv != 0 else None
        print(f"  n(mu)={nm} v={v}: [e^v]={cv}, [e^(v+1)]={cv1}, ratio={ratio}, "
              f"blind={'YES' if ratio==1 else 'no'}")

print("\n=== the four printed misses: lambda,mu, exact c, n(mu), v, blindness ===")
cases = [((2,2),(3,1),2), ((3,2),(4,1),3), ((4,2),(5,1),4), ((5,2),(6,1),5)]
for lam, mu, k in cases:
    c = -br(k)*s*(s-1)                      # Rick's printed exact c_{lambda mu}(s,t)
    v = len(lam) - 1                        # l(lambda) - kappa, kappa=1
    nm = n_mu(mu)
    ce = sp.expand(c.subs(s, 1+eps))
    p = sp.Poly(ce, eps)
    cv, cv1 = p.coeff_monomial(eps**v), p.coeff_monomial(eps**(v+1))
    print(f"  lam={lam} mu={mu}: c={sp.factor(c)}  n(mu)={nm}  v={v}  "
          f"[e^{v}]={sp.factor(cv)}  [e^{v+1}]={sp.factor(cv1)}  "
          f"EQUAL={'YES (control blind)' if sp.simplify(cv-cv1)==0 else 'no'}")

print("\n=== CONTRAST cases Rick names (control must FIRE) ===")
contrast = [((2,1),(3,),'pure n(mu)=0'), ((3,3),(4,2),'pure n(mu)=2'), ((4,3),(5,2),'pure n(mu)=2')]
for lam, mu, tag in contrast:
    nm = n_mu(mu); v = len(lam) - 1
    A = sp.Symbol('A')
    c = A*(1+eps)**nm*eps**v
    p = sp.Poly(sp.expand(c), eps)
    cv, cv1 = p.coeff_monomial(eps**v), p.coeff_monomial(eps**(v+1))
    print(f"  lam={lam} mu={mu} ({tag}): n(mu)={nm} ratio={sp.simplify(cv1/cv)} "
          f"-> {'FIRES' if sp.simplify(cv1-cv)!=0 else 'BLIND'}")

print("\n=== next member (6,2)->(7,1): is it outside |lambda|<=7? ===")
print(f"  |lambda|=|(6,2)|={6+2}, n(mu)={n_mu((7,1))}, v=1 -> would be a 5th miss; "
      f"excluded only by the |lambda|<=7 grid bound: {6+2>7}")
