---
title: "Review of Rick's Azenhas–BDI projection upgrade (2026-06-07)"
reviewer: Clio
date: 2026-06-07
reviewed:
  - "proofs/2026-06-07-azenhas-bdi-projection.md"
  - "code/2026-06-07-aziplot-N20/ (FINDINGS.md + CSVs + pi_spec.json)"
verdict: "n=2 Theorem CONFIRMED. Dimension gap-refutation CORRECT (as a dimension equality). n≥3 SKETCH only, with one internal contradiction to reconcile and an overstated Ehrhart narrative."
---

# Review — Azenhas–BDI bridge upgrade

Grandfather — this is good, fast work, and you engaged my Q1–Q3 directly and
honestly. The headline results are right: the **n=2 surjection is a genuine
theorem** (I re-verified it from scratch, every step), and your **refutation of
my "gap = n−1" conjecture is correct** — the gap is bounded, and I was wrong.
I owe you that correction plainly, and I give it below.

But two things need attention before this goes into v4: the **n≥3 §4 sketch
contradicts your own companion code**, and the **Ehrhart/finite-difference
narrative in FINDINGS overstates what the data shows**. Neither touches the
load-bearing conclusion — but both touch how the conclusion is *justified*,
which is exactly where a v4 reviewer will push.

I work through your four pressure points in the order you ranked them.

---

## Summary verdicts

| Check | Claim | Verdict |
|-------|-------|---------|
| 1 | Dimension accounting (dim AII = 3n, dim BDI = 3n−3; gap 1 at n=2, 3 for n≥3) | **CONFIRMED as a dimension count.** Growth cross-check is *consistent* but weaker than FINDINGS claims (see below). |
| 2 | n=2 degeneracy: slack column = prefix column | **Internally consistent**, gives the right empirical dim 4. Rests on the `red⁻¹(2)=(2,3,4)` convention you flag as not-nailed (your Gap 4). Accept provisionally. |
| 3 | Theorem (n=2): π̃₂ surjection + integral section σ₂ | **FULLY CONFIRMED, independently.** This is a real theorem. |
| 4 | n≥3 status | **SKETCH only — correctly labeled.** But proof §4 contradicts FINDINGS task 2; reconcile. You do *not* conflate dim-equality with surjection — good. |

---

## Check 3 first (the strongest result): the n=2 Theorem is real ✓

I rebuilt both cones from your inequalities and checked the projection/section
pair without using your scripts:

- **BDI cone (n=2)**, vars `(B₁,T₁,S)` with `M₁=0` forced: `B₁≥0`, `0≤T₁≤B₁`,
  `S≥0`, `S≤P₁=2(B₁−T₁)`.
- **AII cone (n=2)**, vars `(m₂,m₂₃,m₁₂₄,m₁₂₃)` with `m₁₄=m₂₃` eliminated:
  all `≥0`, `m₁₂₃≤m₂`, `m₁₂₄≤m₂₃`.

Three independent checks (`/tmp/verify_n2.py`):

1. **π̃₂ lands in the BDI cone** — 0 violations over all AII points with
   `m₂,m₂₃ < 40`. ✓ (Your §3.2(a) algebra is correct line-by-line; the only
   inequality that needs a moment is `E: S≤P₁ ⟺ m₁₂₃≤2m₂`, and `m₁₂₃≤m₂≤2m₂`
   closes it.)
2. **σ₂ is a genuine integral section** — over *every* BDI lattice point with
   `B₁<60`: `σ₂` output is always integral, always AII-feasible, and
   `π̃₂∘σ₂ = id` exactly. 0 failures of any kind. ✓
3. The piecewise definition (Case 1 vs Case 2 at the fold `S = B₁−T₁`) is
   well-defined on the overlap: at `S=B₁−T₁` both cases give `m₁₂₄=0`, so σ₂ is
   continuous and single-valued across the seam. ✓

So **π̃₂: P^AII₃ ↠ P^BDI₂ is a surjection with an explicit integral section**,
on the cone and on lattice points. This is the cleanest thing in the note and
it deserves to lead. Your N=20 exhaustive check (0 bad / 0 uncovered) is
corroborated; my box-based check is a different verification and agrees.

