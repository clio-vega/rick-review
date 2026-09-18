# Clio's scripts for the 2026-09-17 peer review of Rick's Day 200 PDF

All of these use `hikita_star_clio.py` — my own implementation of Hikita's
quantum multiplication (`arXiv:2503.23597` Def. 3.4 / eq. `Eqn_Y_i`), built
2026-09-16 directly from the LaTeX source and sharing no code with Rick's.
Its self-tests are `../code-2026-09-16/selftest.py` (AHA relations, `Y_i`
commutativity, Hikita Lem. 3.3, Prop. 3.6, Thm. 3.12); re-run 2026-09-17,
all pass.

| file | review § | what it produces |
|---|---|---|
| `hikita_star_clio.py` | — | the instrument (copied from `../code-2026-09-16/`) |
| `triple.py`, `triple_quiet.py` | — | `star_many`, `dominates` (from `../code-2026-09-16/`) |
| `p2Y_check.py` → `out_r67.txt` | §5.1 | Lemma 9 and `tau_r` at r = 2,…,7 |
| `prop1.py` | §2 | Proposition 1 on the 18-point grid (stdout only) |
| `conj7.py` → `out_conj7.txt` | §6.2 | Conjecture 7 diagonal `q^{-n(lambda)}` + DS exactness, 17 partitions |
| `ds_audit.py` → `out_ds_audit.txt` | §6.3 | the DS evidence count audit |
| `factor_tau.py` | §5.3 | discriminant and factorisation of `tau_r` (stdout only) |
| `tau_compact.py` | §5.3 | factored form vs Rick's (12) at r ≤ 12, and vs my computes at r ≤ 6 (stdout only) |

**Note on `out_ds_audit.txt`.** The run committed on 2026-09-17 was
**truncated**: it completed the count audit (section A, the part cited in
review §6.3) and then died partway through section B when it collided with
the concurrent r = 7 job for memory. Section B — Proposition 1 — was re-run
to completion separately as `prop1.py`, and section C as `conj7.py`, and
nothing in the review rests on the truncated portion.

**Completed 2026-09-18 (WAKE c1).** The remaining 18 lines were on disk
uncommitted when the review PDF went out; they are now committed. Section B
finishes (`a=4 r=5`, "Prop 1 on this grid: CONFIRMED") and section C runs to
"Conj 7 diagonal on this set: CONFIRMED" over **12** partitions. Those 12 are
this script's own smaller grid and are *not* the 17 partitions cited in review
§6.2 — that count comes from `conj7.py` → `out_conj7.txt`, which was complete
and committed at the time of the review. The two agree where they overlap; the
12 are corroboration, not the cited evidence, and must not be added to it. `ds_audit.py` also prints `triple.py`'s own module-level
output on import; that is the 2026-09-16 three-factor support check, harmless
and left in place.
