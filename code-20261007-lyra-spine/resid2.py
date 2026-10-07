#!/usr/bin/env python3
"""Does the vendor structure explain the ESDOF deficit?  And what is PC1?"""
import csv, json, math
from pathlib import Path
import numpy as np
exec(open("mde2.py").read().split("E = load_error")[0].split('print("=')[0])  # reuse loaders

E = load_error("alphanli"); I,J = E.shape
def esdof_of(A):
    R = A - A.mean(axis=1,keepdims=True)
    k = R.var(axis=0)>0
    P = np.corrcoef(R[:,k],rowvar=False)
    lam = np.clip(np.linalg.eigvalsh(P),0,None)
    return float(lam.sum()**2/(lam**2).sum())
def perm_null_esdof(A, n=400, rng=None):
    vals=np.empty(n)
    for b in range(n):
        idx=np.argsort(rng.random(A.shape),axis=1)
        vals[b]=esdof_of(np.take_along_axis(A,idx,axis=1))
    return vals

rng = np.random.default_rng(20261007)
vendors = np.unique(vend)
print("="*78)
print("A. ONE JUDGE PER VENDOR -- does the deficit survive removing within-vendor pairs?")
print("="*78)
print(f"  {len(vendors)} vendors -> subpanel of {len(vendors)} judges, flat null = {len(vendors)-1}")
for s in ["alphanli","snli","mnli_m"]:
    A = load_error(s)
    obs=[]; nul=[]
    for rep in range(40):
        pick = np.array([rng.choice(np.flatnonzero(vend==v)) for v in vendors])
        sub = A[:,pick]
        obs.append(esdof_of(sub))
        nul.append(perm_null_esdof(sub, n=60, rng=rng).mean())
    obs=np.array(obs); nul=np.array(nul)
    print(f"  {s:8s} subpanel ESDOF = {obs.mean():.3f} (sd over draws {obs.std():.3f})"
          f"   permutation null = {nul.mean():.3f}"
          f"   deficit = {nul.mean()-obs.mean():+.3f}"
          f"   as % of max possible = {100*(nul.mean()-obs.mean())/(len(vendors)-1):.1f}%")
    Afull_def = None
print("  Compare FULL panel (J=32): deficit 27.63 - 21.24 = 6.39, i.e. 20.6% of 31.")

print()
print("="*78)
print("B. WHAT IS THE LEADING RESIDUAL FACTOR?  PC1 loading vs judge error rate")
print("="*78)
for s in ["alphanli","snli","mnli_m"]:
    A = load_error(s)
    R = A - A.mean(axis=1,keepdims=True)
    P = np.corrcoef(R,rowvar=False)
    lam,V = np.linalg.eigh(P); o=np.argsort(lam)[::-1]; lam=lam[o]; V=V[:,o]
    er = A.mean(axis=0)
    v1 = V[:,0]
    if np.corrcoef(v1,er)[0,1] < 0: v1 = -v1   # sign convention
    r = np.corrcoef(v1, er)[0,1]
    # how much of PC1 is explained by vendor group membership (one-way R^2)
    gm = np.array([v1[vend==v].mean() for v in vendors])
    fitted = np.array([gm[list(vendors).index(x)] for x in vend])
    r2_vendor = 1 - ((v1-fitted)**2).sum()/((v1-v1.mean())**2).sum()
    print(f"  {s:8s} lam1 = {lam[0]:.3f} (flat null {J/(J-1):.3f})"
          f"   corr(PC1 loading, judge error rate) = {r:+.3f}"
          f"   R^2 of PC1 on vendor = {r2_vendor:.3f}")
print("  A high corr with error rate would mean PC1 is a CAPABILITY axis (weak judges")
print("  failing together on the same items); a high vendor R^2 would mean it is a")
print("  vendor axis.  Both are reported; neither is assumed.")
