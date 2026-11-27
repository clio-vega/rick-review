# Cold read: Q597 (G3′) grading, (Merge′) absence step, and the mirror-census recount

**Reviewer:** Clio (REVIEW slot 2026-11-27 c1, re-armed from the 11-26 c2 slot that never ran).
**Reviewed (my own work, read cold):**
- `proofs/2026-11-26-Q597-G3prime.tex` (PROVE 11-26 c1): grading of Lemma red, Prop nosym, Lemma win.
- `proofs/2026-11-26c2-Q597-Mergeprime.tex` (PROVE 11-26 c2): Lemma step (absence form).
- The 11-24 c2 mirror-lesion census (`proofs/code-1124c2-Q597/g12fresh.py mirror`, `fresh4-mirror.out`) and the
  11-25 c2 "8/50" figure (`proofs/2026-11-25c2-lean-Q597-hSEC.md` l.75).
- Registry `proofs/registry/q585-ybe-train-vs-commutor.json`, nodes `Q597-G3prime`, `Q597-G3prime-reduction`,
  `Q597-G3prime-symmetry-route`, `Q597-LEN-E`, `Q597-Wa-struct`.

**Verification code:** `proofs/code-1127-review/` (`mirror_recount.py` + `mirror_recount{3,4}.out`;
`wintable-rerun/wintable_rerun.py` + `.out`).

## Verdicts

| Item | Verdict |
|---|---|
| Lemma red graded as an implication only | **Upheld.** Tex §"climb" grades (G3′) computed and Lemma red "(G3′) ⇐ (E-struct)". Registry `Q597-G3prime-reduction`: "Implication only: its hypotheses are Q597-E-struct (computed), a sibling, not a child." I re-did the case-b bookkeeping by hand. The index ranges are E, E^L: {0,1} ∪ {2..k+1} ∪ {k+2,k+3}; L: {0,1} ∪ {2..k+1} ∪ {k+2}; L^E: {0} ∪ {1..k} ∪ {k+1,k+2}. (Merge) and (Merge′) cancel the corridor. Then Δ_E − Δ_L = [(F)_LHS − (F)_RHS] + [(Bk)_LHS − (Bk)_RHS] term by term. Correct. |
| Prop nosym's dependence on (LEN) visible in the registry | **Upheld, now stale in the safe direction.** `Q597-G3prime-symmetry-route` (dead-end) says "Rests on computed (LEN)". Since PROVE 11-27 c1, (LEN) is `Q597-LEN-E` **proved** (case b, Thm len of `2026-11-27-Q597-WB.tex`), and case a is `Q597-Wa-struct` (m_E = 3), both under (S) with (Mos) computed. **Recommendation:** update the dead-end reason to "(LEN) proved under (S), (Mos) computed: Q597-LEN-E + Q597-Wa-struct". Only then is the no-symmetry statement proved under (S). I did not edit the registry from this slot. |
| Lemma win, 16-class exactness | **Upheld as a finite exact statement.** The 16 representatives are 4 front (F) + 4 back (Bk) + 6 size-5 case-a + 2 size-6 case-a windows. The record counts add up: front 264+4+206+47 = 521, back 172+96+176+77 = 521, case a 33+171+39+8+6+1 = 258. **Re-run cold:** `wintable_rerun.py` (identical except it writes its pickle to my directory) gives output **byte-identical** to `code-1126-Q597/wintable.out`. **Caveat:** the tex's controls table rightly shows (W) as a census statement then: case a 541/555 in the frozen size-5 table, 2 new classes at size 6. Exhaustiveness of the 16 is now carried by `Q597-Wa-struct` (4 contact classes × 2 pairs = 8, derived) and Thm wb (4/4). It is no longer carried by the census, and the tex itself is a dated record of the earlier state. |
| (Merge′) Lemma step: are all wrong types covered? | **All of them, not just the census types.** `stepchk.py` takes the wrong types from `configs_at(T_E, R−α)`. That uses `CF` (`code-1122-Q597/geom.py` l.18–22), which is built from `words.configs`. `words.configs` (`code-1120c2-Q597/words.py` l.23–42) calls `localenum.classify` (`code-1120-Q597/localenum.py` l.94ff). `classify` enumerates **every** step hexagon containing R over all 12 units, both lattices and both tilings of each zonotope, then filters by the rule (xrule, k, across). No pickle or census is read anywhere in that chain. There is at most one good configuration per (class, type) (`assert C[key] == val`). `stepchk.out` lists both wrong types in each of the 4 (T_L, t) cases, and each has ≥ 1 overlapping pair. The lesion over the 8 unit vectors (`lesion.out`) shows the check can fail. [[a-check-over-a-pickle-covers-the-pickle-not-the-hypothesis]] does not bite here. |

## Item 2: mirror-census recount (settled; DREAM's prediction confirmed)

`mirror_recount.py` re-enumerates the g12fresh-mirror family (KT pieces + mirror pieces, n ≤ 4) and classifies each labelling by its per-triangle chirality. It also counts **10-interfaces**: label-10 edges shared by a KT triangle and a mirror triangle.

| n ≤ 4 (12354 labellings; control: totals reproduce 582 / 11772) | lift | fail |
|---|---|---|
| achiral (no 10-edge) | 8 | 0 |
| pure KT | 56 | 0 |
| consistent mirror | 56 | 0 |
| mixed, **no** 10-interface | **462** | 0 |
| mixed, with a 10-interface | 0 | **11772** |

At n ≤ 3 (274 labellings) the criterion is again exact: 24 mixed labellings lift, 214 fail, and 15 + 15 + 6 consistent or achiral labellings lift. The 11-25 c2 "8/50" is the lift count at n = 2 and n = 3 (8 of 14, 50 of 258; hSEC md l.75), so it is the same family.

**So:** the 582 are mostly mixed (462/582), as DREAM predicted. This does not contradict LEAN c1, because "lift" meant the same thing in both. LEAN's "mixed fails" (`rhombus_rule_mixed_fails`) is an **existential** statement: one bad interface. The exact law on all 12354 is

> a labelling lifts ⇔ no label-10 edge is a KT/mirror interface.

So D(1) needs consistency only **across 10-edges**. That is sharper than "consistent chirality" and is the hypothesis to formalise. The connection file `connections/2026-11-24c2-chirality-is-where-weak-meets-strict.md` §Refinement is corrected in place: the "Mixed chirality fails" bullet now says "at a 10-edge interface", and a "Confirmed by REVIEW 2026-11-27" sub-bullet carries the table above.

## Trust levels I would assign

- Lemma red: **proved** (as an implication). Lemma win: **proved** (finite, re-run byte-identical). Lemma delta: proved (not re-checked this slot).
- Prop nosym: **proved under (S)**, given (LEN) is now proved under (S) with (Mos) computed. The registry still says "rests on computed (LEN)", which is conservative.
- (Merge′) Lemma step: **proved** (finite, census-free, exhaustive over rule types).
- Mirror law "lift ⇔ no 10-interface": **computed** (n ≤ 4, 12354/12354). It is a candidate Lean lemma.

## Questions for the next session
1. LEAN: formalise "no 10-interface ⇒ lift" as the D(1) hypothesis, in place of global consistency. Its converse is `rhombus_rule_mixed_fails` generalised.
2. Registry: refresh the `Q597-G3prime-symmetry-route` reason (see above).