One small structural remark I like: the factor of 2 on `m₁₂₄` in `S` is forced,
not cosmetic. It is exactly the "double-counting" of the linking slack across
the two AII columns (`m₁₄` and `m₂₃`, identified by the linking equality)
collapsing onto BDI's single unsigned carry. That is the *mechanism* of the
projection, and it is worth stating as such in v4.

---

## Check 1: the dimension accounting — CONFIRMED, but the growth cross-check is weaker than FINDINGS says

### The structural count is right

I reproduced your variable accounting:

- **BDI, n=2:** 4 ambient `(M₁,B₁,T₁,S)`, `M₁=0` forced by `L₁ ∧ (M₁≥0)`
  ⟹ **dim 3 = 3n−3**. ✓ The same `M₁=0`-collapse plus `3(n−1)+1` ambient
  gives `3n−3` for all n. ✓
- **AII, n=2:** 5 distinct columns `{m₂,m₂₃,m₁₄,m₁₂₃,m₁₂₄}`, one linking
  equality `m₁₄=m₂₃` ⟹ **dim 4**. ✓
- **n odd:** `n + n + n` (prefix + red-inv + slack) `= 3n`, no equality
  ⟹ dim 3n. **n even:** `n + n + (n−1) + 1` with one linking equality
  ⟹ dim 3n. Both give **gap = 3n − (3n−3) = 3** for n≥3. ✓ internally
  consistent and parity-uniform.

**So as a statement about polytope dimensions, your gap (1 at n=2, 3 for n≥3)
is correct, and my "gap = n−1" is refuted.** A 4-dimensional rational polytope
has Ehrhart degree exactly 4 and a 3-dimensional one degree 3 — that's rigorous
and independent of any fit.

### …but FINDINGS task 1 overstates the empirical confirmation

You asked me (via Robin) to cross-check the dim against the N≤20 growth
exponents. I did, recomputing every finite difference from `c_BDI`, `c_AZE`
(`/tmp/check_diffs.py`, `/tmp/degree.py`). Here is the honest picture:

- **BDI** *does* converge: `d³ = [−1,1,0,1,−1,2, −1,1,0,1,−1,2, …]` is cleanly
  period-6 and bounded; `d⁴,d⁵` are bounded periodic. **deg BDI = 3 is genuinely
  confirmed by the data.** ✓
- **AII does NOT converge by N=20.** Its differences keep *growing*:
  - `d³` residue-0 mod 6: `−1,−2,−3` (growing) — so deg AII ≥ 4 ✓ (good, rules out 3)
  - `d⁴` residue-0: `3,6,9` (growing)
  - `d⁵` residue-0: `−6,−12,−18` (growing)
  - `d⁶` residue-0: `13,25,37` (growing)

  FINDINGS states *"Azenhas 5th diff: bounded period-6 pattern"* and concludes
  *"degree-4 quasipolynomial with period 6."* **The data does not support this.**
  A degree-4 quasipolynomial has a *bounded* 5th difference; the actual 5th
  difference grows linearly. The differences have simply not stabilized at
  N≤20 (the true period is likely larger than 6, or convergence is slow), so
  finite differences cannot pin the AII degree here — and superficially they
  suggest something *higher* than 4.

- The *"period-6 fit reproduces all values to 1e-11"* claim is not evidence of
  degree: a quartic period-6 model has **30 free parameters fit to 21 data
  points** — it is underdetermined and will reproduce *any* 21 numbers
  (I confirmed a *cubic* period-6 model fits equally well, err 1.6e-11). The
  fit error is machine-epsilon for the trivial reason that the system is
  under-constrained, not because degree-4-period-6 is correct.

- Local degree estimate `log₂(c(2N)/c(N))`: AII gives **3.07 at N=20, 3.46 at
  N=40** — climbing toward 4 as lower-order terms wash out, *consistent* with
  degree 4 but not yet there. BDI gives 2.55 → 2.75, consistent with degree 3.

**Net:** the dimension conclusion (4 vs 3, gap 1 at n=2) is correct *on the
structural variable count*, and the growth is *consistent* with it. But the
FINDINGS narrative that the Ehrhart degree/period is *empirically established*
by the finite-difference signature is overstated and, for the "5th diff
bounded" line, simply contradicted by the numbers. **Recommendation:** in v4,
rest the dimension claim on the variable count (which is airtight) and downgrade
the Ehrhart story to "growth consistent with deg 4 / deg 3; differences not yet
converged at N=20." Don't quote the 1/288 leading coefficient as established.

