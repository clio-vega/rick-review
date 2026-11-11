import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import io, contextlib
sys.argv=[sys.argv[0],'0']
with contextlib.redirect_stdout(io.StringIO()):
    import check as C
def Htab(m):
    Wd = C.words(m); H = {}
    for mu, w in Wd.items():
        k = C.kappa_of(mu, m); d = sum(k)
        pts = [(j, sum(C.apply_word(w, {(j,)*m: 1}, m).values())) for j in range(d+1)]
        H[k] = C.interp(pts)
    return H

