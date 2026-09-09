"""Day180 §3 bullet: at e=2, does legality force a PARITY constraint on P+Q?
P = ht_2(b,M) = [b+1 in M],  Q = ht_2(c,M) = [c+1 in M], for two legal 2-moves b,c."""
def parts(n, maxpart):
    if n == 0: yield (); return
    for k in range(min(n, maxpart), 0, -1):
        for rest in parts(n-k, k):
            yield (k,)+rest
def maya(lam, cutoff=30):
    M=set(range(-cutoff,0)); lam=list(lam)
    for i in range(len(lam)+cutoff):
        li=lam[i] if i<len(lam) else 0
        M.discard(-(i+1)); M.add(li-(i+1))
    return M
seen=set(); examples={}
for n in range(0,13):
  for lam in parts(n,8):
    M=maya(lam)
    legal=[b for b in M if b+2 not in M and b>-15]
    for b in legal:
      for c in legal:
        if b==c: continue
        P=int(b+1 in M); Q=int(c+1 in M)
        seen.add((P,Q)); examples.setdefault((P,Q),(lam,b,c))
print("(P,Q) pairs realised at e=2:", sorted(seen))
print("P+Q parities realised:", sorted({(P+Q)%2 for P,Q in seen}))
for k in sorted(seen): print(f"  {k}: lam={examples[k][0]} b={examples[k][1]} c={examples[k][2]}")
