import sympy as sp
from itertools import permutations
exec(open('verify66.py').read().split('# ---------------- checks')[0])

print("== E. Cor 5.2 ground truth: (2,2,2)->(3,3) should have Lead [3]_t (t+2).  x=y=3, so m_xy=2 ==")
want = sp.expand((1+t+t**2)*(t+2))
got  = thm66(2,2,2,3,3)
print("   want =", want)
print("   got  =", sp.expand(got))
print("   MATCH" if sp.simplify(got-want)==0 else "   MISMATCH")

print()
print("== F. Does Thm 6.6 break if (x,y) is given with x < y?  (Example 6.8 targets) ==")
w1 = 2*t**13+3*t**12+3*t**11+6*t**10+6*t**9+6*t**8+9*t**7+6*t**6+3*t**5+9*t**4+6*t**3+3*t+4
w2 = sp.expand((t+1)*(t**2+1)*(2*t**8+t**7+t**6+3*t**4+t**3+t**2-t+2))
for (lab,a,b,c,x,y,w) in [("(3,3,3)->(7,2) as x=7,y=2",3,3,3,7,2,w1),
                          ("(3,3,3)->(7,2) as x=2,y=7",3,3,3,2,7,w1),
                          ("(4,4,2)->(7,3) as x=7,y=3",4,4,2,7,3,w2),
                          ("(4,4,2)->(7,3) as x=3,y=7",4,4,2,3,7,w2)]:
    d = sp.simplify(thm66(a,b,c,x,y)-w)
    print("   %-32s %s" % (lab, "MATCH" if d==0 else "MISMATCH"))

print()
print("== G. Systematic: is the printed Thm 6.3 RHS symmetric under x<->y? ==")
nsym=0; nasym=0; asym_cases=[]
for a in range(2,6):
  for b in range(1,4):
    for c in range(1,4):
      n=a+b+c
      for y in range(1,n//2+1):
        x=n-y
        if x<1 or y<1: continue
        try:
            d=sp.simplify(sp.together(Phi(a,b,c,x,y)-Phi(a,b,c,y,x)))
        except Exception as ex:
            print("   err",a,b,c,x,y,ex); continue
        if d==0: nsym+=1
        else:
            nasym+=1; asym_cases.append((a,b,c,x,y))
print("   symmetric: %d    ASYMMETRIC: %d" % (nsym,nasym))
print("   asymmetric (a,b,c,x,y) first 25:", asym_cases[:25])
import collections
print("   asymmetric by a:", collections.Counter(a for (a,b,c,x,y) in asym_cases))
print("   symmetric-case a-values present overall: a in 2..5")
