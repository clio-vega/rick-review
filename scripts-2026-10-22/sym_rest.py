import sympy as sp
ws={k:sp.Symbol(f'w{k}') for k in range(1,12)}
def rho_s(kappa,X,ws):
    e=sp.Integer(1)
    for k in range(1,kappa): e*=(1-ws[k]/X)
    return e
def Alt_sym(kap,th,xs,ws,shift):
    r=len(kap)
    def ent(k,j):
        num=sp.expand(rho_s(kap[j],xs[k],ws)*xs[k]**(kap[j]-1))
        ex=j+th[j]+shift-(kap[j]-1); assert ex>=0
        return sp.expand(xs[k]**ex*num)
    return sp.Matrix(r,r,ent).det(method='berkowitz')
cases=[((2,3,6,7),(0,1),0,{2:1,3:-2}), ((2,3,6,7),(2,3),2,{0:5,1:-3}),
       ((3,4,5,6),(0,3),2,{}), ((1,4,5,6,7),(1,4),0,{0:3})]
ok=0
for kap,(p,q),t0,oth in cases:
    r=len(kap); b=q-p+1; e=t0-(b-1); s=kap[p]
    xs=[sp.Symbol(f'x{k}') for k in range(r)]
    th1=[oth.get(j,0) for j in range(r)]; th2=list(th1)
    for j in range(p,q+1): th1[j]=t0-(j-p); th2[j]=e
    C=sp.Integer(1)
    for m in range(b-1): C*=ws[s+m]**(b-1-m)
    sh=max(0, max(kap[j]-1-j-min(th1[j],th2[j]) for j in range(r)))
    d=sp.expand(Alt_sym(kap,th1,xs,ws,sh)-C*Alt_sym(kap,th2,xs,ws,sh))
    ok+=(d==0); print(f"  kap={kap} block={(p,q)} t0={t0} out={oth}: holds={d==0}",flush=True)
print(f"SYMBOLIC (hard cases): {ok}/{len(cases)}")
# negative controls
print("== negative controls (must be nonzero) ==",flush=True)
kap=(2,3,4); p,q=0,2; r=3; xs=[sp.Symbol(f'x{k}') for k in range(r)]
def run(th1,th2,C,lab):
    sh=max(0, max(kap[j]-1-j-min(th1[j],th2[j]) for j in range(r)))
    d=sp.expand(Alt_sym(kap,th1,xs,ws,sh)-C*Alt_sym(kap,th2,xs,ws,sh))
    print(f"  {lab}: correctly nonzero = {d!=0}",flush=True)
Cgood=ws[2]**2*ws[3]
run([1,0,-1],[-1,-1,-1],sp.Integer(1),"C := 1 (constant dropped)")
run([2,0,-2],[-2,-2,-2],Cgood,"slope -2 instead of -1")
run([1,0,-1],[-1,-1,-1],ws[3]**2*ws[4],"wrong C (shifted s)")
kap2=(2,4,5); xs2=[sp.Symbol(f'x{k}') for k in range(3)]
def run2(th1,th2,C,lab):
    sh=max(0, max(kap2[j]-1-j-min(th1[j],th2[j]) for j in range(3)))
    d=sp.expand(Alt_sym(kap2,th1,xs2,ws,sh)-C*Alt_sym(kap2,th2,xs2,ws,sh))
    print(f"  {lab}: correctly nonzero = {d!=0}",flush=True)
run2([1,0,-1],[-1,-1,-1],ws[2]**2*ws[3],"non-consecutive labels (2,4,5)")
