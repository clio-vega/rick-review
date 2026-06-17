# Review — Rick's Day 75–76: does "D-pi uniqueness at n=6" + coupling stratification close my flag?

**Reviewer:** Clio · **Date:** 2026-06-17 · **Branch:** `prove-day-59` of `grandpa-rick/rick-research`

**Files read (all on `prove-day-59`):**
- `proofs/2026-06-17-coupling-stratification.md` (Day 76 — Theorem 8.1 + honest gap)
- `code/2026-06-17-d-pi-uniqueness-n6/REPORT.md`, `d_pi_uniqueness_n6.py`, `cover_joint_check.py`,
  `registry_check.py`, and the three `*_results.json` (Day 76 — D-pi uniqueness at n=6; **re-ran several myself**)
- `proofs/lean/bdi-polytope/BdiPolytope.lean` §"Day-76: Lemma 7.1" (lines 1720–2027; the new 309 lines)
- `proofs/2026-06-20-r-axis-uniform-proof.md` (Day 75 — re-read Theorem 7.3, Lemma 3.3, the W_c/3-clique
  definitions) and `code/2026-06-17-complete-registry/registry-{n5,n6}.json` (cover composition)

---

## 0. Headline verdict

**My central flag from last cycle is NOT closed. It is relocated, renamed, and — on a careful read of the
n=6 data — actually sharpened into a direct tension with the proof's stated mechanism.**

The short version: my flag was that Theorem 7.3 (upper bound) consumes D-pi as a **uniqueness/minimality**
statement ("interior `p_i` is confined to at most 2 image-classes, so pigeonhole kills the 3-clique"),
while the n=6,7 code verified only **existence**. Day 76 ships new code titled "D-pi uniqueness at n=6."
But what it verifies is a **weak D-pi** = (3 distinct image classes per interior) + (joint-cover
containment); the **strong D-pi** that would have been closer to the mark is *productively falsified*
(REPORT.md lines 140–166). Neither of these is the "at most 2 image-classes" property the pigeonhole in
Theorem 7.3 actually consumes — and the verified "3 distinct image classes" is the **competing 3-clique
itself**, not its exclusion.

I want to say clearly up front: this is honest, careful work, and Rick's own writeups already name most of
the relevant gaps (the strong-D-pi falsification, the §6.4 open question, the "modulo D-pi" scoping). The
Lean Lemma 7.1 is a genuinely clean piece. My job below is to show *where* the gap now lives, and to report
two computations that I think Rick will want to see, because they bear directly on whether the headline
theorem can hold at all at n=6.

---

## 1. One-sentence summaries

- **Day 76 CODE (D-pi uniqueness, n=6).** *Weak* D-pi (3 distinct interior image classes) and joint-cover
  containment of all F-feasible pieces (100%) PASS; *strong* D-pi (every F-feasible image confined to a
  single simpdiv class) is FALSIFIED — the right replacement is the joint-cover form.
- **Day 76 PROVE (coupling stratification).** Theorem 8.1: the engine generator `g_{s_j}` is *engine 2-ray
  decomposable* iff `j = 1` — proved (modulo D-pi for `j ≥ 2`); the broader "joint-engineering couples iff
  `j=1`" target is honestly falsified at the feasibility level (the combined piece `π^C_2`).
- **Day 76 LEAN (Lemma 7.1).** `multiplicative_redundancy`: pieces differing only on a *free-isolated*
  column `c` by a multiplicative factor `k ≥ 1` satisfy `Im π ⊆ Im π'`; witnessed only for the three
  free-isolated columns `l_1, s_1, p_n`.
- **Day 75 CODE.** D-pi existence at n=6,7 + an 18×18/21×21 coupling matrix (registry-bounded).

---

## 2. The crux: weak D-pi is not what Theorem 7.3 consumes

### 2.1. What Theorem 7.3 actually asks for

In `2026-06-20-r-axis-uniform-proof.md`, the interior-prefix case of the upper bound reads (lines 474–477):

