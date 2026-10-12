"""Check Rick's psi' claim at longversion.tex:588 by content, with HL polynomials
built from Macdonald III (2.2) -- the symmetrisation formula, read off the book page.

Claim:  e_k P_rho(x;u) = sum_kappa psi'_{kappa/rho}(u) P_kappa(x;u)  over vertical k-strips,
        psi'_{kappa/rho}(u) = prod_v qbinom(m_v(kappa), r_v)_u,
        m_v(kappa) = kappa'_v - kappa'_{v+1},  r_v = kappa'_v - rho'_v.
Also eq:ncount:  n(kappa)-n(rho) = C(k,2) + inv(kappa/rho) + sum_v r_v (m_v - r_v).
"""
import itertools, functools
import engine as E
from sympy import symbols, cancel, expand, Poly, Integer, simplify, binomial, prod, factor
u = symbols('u')

def vm(m):   # v_m(t) = [m]_u!
    out = Integer(1)
    for i in range(1, m+1): out *= (1-u**i)/(1-u)
    return out

def v_lam(lam, n):
    lam = tuple(lam)+(0,)*(n-len(lam))
    out = Integer(1)
    for val in set(lam):
        out *= vm(sum(1 for z in lam if z == val))
    return out

@functools.lru_cache(maxsize=None)
def HL(lam, n):
    """Macdonald III (2.2): P_lam = (1/v_lam) sum_{w in S_n} w( x^lam prod_{i<j}(x_i-u x_j)/(x_i-x_j) )"""
    X = E.xs(n)
    lam = tuple(lam)+(0,)*(n-len(lam))
    base_num = Integer(1)
    for i in range(n):
        for j in range(i+1, n):
            base_num *= (X[i]-u*X[j])/(X[i]-X[j])
    mon = Integer(1)
    for v, e in zip(X, lam): mon *= v**e
    tot = 0
    for w in itertools.permutations(range(n)):
        sub = {X[i]: X[w[i]] for i in range(n)}
        tot += (mon*base_num).subs(sub, simultaneous=True)
    return cancel(expand(cancel(tot/v_lam(lam, n))))

def mult(lam, v):  return sum(1 for p in lam if p == v)
def qb(m, r):
    if r < 0 or r > m: return Integer(0)
    num = Integer(1); den = Integer(1)
    for i in range(r):
        num *= (1-u**(m-i)); den *= (1-u**(i+1))
    return cancel(num/den)

def vertical_strips(rho, k, maxlen):
    """kappa >= rho with kappa/rho a vertical k-strip: kappa_i - rho_i in {0,1}"""
    rl = list(rho)+[0]*(maxlen-len(rho))
    out=[]
    for add in itertools.product([0,1], repeat=maxlen):
        if sum(add)!=k: continue
        kap=[rl[i]+add[i] for i in range(maxlen)]
        if all(kap[i]>=kap[i+1] for i in range(maxlen-1)):
            out.append(tuple(z for z in kap if z>0))
    return out

print("=== sanity: HL P_{(1^k)} = e_k, from Macdonald III (2.2) ===")
for n in [2,3]:
    X=E.xs(n)
    for k in range(1,n+1):
        print(f"  n={n} P_(1^{k}) - e_{k} =", simplify(HL(tuple([1]*k),n)-E.e_sym(k,X)))

print()
print("=== psi' Pieri rule, by content ===")
ok=bad=0; vac=0; fails=[]
for n in [3,4]:
    X=E.xs(n)
    for d in range(0,4):
        for rho in (list(E.partitions(d,maxlen=n)) if d>0 else [()]):
            rho=tuple(rho)
            for k in range(1,n+1):
                lhs = cancel(expand(E.e_sym(k,X)*HL(rho,n)))
                strips = vertical_strips(rho,k,n)
                if not strips:
                    vac+=1; continue
                rhs=0
                for kap in strips:
                    kp=E.conj(kap); rp=E.conj(rho)
                    coef=Integer(1)
                    vmax=max([kap[0] if kap else 0, rho[0] if rho else 0])
                    for v in range(1,vmax+1):
                        kpv  = kp[v-1] if v-1<len(kp) else 0
                        kpv1 = kp[v]   if v  <len(kp) else 0
                        rpv  = rp[v-1] if v-1<len(rp) else 0
                        mv = kpv-kpv1          # = m_v(kappa)
                        rv = kpv-rpv
                        assert mv == mult(kap,v), (kap,v,mv,mult(kap,v))
                        coef *= qb(mv,rv)
                    rhs += coef*HL(kap,n)
                rhs=cancel(expand(rhs))
                if cancel(expand(lhs-rhs))==0: ok+=1
                else: bad+=1; fails.append((n,rho,k))
print(f"  psi' Pieri: {ok} of {ok+bad} pass, {bad} fail ({vac} skipped: no vertical k-strip exists)")
for f in fails[:5]: print("     FAIL",f)
print("  (assertion m_v(kappa) == kappa'_v - kappa'_{v+1} held on every term)")

print()
print("=== negative controls (each MUST fail) ===")
def ctrl(name, coeffun):
    o=b=0
    for n in [3]:
        X=E.xs(n)
        for d in range(1,4):
            for rho in E.partitions(d,maxlen=n):
                rho=tuple(rho)
                for k in range(1,n+1):
                    strips=vertical_strips(rho,k,n)
                    if not strips: continue
                    lhs=cancel(expand(E.e_sym(k,X)*HL(rho,n)))
                    rhs=0
                    for kap in strips: rhs+=coeffun(kap,rho)*HL(kap,n)
                    if cancel(expand(lhs-cancel(expand(rhs))))==0: o+=1
                    else: b+=1
    print(f"  {name:46s} {b} of {o+b} FAIL (ok={o})")

def coef_correct(kap,rho):
    kp=E.conj(kap); rp=E.conj(rho); c=Integer(1)
    for v in range(1,(kap[0] if kap else 0)+1):
        kpv=kp[v-1] if v-1<len(kp) else 0; kpv1=kp[v] if v<len(kp) else 0
        rpv=rp[v-1] if v-1<len(rp) else 0
        c*=qb(kpv-kpv1,kpv-rpv)
    return c
def coef_rhomult(kap,rho):   # use m_v(rho) instead of m_v(kappa)
    kp=E.conj(kap); rp=E.conj(rho); c=Integer(1)
    for v in range(1,(kap[0] if kap else 0)+1):
        rpv=rp[v-1] if v-1<len(rp) else 0; rpv1=rp[v] if v<len(rp) else 0
        kpv=kp[v-1] if v-1<len(kp) else 0
        c*=qb(rpv-rpv1,kpv-rpv)
    return c
def coef_all1(kap,rho): return Integer(1)
ctrl("C1 m_v(rho) in place of m_v(kappa)", coef_rhomult)
ctrl("C2 all coefficients = 1",            coef_all1)
ctrl("C3 correct coefficient (must PASS)", coef_correct)

print()
print("=== eq:ncount : n(kappa)-n(rho) = C(k,2) + inv(kappa/rho) + sum_v r_v(m_v-r_v) ===")
# inv(kappa/rho): Rick's definition -- locate it
