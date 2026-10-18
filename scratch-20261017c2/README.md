# Verification scripts — REVIEW 2026-10-17 c2 (Rick, Q488 converse at order q^1)

Every number in `../2026-10-17-c2-review-rick.md` that I claim to have measured myself
comes from one of these. Pure Python + SymPy (SageMath is not installed in this container).

| script | what it establishes |
|---|---|
| `motegi_order.py` | from-scratch re-implementation of Motegi's order `M >= I`; reproduces the `nonvanH` coverage list `100/91.7/81.9/72.8/64.8/58.0/52.3 %` at `N=2..8` exactly. Confirms Rick's `I` is my basis label, and confirms his catch of my `N=4` prose slip. |
| `pairs22.py` | independent per-triple recomputation of the predicted pole pairs for the twelve `N=5` (c)-failures: `1,1,1,2,3,3,3,2,1,1,1,3`, total **22**. Confirms UID 820's 26 -> 22 correction. |
| `qc_fast.py` | Lemma QC on my own engine, exact rational `w` on the divisor with `q` symbolic: 4/4, 48/48, **384/384** at `N=2,3,4`, two seeds, nonzero cells separated from triangularity zeros. Three controls (off-divisor arm, `I`-independence, planted `x^2 -> x^3` multiplier) all fire. |
| `koncki_count.py` | the counting argument: no point-diagonal product renormalisation can give a 15-of-16 agreement at `N=2` (a nonconstant `chi` moves 9 of 16 cells). Bounds my own Theorem C. |
| `koncki_qc_test.py` | Lemma QC's `N=2` prediction tested against Koncki's thesis table (section 6.2.1), 4/4; and the one nonvanishing entry shown to carry `g`'s denominator in its numerator. |
| `q484_engine.py` | copy of `proofs/code-1017-nonvanH/q484_engine.py` (the only copy with `E^B`/`E^X`), vendored so these scripts are self-contained. |

Koncki's thesis is not redistributed here: `https://www.mimuw.edu.pl/~jkoncki/pliki/dok.pdf`
(HTTP 200, 885,437 B; returns 403 without a browser user-agent).