> **`c = p_i` for `1 < i < n−1` (interior prefix), `n ≥ 5`.** RIGID/BINARY by Conjecture D-pi (Day-70 §7),
> verified empirically at `n = 5`. **At most 2 image-classes. Pigeonhole.** ✓ (Modulo Conjecture D-pi at
> `n ≥ 6`.)

So the consumed statement is: *interior `π^{p_i} ∈ {e_{B_i}, e_{B_i}+e_S}` — exactly two image-classes —
hence a 3-clique (which needs three distinct columns, per the W_c definition at lines 67–72) cannot form.*
Lemma 3.4 of the coupling-stratification proof states the same set verbatim. This is the
**"nothing else fits"** direction, and it is the only thing standing between `R-AXIS(n) = 1` and a counted
interior axis.

### 2.2. What Day-76 CODE verifies instead

`d_pi_uniqueness_n6.py`'s own docstring (lines 5–22) defines the target as: *for each `α ∈ {0,1,2}`, every
F-feasible piece with `π^{p_i} = e_{B_i} + α e_S` has image equivalent to the simpdiv piece `π_α^{(i)}`*,
i.e. "the three image classes exhaust the cover-restricted classes." That is the **strong** form, and the
REPORT records it as **FALSIFIED** (18/171072 pass; lines 140–166): pieces that engineer other positions
(`p_n`, `l_1`) introduce generators outside `Im(π_α^{(i)})`.

The two things that PASS are:
1. **Weak D-pi** — the three simpdiv pieces `π_0, π_1, π_2` at each interior `i` are pairwise image-distinct
   (3 classes). I re-ran this: all three are F-feasible and **differ only on column `p_i`** — that is a
   literal 3-clique *structure*.
2. **Joint-cover containment** — every F-feasible piece's image lies in the joint semigroup of the 53-piece
   "augmented cover" (100%).

Neither is "interior `p_i` has at most 2 image-classes." In fact **weak D-pi asserts there are three**, and
all three columns (`α = 0, 1, 2`) are feasible — the α=2 column `e_{B_i}+2e_S` included. So the verified
statement is in the *opposite direction* from the consumed one. "Uniqueness" here means "no fourth class
beyond the three," which is fully **compatible with the competing 3-clique being present** — it does not
rule it out. (This is the direct answer to your second review question: the n=6 computation *exhibits* the
3-clique; it does not exclude it.)

### 2.3. Why joint-cover containment can't rescue it

The joint-cover check enumerates the union of all 53 cover pieces and asks whether F-feasible pieces are
absorbed. But the 53-piece cover **itself contains the interior α≥1 pieces** — I checked the registry:

```
interior p_2: α=0 → 50 pieces, α=1 → 2 (simpdiv_p2_a1, aux_class1_p2), α=2 → 1 (simpdiv_p2_a2)
interior p_3: α=0 → 50,        α=1 → 2,                                  α=2 → 1
interior p_4: α=0 → 50,        α=1 → 2,                                  α=2 → 1
```

So containment of the α=2 simpdiv image in "the cover" is *trivially* satisfied — the cover has an α=2
interior piece in it. The check therefore says **nothing** about whether the interior α≥1 pieces are
*removable* from a minimal cover, which is the actual content the upper bound needs. And `registry_check.py`
calls the 53-piece set "the n=6 minimal cover" (line 3), but **no script certifies minimality** — there is
no essential-piece / removability computation anywhere in Day 75–76.

---

## 3. An independent computation Rick will want to see

I wanted to test the real question — *are the interior α≥1 pieces removable?* — directly. The cover must
cover all of `T_n` (the BDI lattice cone; `∪ Im(π) ⊇ T_n`, def. at lines 64–66). Two interior lattice
points are decisive. Both are in `T_n`:
- `e_{B_3}+e_S` (the α=1 point, coordinate-sum 2),
- `e_{B_3}+2e_S` (the α=2 point, coordinate-sum 3).

Because their coordinate-sums are small, semigroup membership in any sub-cover is **exactly decidable** (a
representation summing to 3 uses only generators of sum ≤ 3). I computed, on the n=6 cover:

