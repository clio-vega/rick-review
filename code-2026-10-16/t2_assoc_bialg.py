from qsym_indep import *

SL3 = [[2,-1],[-1,2]]
PHIS = {
  "phi=0":        [[0,0],[0,0]],
  "Feigin 1->2":  [[0,-1],[0,0]],      # antisym part phi(a1,a2)-phi(a2,a1) = -1 = (a1,a2)
  "Feigin 2->1":  [[0,0],[-1,0]],      # antisym part = +1
  "random bilin": [[3,-2],[5,1]],
}

def test_assoc(S, words):
    ok = bad = 0
    for a in words:
        for b in words:
            for c in words:
                L = lin_product(S, lin_product(S, {a:lone()}, {b:lone()}), {c:lone()})
                R = lin_product(S, {a:lone()}, lin_product(S, {b:lone()}, {c:lone()}))
                if L == R: ok += 1
                else: bad += 1
    return ok, bad

def test_bialg(S, words):
    """Delta(M_a * M_b) = (m@m)(1@c@1)(Delta M_a @ Delta M_b),
       c(x@y) = q^{(|x|,|y|)} y@x  with the TRUE symmetrised form."""
    ok = bad = 0
    for a in words:
        for b in words:
            # LHS
            lhs = defaultdict(lzero)
            for w, cf in lin_product(S, {a:lone()}, {b:lone()}).items():
                for k in range(len(w)+1):
                    lhs[(w[:k], w[k:])] = ladd(lhs[(w[:k], w[k:])], cf)
            lhs = {k:v for k,v in lhs.items() if v}
            # RHS
            rhs = defaultdict(lzero)
            for i in range(len(a)+1):
                ap, app = a[:i], a[i:]
                for j in range(len(b)+1):
                    bp, bpp = b[:j], b[j:]
                    br = lmono(S.truepair(wdeg0(app,S.n), wdeg0(bp,S.n)))
                    left  = lin_product(S, {ap:lone()},  {bp:lone()})
                    right = lin_product(S, {app:lone()}, {bpp:lone()})
                    for wl, cl in left.items():
                        for wr, cr in right.items():
                            rhs[(wl,wr)] = ladd(rhs[(wl,wr)], lmul(br, lmul(cl,cr)))
            rhs = {k:v for k,v in rhs.items() if v}
            if lhs == rhs: ok += 1
            else: bad += 1
    return ok, bad

words = words_up_to((2,2))
print("DOMAIN: words of degree <= (2,2) in rank 2:", len(words), "words")
print("  => assoc domain =", len(words)**3, "triples;  bialg domain =", len(words)**2, "pairs")
print()
for name, phi in PHIS.items():
    S = Setup(SL3, phi)
    ao, ab = test_assoc(S, words)
    bo, bb = test_bialg(S, words)
    print(f"{name:14s}  assoc {ao}/{ao+ab} pass, {ab} FAIL   |  bialg {bo}/{bo+bb} pass, {bb} FAIL")
print()
print("POSITIVE CONTROL: plant inverted braiding q^{-(a,b)} in the crossing weights")
INV = [[-2,1],[1,-2]]
for name, phi in [("phi=0", PHIS["phi=0"]), ("Feigin 1->2", PHIS["Feigin 1->2"])]:
    S = Setup(SL3, phi, braid=INV)
    ao, ab = test_assoc(S, words)
    bo, bb = test_bialg(S, words)
    print(f"  {name:14s} assoc {ao}/{ao+ab}, {ab} FAIL  |  bialg {bo}/{bo+bb}, {bb} FAIL")
print()
print("POSITIVE CONTROL 2: plant a NON-bilinear phi (break the cocycle condition)")
class BadPhi(Setup):
    def ph(self, a, b):
        return sum(a)*sum(b) + (1 if (sum(a)>1 and sum(b)>1) else 0)   # not bilinear
S = BadPhi(SL3, PHIS["phi=0"])
ao, ab = test_assoc(S, words)
bo, bb = test_bialg(S, words)
print(f"  non-bilinear phi  assoc {ao}/{ao+ab}, {ab} FAIL  |  bialg {bo}/{bo+bb}, {bb} FAIL")
