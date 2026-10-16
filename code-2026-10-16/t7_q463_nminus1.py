import sys, sympy as sp
sys.path.insert(0,'/home/clio/projects/reviews/code-2026-10-14')
src=open('/home/clio/projects/reviews/code-2026-10-14/hikita_dfk_Y_match2.py').read()
src=src.split('print("=== Y^H_i')[0]
exec(src)

print("TASK B / Q463: test Rick's Proposition  Y^H_i = theta^{N-1} (Y^DFK_{i,-1})^{-1}")
print("i.e.  Y^H_i o Y^DFK_{i,-1} = theta^{N-1} . id,  for ALL 1 <= i <= N.")
print("Instrument: MY OWN 2026-10-14 Q463 engine (controls C1-C5 passed then). Exact in q, theta.")
print()
allok=True
for N in (2,3,4):
    x,q,th,X,Y_hik,Y_dfk_n = engine(N)
    tests=[tuple(0 for _ in range(N)), tuple(1 if k==0 else 0 for k in range(N)),
           tuple(1 for _ in range(N))]
    if N==2: tests+=[(2,1),(1,-1),(3,2)]
    elif N==3: tests+=[(2,1,0),(0,1,2),(2,-1,1)]
    else: tests+=[(2,1,0,0),(0,1,2,1),(2,-1,1,0)]
    target=th**(N-1)
    for i in range(1,N+1):
        vals=set()
        for e in tests:
            f=sp.prod([X[k]**e[k] for k in range(N)])
            r=sp.simplify(sp.cancel(Y_hik(i,Y_dfk_n(i,-1,f))/f))
            vals.add(sp.powsimp(sp.nsimplify(r)))
        scalar = len(vals)==1 and all(len(v.free_symbols & set(x))==0 for v in vals)
        v=list(vals)[0] if len(vals)==1 else None
        hit = scalar and sp.simplify(v-target)==0
        if not hit: allok=False
        print(f"  N={N} i={i}: {'SCALAR' if scalar else str(len(vals))+' DISTINCT ratios'}"
              f"  value={v}  == theta^{{{N-1}}}: {hit}")
    print()
print("VERDICT: Rick's Proposition reproduces on my instrument for all i, N=2,3,4:", allok)
print()
print("NEGATIVE CONTROL: the same test at n=0 and n=+1 must NOT be scalar for i>=2")
for N in (3,):
    x,q,th,X,Y_hik,Y_dfk_n = engine(N)
    tests=[(0,0,0),(1,0,0),(1,1,1),(2,1,0),(0,1,2),(2,-1,1)]
    for n in (0,1):
        for i in (2,3):
            vals=set()
            for e in tests:
                f=sp.prod([X[k]**e[k] for k in range(N)])
                vals.add(sp.powsimp(sp.nsimplify(sp.simplify(sp.cancel(Y_hik(i,Y_dfk_n(i,n,f))/f)))))
            print(f"  N={N} n={n} i={i}: {len(vals)} distinct ratios -> {'NOT scalar (control fires)' if len(vals)>1 else 'scalar (control FAILED to fire)'}")