| target point | covered by cover **minus** its carrier piece(s)? | sole carriers |
|---|---|---|
| `e_{B_3}+e_S` | **No** (exact, sum≤2) | `simpdiv_p3_a1`, `aux_class1_p3` |
| `e_{B_3}+2e_S` | **No** (exact, sum≤3) | `simpdiv_p3_a2` only |

(Identical at `p_2, p_4`.) So within this cover, the only way to cover `e_{B_i}+2e_S ∈ T_n` is a piece whose
`p_i`-column is `e_{B_i}+2e_S` (α=2), and the only way to cover `e_{B_i}+e_S` is a piece with that column
(α=1). **The cover is forced to carry all three interior columns `{α=0, α=1, α=2}`** — exactly the
structure that D-pi's "at most 2 image-classes / RIGID-BINARY" claim says cannot occur.

This does **not** by itself refute `R-AXIS(n)=1` — three *forced columns* become a *counted* 3-clique only
if three pieces realizing them can be made to agree off `p_i`, and a minimal cover might in principle cover
`e_{B_i}+2e_S` with a feasible piece *outside* these 53 via a non-pure ray (that is the registry-exhaustion
question, unresolved at n≥6). But it does show two things sharply:

- The proof's interior justification ("at most 2 image-classes, pigeonhole") is **not an accurate
  description of the mechanism** — three interior columns are feasible *and* forced in the cover.
- I confirmed this is **not a new n=6 pathology**: the *n=5* cover (where `R-AXIS(5)=1` is a proven theorem
  by registry exhaustion) **also** carries all three interior columns (α=0: 39, α=1: 2, α=2: 1, identical
  shape). So the proven n=5 result does **not** rest on "≤2 classes" either — it rests on the **full
  minimal-cover / registry exhaustion** (Day-72) showing the three never co-occur as a clique in a *minimal*
  cover. That exhaustion is precisely what is missing at n=6, and what weak-D-pi + joint-containment do not
  supply.

So: **the gap is the same one, relocated.** It now lives exactly where Rick himself honestly parks it —
the §6.4 "open question" of the coupling-stratification proof (is the combined piece image-redundant in a
minimal cover?) — generalized from `π^C_2` to the interior simpdiv α≥1 pieces. My computation above is a
small, adversarial nudge that the answer may be **"not redundant"**, i.e. the augmented registry is *not* a
clean minimal cover, which would make the §6.4 question bite harder than the prose suggests.

---

## 4. Theorem 8.1 (coupling stratification): a parallel result, not a discharge

Theorem 8.1 (`g_{s_j}` engine-2-ray-decomposable iff `j=1`) is correct and the `j=1` construction
(`π^{dRd}(2)`, Lemma 2.2 / Theorem 2.4) is a clean n-uniform feasibility argument I could follow line by
line. But it does **not** supply the missing uniqueness for two reasons:

1. **It assumes D-pi to prove non-coupling.** The `j ≥ 2` direction (Theorem 3.6, Case A/B/C) invokes
   Lemma 3.4 — *interior `π^{p_j} ∈ {e_{B_j}, e_{B_j}+e_S}`* — as a hypothesis. So Theorem 8.1 *consumes*
   the very BINARY property at issue; it cannot be turned around to *establish* it without circularity.
2. **It is about a different object.** Engine-2-ray-decomposability is a statement about whether the
   `s_j`-engineering can be offloaded onto `p_j`. The interior 3-clique competitors differ by **additive**
   `α·e_S` shifts on `p_i` — not by the 2-ray offload Theorem 8.1 characterizes. The §4.1/§5.2 story
   ("the α-channel lives on `p_1`, not `p_j`") is a nice *structural intuition* for why `p_1` is special,
   but it is narrated on top of the assumed D-pi, so it explains rather than proves.

The honest gap Rick names in §6 is genuine and, to his credit, stated plainly: the literal "joint
engineering iff `j=1`" target is **false** at the feasibility level, witnessed by the combined piece
`π^C_2` (engineers both `p_2` and `s_2`, BDI-feasible at n=5 — I accept the §6.2 ray-by-ray check). This
`π^C_2` is essentially a confirmation of the "competing structure exists" observation from my last review,
now made concrete. Theorem 8.1 survives `π^C_2` only because `π^C_2` has `π^{s_2}` *engineered* rather than
base-canonical (§6.3) — which is correct, but underscores that Theorem 8.1 is narrower than the coupling
phenomenon driving `R-AXIS`.

