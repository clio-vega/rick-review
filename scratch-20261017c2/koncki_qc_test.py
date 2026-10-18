"""
Test Lemma QC (Rick, UID 819) against Koncki's LG(2,4) table, read first-hand from
   J. Koncki, "Motivic Chern classes and stable envelopes" (thesis), Chapter 6, 6.2.1,
   https://www.mimuw.edu.pl/~jkoncki/pliki/dok.pdf
This is the table Rick says he has not checked, and which Motegi 2610.15344 (Discussion,
L5654-5658) compares to his normalised type-C weight functions in 15 of 16 entries.

Dictionary, FORCED by the support pattern (6 zeros, both sides, same shape):
   classes      13 <-> I={1,2}   14 <-> I={2}   23 <-> I={1}   24 <-> I={}
   fixed points e13 <-> M={1,2}  e14 <-> M={2}  e23 <-> M={1}  e24 <-> M={}
QC at N=2, M={1,2}, (a,b)=(1,2), M'' = {} , on H = {w_1 w_2 = 1} = {st = 1}:
   I != {} :  Atilde_{M,I}|_H = g * Atilde_{{},I} = g * 0 = 0      (triangularity)
   I  = {} :  Atilde_{M,{}}|_H = g * Atilde_{{},{}} != 0 ,  g = (1-q)^2/((1-q s^2)(1-q s^-2))
"""
import sympy as sp

s, t, y, q, lam = sp.symbols('s t y q lam', positive=True)
H = {t: 1/s}                      # the divisor st = 1

# --- the e13 row of Koncki's table, transcribed verbatim from 6.2.1 ---
# ceil(2lam) and ceil(lam) are integers; carry them as symbols m2 = ceil(2lam), m1 = ceil(lam).
m1, m2 = sp.symbols('m1 m2', integer=True)
row_e13 = {
    '13  (I={1,2})': (1 - s**2) * (1 - t**2) * (1 - s*t),
    '14  (I={2})  ': (1 - t**2) * (1 - s*t) * (1 + y) * s**(2 - 2*m1),
    '23  (I={1})  ': (1 - s*t) * (1 + y) * t**(1 - m2) * (s*(1 + y) + t + s*t*y),          # alpha=0
    '23b (I={1})  ': (1 - s*t) * (1 + y) * t**(1 - m2) * (1 + s*t*(1 + y) + s**2*y),       # alpha=1
    '24  (I={})   ': (1 + y) * (s*t)**(1 - m2) * (s*t*(1+y) - y + s**2*y + t**2*y + s**2*t**2*y**2),   # alpha=0
    '24b (I={})   ': (1 + y) * (s*t)**(1 - m2) * (s*t*(y + y**2) + 1 + s**2*y + t**2*y - s**2*t**2*y), # alpha=1
}

print("QC prediction at the deepest fixed point e13, restricted to {st = 1}:")
print("   I != empty  ->  must VANISH ;   I = empty  ->  must NOT vanish\n")
for name, expr in row_e13.items():
    r = sp.simplify(sp.expand(expr.subs(H)))
    print(f"  mC_y({name})|_e13  on st=1  =  {sp.factor(r)}")
    print(f"       vanishes? {r == 0}")

print("\n--- the one nonvanishing entry: does it carry g's denominator? ---")
k0 = sp.expand(row_e13['24  (I={})   '].subs(H) / ((1 + y) * (s*t)**(1 - m2)).subs(H))
k1 = sp.expand(row_e13['24b (I={})   '].subs(H) / ((1 + y) * (s*t)**(1 - m2)).subs(H))
print("alpha=0 bracket on st=1:", sp.factor(k0))
print("alpha=1 bracket on st=1:", sp.factor(k1))
print("the two alpha branches agree on st=1:", sp.simplify(k0 - k1) == 0)
target = sp.expand((1 + y*s**2) * (1 + y*s**-2))
print("equals (1 + y s^2)(1 + y s^-2)?", sp.simplify(k0 - target) == 0)

print("\n--- compare with the collapse multiplier g ---")
g = (1 - q)**2 / ((1 - q*s**2) * (1 - q*s**-2))
print("g =", g)
print("denominator of g      :", sp.factor(sp.denom(sp.cancel(g))))
print("Koncki numerator at y=-q:", sp.factor(sp.expand(target.subs(y, -q))))
print("SAME factor, numerator vs denominator:",
      sp.simplify(sp.expand(target.subs(y, -q)) - sp.expand((1 - q*s**2)*(1 - q*s**-2))) == 0)
