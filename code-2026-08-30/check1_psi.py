from core import *
import time, pickle
BMAX = 7
Psi = {}
t0=time.time()
for b in range(BMAX+1):
    Psi[b] = to_E(Psi_u(e2**b))
    print(f"Psi_{b}  w<= {wmax(Psi[b])}   ({time.time()-t0:.1f}s)")
print()
for b in range(BMAX+1):
    print(f"tops[{b}] =", sp.factor(top(Psi[b])) if b<4 else top(Psi[b]))
pickle.dump({b:sp.srepr(v) for b,v in Psi.items()}, open('psi.pkl','wb'))
