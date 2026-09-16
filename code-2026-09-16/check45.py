import sympy as sp, re
q,t = sp.symbols('q t')
def qi(n): return sp.expand(sum(t**i for i in range(n))) if n>0 else sp.Integer(0)
def level(l,a,r):
    pre=(q-1)/q**a
    if l==0: return 1/sp.Integer(1)/q**a
    if l==1: return pre*qi(r+2-a)
    if l==2: return pre*(qi(r+4-a)/qi(2))*(qi(r+3-a)*q-t*qi(r+1-a))
    if l==3: return pre*(qi(r+6-a)/(qi(2)*qi(3)))*(qi(r+5-a)*qi(r+4-a)*q**2
             - t*qi(2)*qi(r+2-a)*qi(r+4-a)*q + t**3*qi(r+1-a)*qi(r+2-a))
txt=open('out_45.txt').read()
data={}
for m in re.finditer(r'e_\((\d+)(?:, (\d+))?\) : (.+)', txt):
    k1=int(m.group(1)); k2=int(m.group(2)) if m.group(2) else 0
    data[(k1,k2)]=sp.sympify(m.group(3))
a,r=4,5
print("e_4 * e_5 : Rick's level-l meta-shape (fitted only at (4,4)) vs my independent m=9 compute")
for lam,val in sorted(data.items(), reverse=True):
    k=lam[1]; l=a-k
    if l>3:
        print("   e_%s  l=%d : Rick has no formula (top level)" % (str(lam),l)); continue
    d=sp.simplify(sp.expand(sp.together(val-level(l,a,r))))
    print("   e_%s  l=%d : %s" % (str(lam), l, "MATCH" if d==0 else "*** MISMATCH: %s"%d))
