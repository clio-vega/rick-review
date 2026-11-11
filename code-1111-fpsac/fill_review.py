"""Fill the m<=4 results into the review .tex (one-off patch). Clio 2026-11-11."""
p = '/home/clio/projects/reviews/2026-11-11-review-rick-fpsac-cut-6dbecb8.tex'
s = open(p).read()
rows = r"""Thm 1.1(a) $H(j)=F_\kappa(2j)$, $j\le5$ & 180/180\\
Thm 1.1(b) $s_j=N_\kappa(j)$, $j\le6$ & 180/180\\
Lemma 3.1(a): reduced-word length $=|\kappa|$; degree check & 30/30, 30/30\\
Prop 4.3 $(\star)$ at $x\in\{-3,-\frac52,\dots,\frac{13}2\}$ & 600/600\\
Lemma 4.1 closed form vs brute force & 144/144\\
Lemma 2.3 anchor; $r(\kappa)=\max(\kappa_i+2i-2)$ & 26/26, 26/26\\
Thm 1.4 (LG): zeros / positive / monotone & 30/30 each\\
Prop 6.1 Bridge, $a\le3$ & 120/120\\
Thm 6.2 $H(-\frac12)=2^{-\kappa_1}$ & 30/30\\
Lemma 6.3 (a), (b at $a=1$), (c) & 174/174, 174/174, 30/30\\
Cor 6.4 row formula, $a\le8$ & 208/208\\
Thm 1.5 (i) zero iff, $a\le8$ & 208/208\\
Thm 1.5 (ii) signs ($2a>\kappa_1$ / $2a<\kappa_1$ / $2a=\kappa_1$) & 175/175, 3/3, 6/6\\
Thm 1.5 (iii) bound / equality for $2a\le\kappa_1$ / integrality & 208/208, 30/30, 208/208\\
Cor 1.6, $a=m..m+4$ & 150/150\\
Rem 4.4 vs BR Thm 5.5 on $R(\theta)$ & 144/144\\
Rem 5.1 / 6.5 combinatorics & 64/64, 26/26, 26/26, 22/22\\
Rem 6.6 $s_{x+1/2}=Ts_x$ & 224/224\\"""
subs = [
    ('RESULTSTABLE', rows),
    (r'check (at $m\le M_{\max}$) & result',
     r'check (all strict $\kappa$, $m\le4$; total failures 0) & result'),
    (r'independent Demazure engine 84/84 (a), 84/84 (b) at $m\le3$ (m$\le$5: see \S5)',
     r'independent Demazure engine, $m\le4$: 180/180 (a), 180/180 (b)'),
    ('I checked the closed form against brute force on all 34 (resp.\\ all) pairs at $m\\le3$ (resp.\\\n$m\\le4$).',
     r'The closed form matches brute force on all 144 pairs at $m\le4$.'),
    ('280/280 at $m\\le3$, plus the $m\\le4$ recheck at\n$x=\\tfrac52$.', r'600/600 at $m\le4$.'),
    (r'56/56 at $m\le3$, $a\le3$', r'120/120 at $m\le4$, $a\le3$'),
]
for old, new in subs:
    n = s.count(old)
    print(f"{n} x {old[:50]!r}")
    s = s.replace(old, new)
open(p, 'w').write(s)