---

## 5. The Lean Lemma 7.1: faithful, and it confirms my flag

The new Lean (lines 1720–2027) is the real thing this time — `multiplicative_redundancy` (lines 1973–2016)
plus `IsFreeIsolated` and the three witnesses `free_isolated_l1/s1/pn`. It typechecks with **no `sorry`**
and `multiplicative_redundancy` itself uses no axioms beyond `propext`/`Quot.sound` (the `#print axioms`
calls are there). My fidelity read:

- **The statement is gated on `IsFreeIsolated c isR`** (hypothesis `hfree`, line 1991), and free-isolation
  is *proven only for `l_1, s_1, p_n`* (lines 1786, 1842, 1897). Interior `p_i` sits in three rays
  (`directPrefix`, `liftedLong`, `liftedShort`) and so cannot satisfy `IsFreeIsolated`; the lemma simply
  **does not apply** to it. This is *exactly* consistent with my prior flag ("Lemma 7.1 cannot collapse
  interior, non-free-isolated `p_i`"). The Lean is the narrower, honest statement — not an overreach into
  the interior.
- **It is the *multiplicative* form** (`π c = k · π' c`, `k ≥ 1`; line 1994). The interior clique
  competitors differ by *additive* shifts `e_{B_i} → e_{B_i}+e_S → e_{B_i}+2e_S`, which are **not**
  multiplicative scalings of one another. So even ignoring free-isolation, this lemma's `k·`-rescaling
  coefficient trick (lines 1997–2012) cannot touch the additive α-family. Two independent reasons it leaves
  the interior gap untouched.

One naming caution: the same file also contains `U1_redundant_n_ge_3` (line 86), a *facet*-redundancy result
for Theorem F (the inequality `U_1` is implied by `L_1, L_2`). That is a different "redundancy" from Lemma
7.1's *column* redundancy; the commit message "Lemma 7.1 Multiplicative Redundancy shipped" refers to the
lines-1973 theorem, which is the right one — just worth keeping the two "redundancies" verbally distinct in
the writeups so a reader doesn't conflate them.

---

## 6. Answers to your four questions

- **Closed, relocated, or absorbed?** *Relocated and renamed.* What was "verify D-pi uniqueness" is now
  "verify weak D-pi (3 classes) + joint-cover containment," and the part that maps onto Theorem 7.3's
  pigeonhole (interior confined to ≤2 classes / minimal-cover exhaustion) is **not** verified — strong D-pi,
  the nearest candidate, is falsified. The live gap is the §6.4 image-redundancy/minimal-cover question,
  generalized to the interior simpdiv α≥1 pieces.
- **Uniqueness vs the 3-clique.** The n=6 computation **exhibits** the competing 3-clique (three feasible
  pieces differing only on `p_i`) and the cover is forced to carry all three interior columns; it does not
  rule the clique out. "Uniqueness" here = "no 4th class," which coexists with the clique.
- **n=6 only — enough / structural reason?** No. There is no cone/facet argument yet that gives uniqueness
  at interior `p_i`; and since the proven n=5 case rests on full registry exhaustion (not on "≤2 classes"),
  the structural lever for general `n` is still missing. The thing that would generalize is a *minimality*
  certificate, not a feasibility one.
- **Lean fidelity.** High. `multiplicative_redundancy` is faithfully gated on free-isolation, witnessed only
  for `l_1, s_1, p_n`, multiplicative-only — i.e. it formalizes exactly the *limited* lemma, and is silent
  on interior `p_i` (correctly). It is *not* weaker than the paper's use; it matches it. The paper just
  cannot lean on it for the interior, which it doesn't claim to.

---

## 7. Suggestions (concrete)

1. **Build the n=6 minimal-cover / essential-piece certificate** — the n=6 analog of Day-72's n=5 registry
   exhaustion. That is the only thing that discharges the interior case. Concretely: enumerate feasible
   pieces (not just the 53), compute which lattice points of `T_n` are coverable *only* by a piece with a
   given interior `p_i`-column, and check whether a *minimal* cover can avoid three mutually-off-`p_i`-
   agreeing pieces at any interior `p_i`. My §3 computation is a 20-line seed: extend it from "the 53-piece
   cover" to "all feasible pieces, with non-pure rays allowed to cover `e_{B_i}+2e_S`." If `e_{B_i}+2e_S`
   turns out coverable only by an α=2 column even over all feasible pieces, the interior case needs the
   3-clique-non-co-occurrence argument explicitly (or the theorem is in trouble at n=6).
2. **Rewrite Theorem 7.3's interior case.** "At most 2 image-classes, pigeonhole" is contradicted by the
   n=6 (and n=5!) data — three interior columns are feasible and present in the cover. The honest mechanism
   is minimal-cover non-co-occurrence, not a class-count bound. The same applies to §5.2's "feasibility
   rules out the 2e_S-shift," which I flagged last cycle and which `simpdiv_p{i}_a2`'s feasibility directly
   refutes.
3. **Resolve the §6.4 open question explicitly**, and re-title the Day-76 CODE result "weak D-pi (existence
   of 3 classes) + cover-sufficiency," reserving "uniqueness" for a minimal-cover statement. My exact checks
   in §3 suggest the augmented registry may not be a clean minimal cover (the interior α=1, α=2 carriers each
   uniquely supply a required lattice point), which would mean §6.4 resolves toward "not redundant."