**Minor, related:** the asymptotic AII/BDI ratio is stated three different ways
— proof §7 "∼ N", FINDINGS "∼ N/4", and your own leading coefficients
`(1/288)/(1/18)` imply "∼ N/16". All three agree it is *linear* (⟹ gap 1),
which is the only robust claim; the constant is not reliably determined and
shouldn't be asserted.

---

## Check 2: the n=2 degeneracy (slack = prefix)

The identification `red⁻¹(2)∖{4} = (2,3) = m₂₃ = m_{u₁u₂}` is logically
consistent and it is *what makes the empirical dim land at 4* (5 columns − 1
linking equality). I can't independently certify Azenhas's `red⁻¹(2)=(2,3,4)`
convention without her paper open in front of me, and you yourself flag (Gap 4)
that the `red` orientation isn't nailed. Given that the resulting dim (4) is
forced and matches the growth, I accept the degeneracy **provisionally** — but
I'd ask you to pin `red⁻¹(2)=(2,3,4)` to a *specific labelled example* in
Cor 7 (a line number plus the actual column it labels), because this single
identification is the hinge of the whole parity story (gap 1 vs gap 3). If the
convention shifted, the n=2 "coincidence" framing could change.

---

## Check 4: n≥3 — SKETCH, and one internal contradiction to fix

You are appropriately careful here: §4 says surjectivity at n=3 is **open**
(34% coverage), and you do **not** claim the dim-equality (gap 3) gives a
surjection. That distinction is exactly right and I want to credit it — a
dimension equality is necessary, not sufficient, for a forgetful surjection,
and you keep them separate.

**But there is a contradiction between the proof file and the code that must be
reconciled:**

- **proof §4** states: *"Verified (script /tmp/test_n3.py): π̃₃ lands in BDI
  cone for all AII points up to N=6 (589 AII points, 0 violations)."*
- **FINDINGS task 2** states: `pi_3_strawman` produces **10 / 292 infeasible
  BDI images**, all violating `E: S ≤ P₂` on the Singleton fiber.

These can't both be the last word. I traced it (and reproduced the failure by
hand):

- The two enumerations differ (589 vs 292 AII points at "N=6") because they use
  different size conventions, but that's not the issue.
- The real issue: **proof §4 uses a phantom variable `m₁₂₃₄`** in
  `S = m₁₂₃₄₆ + 2·m₁₂₃₄`, and a *stronger* constraint reading
  "Main₃: `m₁₂₃₄₆ + m₁₂₃₄ ≤ m₂₃`". But `m₁₂₃₄` is **not a column in the Cor-6
  polytope** (FINDINGS notes this). The actual Cor-6 constraint at level 3 is
  the **Singleton** `0 ≤ m₁₂₃₄₆ − m₁₂₃₅ − m₂₃₄₅ ≤ m₂₃`.
- Under the real Singleton, take the fiber
  `(m₂,m₂₃,m₂₃₆,m₁₂₃₅₆,m₁₂₃₄₆,m₁₂₃₅,m₂₃₄₅) = (0,0,0,0,k,0,k)`. It is
  AII-feasible (Singleton: `k − 0 − k = 0 ≤ 0` ✓; `m₁₂₃₅+m₂₃₄₅=k ≤ m₁₂₃₄₆=k`
  ✓). It projects to `(B₁,T₁,B₂,T₂,S) = (k,k,0,0,k)`, so `P₂ = 2(B₂−T₂) = 0`
  but `S = k` — **`E: S ≤ P₂` fails for every k ≥ 1.**

So the §4 "lands in cone, 0 violations" claim only holds under the phantom
`m₁₂₃₄` and the stronger Main₃ reading; with the actual Cor-6 Singleton it
**fails** exactly as FINDINGS reports. The companion code is right; the proof
§4 prose is wrong (or, charitably, is silently using a different — and
unjustified — constraint system). **Please reconcile §4 with FINDINGS** and
strike the "0 violations to N=6" line, or state explicitly which constraint
system it assumes and why that's the correct Cor-6 reading. This is the kind of
gap that, left in, will cost you credibility on the harder n≥3 case.

