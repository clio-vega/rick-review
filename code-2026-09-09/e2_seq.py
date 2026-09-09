"""Sequential reading: move b->b+2 giving M', then c legal in M'. P from M, Q from M'."""
def parts(n,mx):
    if n==0: yield (); return
    for k in range(min(n,mx),0,-1):
        for r in parts(n-k,k): yield (k,)+r
def maya(lam,cut=30):
    M=set(range(-cut,0)); lam=list(lam)
    for i in range(len(lam)+cut):
        li=lam[i] if i<len(lam) else 0
        M.discard(-(i+1)); M.add(li-(i+1))
    return M
seen=set()
for n in range(0,13):
  for lam in parts(n,8):
    M=maya(lam)
    for b in [x for x in M if x+2 not in M and x>-15]:
      P=int(b+1 in M)
      Mp=(M-{b})|{b+2}
      for c in [x for x in Mp if x+2 not in Mp and x>-15]:
        Q=int(c+1 in Mp)
        seen.add((P,Q))
print("sequential (P,Q):",sorted(seen),"  P+Q parities:",sorted({(P+Q)%2 for P,Q in seen}))
