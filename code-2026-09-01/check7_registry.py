"""The registry node C5-level-1-signature-word states:
     word = A^delta (RA)^m,  delta = [i = 0 mod e],  m = #{r : r = -i mod e, lam_r > lam_{r+1}}
   The tex (Step 3) states:
     bottom-up word = (AR)^n A^delta
   Test BOTH against computation, in both reading orders.
"""
from clio_sig import partitions_upto, signature

def m_registry(lam, i, e):
    ext = list(lam) + [0, 0]
    return sum(1 for r in range(len(lam)+1) if r % e == (-i) % e and ext[r] > ext[r+1])

def m_corrected(lam, i, e):
    ext = list(lam) + [0]
    return sum(1 for r in range(1, len(lam)+1) if r % e == (-i) % e and ext[r-1] > ext[r])

bad_reg_bu = bad_reg_td = bad_tex_bu = bad_corr_td = 0
tot = 0
first = {}
for e in range(2, 7):
    for lam in partitions_upto(10):
        mu = tuple(e*p for p in lam)
        for i in range(e):
            bu = signature(mu, i, e, 'bottom_up')[0]
            td = signature(mu, i, e, 'top_down')[0]
            d  = 'A' if i % e == 0 else ''
            mr, mc = m_registry(lam,i,e), m_corrected(lam,i,e)
            tot += 1
            for key, actual, pred in [('registry-word-vs-bottomup', bu, d + 'RA'*mr),
                                      ('registry-word-vs-topdown',  td, d + 'RA'*mr),
                                      ('tex-word-vs-bottomup',      bu, 'AR'*mc + d),
                                      ('corrected-vs-topdown',      td, d + 'RA'*mc)]:
                if actual != pred and key not in first:
                    first[key] = (e, lam, i, f"actual={actual!r}", f"predicted={pred!r}")
            bad_reg_bu += (bu != d + 'RA'*mr)
            bad_reg_td += (td != d + 'RA'*mr)
            bad_tex_bu += (bu != 'AR'*mc + d)
            bad_corr_td += (td != d + 'RA'*mc)

print(f"{tot} triples (e<=6, |lam|<=10)\n")
for label, bad, key in [("registry word A^d(RA)^m  vs BOTTOM-UP word", bad_reg_bu, 'registry-word-vs-bottomup'),
                        ("registry word A^d(RA)^m  vs TOP-DOWN  word", bad_reg_td, 'registry-word-vs-topdown'),
                        ("tex word (AR)^n A^d      vs BOTTOM-UP word", bad_tex_bu, 'tex-word-vs-bottomup'),
                        ("A^d(RA)^m, m corrected   vs TOP-DOWN  word", bad_corr_td, 'corrected-vs-topdown')]:
    print(f"  {label}:  {bad:5d}/{tot} mismatches" + (f"\n        first: e={first[key][0]} lam={first[key][1]} i={first[key][2]} {first[key][3]} {first[key][4]}" if bad else "   CLEAN"))