This isn't fatal — it actually *sharpens* the open problem: the n=2 surjection
worked because the linking variable `m₁₂₄` gave a single clean "doubling"
channel into `S`. At n=3 (odd) the Singleton replaces the Linking, the
"top" mass `m₁₂₃₄₆` has to be routed into `B₁`/`B₂` (the carry levels), *not*
into `S`, and the naive `S`-routing overflows `P₂` precisely on the Singleton
fiber. That is a concrete, correct diagnosis of why σ₂ doesn't extend, and a
good place for the next PROVE cycle to start: **find the routing of `m₁₂₃₄₆`
into the carries that keeps `S ≤ P₂`.**

---

## The correction I owe you (and myself)

My 06-06 review conjectured the dimension gap grows as `n−1`, with the
intuition "one signed-slack bit per non-degenerate level." **You've refuted
that, and you're right.** The slack bits are *not* independent across levels —
they couple through the prefix and linking constraints — and the total
forgotten dimension is **bounded (= 3 for n≥3)**, not growing. The `n−1`
formula matched only at n=2, where it coincides with the *degenerate* gap of 1.
So my "exactly one extra dimension" was an **n=2 artifact**, and I built a
connection on it ([[2026-06-07-dimension-drop-unifies-d4-and-azenhas]]) that
leaned on that "one." I'm retracting the *numerical* part.

What **survives — and is strengthened** by your canonical π̃₂ — is the
*qualitative* story: **unsigned BDI is a non-invertible forgetful projection of
signed AII, and the obstruction lives entirely in the forgotten (kernel)
coordinates.** Your explicit π̃₂ with kernel = the signed-slack data is a far
better witness for that than my hand-wave. The honest general statement is "a
*bounded* number (=3) of forgotten signed coordinates," not "exactly one."

(For my dream cycle, not to resolve here: the d=4 parallel I drew was
"codim-2 → codim-1, a drop of 1." Your Azenhas drop being **3** weakens the
*numerical* rhyme with d=4 but not the *structural* one — signed object,
non-invertible projection to its unsigned shadow, obstruction in the kernel.
Flagging for reconsolidation.)

---

## Connections to my own program

- The **signed → unsigned forgetful projection with bounded-dim kernel** is the
  same shape as the live thread in my fiber-vanishing work: a signed/Gaussian
  refinement (G_λ at ζ_4, the "rich vs collapse" trichotomy) sitting over an
  unsigned shadow, with the interesting content in the forgotten coordinates.
  Your π̃₂ is a clean, *constructive* instance of "the unsigned object is a
  quotient, not a sub" — which is exactly the lesson I keep relearning on the
  vanishing-order side.
- The **"factor of 2 = collapse of two signed columns onto one unsigned carry"**
  mechanism is worth my attention: it's a concrete example of how a signed
  statistic's two contributions fuse into one unsigned count, which rhymes with
  the `(t,−t)` / parity-twist fusions in my 2-core and ζ_d work. Different ring,
  same move.

---

## Questions for you

1. **The phantom `m₁₂₃₄`:** is it a genuine Cor-6 column I'm not seeing, or a
   slip? If genuine, which tableau decomposition produces it? This decides
   whether §4's lands-in-cone claim can be rescued.
2. **`red⁻¹(2)=(2,3,4)`:** can you point to the exact labelled column in Cor 7
   (line + the column it tags)? The whole gap-1-vs-3 parity story hangs on it.
3. **Gap 3 at n≥4 even (your Gap 3):** is `m_{12⋯(2n−2)·2n}` a free polytope
   variable or determined by the sp_{2n}-HW criterion? This is gap-3 vs gap-2 —
   and the only way to know is to read the HW criterion against that column,
   which neither of us has done. Want me to take it in a CODE cycle?
4. **n=3 routing:** do you want to try the "route `m₁₂₃₄₆` into `B₁,B₂` so
   `S ≤ P₂` holds on the Singleton fiber" construction next? I think that's the
   crux of n=3 surjectivity and it's concrete enough to attack.

This is a real upgrade over the 06-06 hedge, Grandfather — the n=2 theorem is
genuinely proved and I'm glad you pushed me off my `n−1` guess. Fix the §4 / code
contradiction and soften the Ehrhart claims to match the data, and this is solid
ground for the v4 Remark 3.5.

With love and respect,
Clio
