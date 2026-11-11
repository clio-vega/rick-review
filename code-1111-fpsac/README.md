# code-1111-fpsac — independent checks for the 2026-11-11 review of Rick's FPSAC cut

Target: grandpa-rick/work-in-progress `6dbecb8` (papers/lg-og-fpsac-cut) == `9fa6b0c`
(papers/lg-og-fpsac-submit), mathematically identical (diffed: 5 hunks, front matter / footnote /
acknowledgements / declaration placeholder only).

Pure Python, exact `Fraction`s, written from the PRINTED statements. Shares no code with Rick.

- `check.py M` — type C_m Demazure engine (G1) + brute-force counts. Checks Thm 1.1, Lemmas 2.1–2.3,
  Lemma 3.1(a), Lemma 4.1, Prop 4.3 (star) at 20 points incl. negative/half-integer x, Thm 1.4 (LG),
  Prop 6.1 (Bridge — independent route to half-integer values), Thm 6.2, Cor 6.4, Thm 1.5 (i)–(iii),
  Cor 1.6, Table 1, worked examples. `check4.out`: all strict kappa, m <= 4, 0 failures.
- `extra.py M` — Lemma 6.3, Rem 4.4 vs BR Thm 5.5 recursion on R(theta) (engine:
  `../code-1024c2-thmI/referee33.py`, implemented 10-24 from arXiv:1005.2605v1), Rem 5.1/6.5
  combinatorics, and five lesion controls (all fire). `extra4.out`.
- `remT.py` — Rem 6.6: exact unitriangular sqrt T of A_oA_e; s_{x+1/2} = T s_x. `remT4.out`.
- `fill_review.py` — one-off patch that put these numbers into the review .tex.

m = 5 was attempted and stopped after ~7 min (brute-force strict-map counts dominate). NOT claimed.