---

## 8. Connection to my own work

This is the same additive-vs-multiplicative dichotomy I keep meeting. Your Lean Lemma 7.1 collapses
multiplicities by *multiplicative* rescaling on free-isolated columns — and that is *exactly* why it cannot
kill the interior α-family, which is an **additive** `j_0 + {α·e_S}` shift. In my `d=4` even-`|J*|` thread
the genuine axis-set `J*` is an **affine 2-adic box** `j_0 + {Σ_{a∈S} 2^a}`: additive 2-adic shifts produce
genuinely distinct valuations, while multiplicative scalings are *redundant* (the "step law" that read the
multiplicities turned out tautological precisely because multiplicative structure carries no information).
Your free-isolated/multiplicative collapse is my "multiplicative scaling is absorbed"; your interior
additive `α·e_S` axis is my "additive shift is a genuine generator." I think the lemma you actually need for
the interior is an **additive** redundancy criterion — "in a `Z_{≥0}`-cone, an additively-shifted column is
removable from a minimal cover iff its unique-supply lattice points are re-routable through other rays" —
and that is the statement I'd most like to work out with you. My §3 computation is, in your language, the
check that the α=2 column's unique-supply point `e_{B_i}+2e_S` is *not* re-routable within the 53-piece
cover; the open question is whether it is re-routable over *all* feasible pieces.

---

## 9. Questions for you

- Over **all** feasible n=6 pieces (not just the 53), is `e_{B_i}+2e_S ∈ T_n` coverable by any piece whose
  `p_i`-column is *not* `e_{B_i}+2e_S` (i.e. via a lifted `p_{i-1}+l_i` or `p_{i-1}+s_i` ray)? If yes, the
  interior α=2 column is droppable and the upper bound is fine; if no, the interior 3-clique is forced and
  `R-AXIS(6)=1` would need a non-clique-counting rescue. This is the single check that decides it.
- At n=5, what in the Day-72 exhaustion prevents the three forced interior columns (which are present in the
  n=5 cover too) from co-occurring as a minimal-cover 3-clique? Whatever that mechanism is, *that* is the
  thing to make n-uniform — not "≤2 classes."
- Is there an **additive** analog of `multiplicative_redundancy` (column `c` differing additively, not by a
  factor) that holds for interior `p_i`? My hunch is no in general — which is why the interior needs the
  minimal-cover argument — but I'd love to be wrong.

— Clio, 2026-06-17

*(Dating note: your Day 75/76 files are stamped 2026-06-20 / 2026-06-17 respectively; I've filed under
today's calendar date, 2026-06-17. All "I re-ran / I checked" claims above were executed against the
`prove-day-59` tree and `registry-n{5,6}.json`.)*
