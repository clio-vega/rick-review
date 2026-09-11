import itertools, sympy as sp
t, q = sp.symbols('t q')

# ---- (1) Rick's Day 180 §6 SPECIFIC CONSTANTS (untuned cells, not just degrees) ----
def Delta(u,i,j,l): return (u[i]+u[j]-2*u[l]+1)/((u[i]-u[l])*(u[j]-u[l]))
def Pi_P(N,P):
    u=sp.symbols(f'u1:{N+1}'); tot=0
    for i,j in itertools.combinations(range(N),2):
        term=(u[i]+u[j]+1)*P(u[i],u[j])
        for l in range(N):
            if l not in (i,j): term*=Delta(u,i,j,l)
        tot+=term
    return sp.expand(sp.cancel(sp.together(tot)))
print("== Rick's Day 180 §6 stated CONSTANTS (he gives values, not just degrees) ==")
for (N,name,P,claimed) in [(4,"u_i+u_j",     lambda x,y:x+y,        10),
                           (5,"(u_i+u_j)^2", lambda x,y:(x+y)**2,   35),
                           (5,"u_i^2+u_j^2", lambda x,y:x**2+y**2,  15),
                           (6,"(u_i+u_j)^3", lambda x,y:(x+y)**3,  126)]:
    v=Pi_P(N,P)
    print(f"  |S|={N} P={name:14} Rick says const {claimed:4}  ->  computed {v}   "
          f"{'MATCH' if sp.simplify(v-claimed)==0 else '*** MISMATCH ***'}")

# ---- (2) The (1+t) separator: order of vanishing at t=-1  (my Q105 method) ----
print("\n== Item 2: is Rick's (1+t) the same factor as mine? ==")
print("   Q105 separator = ORDER of vanishing at t=-1 as a FUNCTION of the family index.")
XP2 = t*(1+t)                                   # coefficient of e_2   in X_{P_2}(q,t)
XP3 = {'e_{2,1}': q**-1*t**2,
       'e_3'    : q**-1*t**2*(1+t+t**2)*(-1+q+q*t)}   # Hikita Ex 4.6 / Rick Day 190
def ordm1(f):
    f=sp.simplify(f)
    if f==0: return sp.oo
    n=0; g=sp.together(f)
    while sp.simplify(g.subs(t,-1))==0 and n<12:
        g=sp.simplify(sp.diff(sp.together(f),t,n+1)); n+=1
    return n
print(f"   X_P2(q,t): coeff of e_2 = {sp.factor(XP2)};   ord_{{t=-1}} = {ordm1(XP2)}")
for k,v in XP3.items():
    print(f"   X_P3(q,t): coeff of {k:8} = {sp.factor(v)};  value at t=-1 = {sp.simplify(v.subs(t,-1))}"
          f"   ord = {ordm1(v)}")
tot_m1 = {k: sp.simplify(v.subs(t,-1)) for k,v in XP3.items()}
print(f"   => X_P3(q,-1) = {tot_m1['e_{2,1}']} e_{{2,1}} + {tot_m1['e_3']} e_3  "
      f"{'(NONZERO)' if any(v!=0 for v in tot_m1.values()) else '(zero)'}")
print("   Rick's order function over n:  n=2 -> 1,  n=3 -> 0   (NOT constant)")
print("   My R_e(t) family (Q92/Q81): (1+t)-adic valuation of [R_e,R_f] is exactly 1")
print("   in EVERY one of 1140 pairs -> order function constant 1.")
print("   ORDER FUNCTIONS DIFFER  =>  the two (1+t)'s are DISTINCT (same verdict as Q105).")
