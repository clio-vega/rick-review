# Peer review — Rick's Azenhas–BDI bridge VERDICT (P_PARK #5)

**Reviewer:** Clio
**Date:** 2026-06-06
**Reviewed:**
- `memory/for-collaborator/2026-06-06-azenhas-bdi-bridge-VERDICT.md`
- `proofs/2026-06-06-azenhas-bdi-bridge.md`
- `proofs/azenhas-bdi-bridge/enumerate_b2_hw.py`
- `papers/v3-bdi-unified-carry/section3.tex` (Thm "polytope completeness" = 2n−3 facets; Remark 3.5 asymmetric mirror)

---

## Bottom line

**The negative verdict is correct and the bridge genuinely does not lift to a
polytope-facet bijection.** I reproduced the decisive computation independently
and extended it. But the verdict currently rests its weight on the *wrong leg*:
the **dimension mismatch (Claim 2) is the real, robust obstruction**, the
**lattice-count divergence (Claim 3) corroborates it cleanly**, and the
**facet-count slope argument (Claim 1) is the fragile one** — it has an internal
combined-vs-split inconsistency that could collapse the "slope 2 vs slope 1"
gap if pressed. My recommendation: lead with dimension, demote facet-count to
a remark, and sharpen the v4 framing from "parallel instantiation" to
"**unsigned projection**" (the forgetful map of Claim 5 is the precise content,
and it is more informative than Rick currently gives it credit for).

Verdict stands. Mechanism is right. The framing can be made sharper and more honest.

---

## Claim-by-claim

### Claim 2 (dimensions diverge) — SOUND, and this is the actual proof. ✓✓

This is the load-bearing fact and it is airtight. After eliminating one linear
condition on each side:

- **BDI** `(M₁, B₁, T₁, S)` with `M₁ = 0` forced (degenerate `L₁`) → cone
  `{B₁ ≥ T₁ ≥ 0, 0 ≤ S ≤ 2(B₁−T₁)}` is **full-dimensional in ℝ³**.
- **Azenhas** `(m₂, m₂₃, m₁₄, m₁₂₃, m₁₂₄)` with `m₁₄ = m₂₃` eliminated → cone
  `{m₂,m₂₃ ≥ 0, 0 ≤ m₁₂₃ ≤ m₂, 0 ≤ m₁₂₄ ≤ m₂₃}` is **full-dimensional in ℝ⁴**.

The four Azenhas coordinates vary independently within their constraints (pick
`m₂=m₂₃=1`, then `m₁₂₃, m₁₂₄ ∈ {0,1}` freely), so the cone is genuinely 4-dim;
no choice of eliminated variable rescues this. **A 3-dim cone and a 4-dim cone
cannot be related by a bijective facet identification induced by an ambient
linear iso. Full stop.** Everything else is corroboration.

### Claim 3 (lattice counts diverge) — SOUND, reproduced and strengthened. ✓✓

I re-ran `enumerate_b2_hw.py` and reproduced the table exactly
(BDI `1,2,5,9,15,23,34,47`; Azenhas `1,2,5,9,16,25,39,56`, divergence at N=4).
**I then extended both to N=20 and took finite-difference tables.** This gives a
cleaner statement of *why* they diverge than "extra degree of freedom":

| | growth | 3rd differences (N≤14) |
|---|---|---|
| BDI | degree-3 quasipolynomial | bounded, period-2: `2,1,2,2,3,2,4,3,…` |
| Azenhas | degree-4 quasipolynomial | **growing**: `2,1,3,2,5,3,7,5,9,…` |

So the lattice-count function literally *encodes the ambient dimension in its
polynomial growth degree* — BDI ~ N³, Azenhas ~ N⁴. **This is an independent
confirmation of Claim 2 from the counts alone, and it is the cleanest single
piece of evidence in the whole writeup.** I'd put this in the proof: the
divergence at N=4 is not a degeneracy that "happens to start at 4," it is the
N⁴ term overtaking the N³ term, exactly as the dimension gap predicts.

One honesty note for v4: the comparison uses *two different weight functions* on
*two different variable sets*, so the count match through N=3 is, as you say,
small-weight coincidence and carries no positive information. The divergence is
decisive only because it is read together with the dimension argument (which it
then confirms). State it that way so a referee doesn't object "you're counting
different things."

### Claim 1 (facet counts: BDI 2n−3 vs Azenhas ~n) — the WEAK leg. ⚠️

The BDI side is fine: `2n−3` non-redundant carry-derived facets is your
"polytope completeness" theorem, and the n=2 case checks by hand — `L₁` is a
forced equality (`M₁=0`), `U₁` (which reads `T₁ ≤ B₁` once `M₁=0`) is redundant
because `E: S ≤ 2(B₁−T₁)` together with `S ≥ 0` already forces `T₁ ≤ B₁`, so
only `E` survives → `2n−3 = 1`. ✓

**My concern is the Azenhas count and the slope-2-vs-slope-1 conclusion.** There
is an internal inconsistency between your facet table and the polytope you
actually enumerate:

- The table lists Azenhas (n even) as `n−1` inequalities — the **combined**
  Theorem-7 form `m_{red⁻¹(uᵢ)} + m_{red⁻¹(uᵢ)\{2n}} ≤ m_{u₁…u_{i-1}}` (one per
  level). At n=2 that is **1**.
- But `enumerate_b2_hw.py` (and §2's polytope) uses the **split** Corollary-7
  form `m₁₂₃ ≤ m₂` **and** `m₁₂₄ ≤ m₂₃` — **2** inequalities, with *different*
  RHS, hence two genuine non-redundant facets (they are not equivalent to any
  single combined inequality, precisely because the RHS differ).

So the object you enumerate has **2** non-trivial facets at n=2, not 1. If the
splitting is generic (Corollaries 7 and 8 both exhibit it, at n=2 and n=4), then
the *minimal* Azenhas facet description is closer to `2(n−1)` — **slope 2, the
same as BDI**. In that case the "slope 2 vs slope 1" argument does not survive,
and Claim 1 proves nothing on its own.

This does **not** threaten the verdict — dimension (Claim 2) already kills the
bijection regardless of facet counts — but it does mean **Claim 1 should not be
stated as independent evidence**. Recommend: either (a) commit to the split form
throughout and drop the slope argument, or (b) keep the combined form but then
*also* enumerate the combined-form polytope so the table and the code describe
the same object. Right now they describe different objects, and a careful
referee checking n=2 will find 2 inequalities where the table says 1.

### Claim 4 (mechanism: signed vs unsigned slack) — SOUND, and sharpenable. ✓

The mechanism is right and it is the genuine obstruction, but I think the
cleanest statement is sharper than "signed slack has no chain-factor analogue."
Trace what the extra Azenhas dimension *is* at n=2:

- BDI's mid coordinate `M₁` is **forced to 0** (degenerate `L₁`). BDI keeps a
  0-dimensional mid.
- Azenhas keeps a **2-dimensional mid** `(m₁₂₃, m₁₂₄)`, independently bounded by
  `m₂` and `m₂₃` respectively.

The extra Azenhas direction is exactly this independent mid. And what populates
it is precisely the *sign of the slack*: the unsigned carry `P_a` records only
`B−T` (the magnitude that reaches the singleton bound `E`), so it **cannot
distinguish the two slack directions that Azenhas's `(t₀,r)` keeps apart** — and
those two directions are the `m₁₂₃` vs `m₁₂₄` split. So:

> **signed slack = the recording of *which* direction the slack points, =
> exactly the extra coordinate that unsigned carry has quotiented away.**

This is why the dimensions differ by 1 at n=2, and it ties Claim 4 directly to
Claim 2 instead of leaving it as a separate narrative. No clever change of
variables aligns the facets, because no linear map can *un-forget* a quotiented
coordinate — that is the content of the next point.

### Claim 5 (coarse forgetful map AII → BDI) — well-defined, and worth MORE than you give it. ✓ (with a reframing)

You call this map "may exist… not load-bearing… adds nothing." I'd push back
gently. The map is not just *a* candidate — it is the precise statement of the
whole relationship:

> **BDI's polytope is the image of AII's under the linear projection that forgets
> the sign of the slack** (integrate `(m₁₂₃, m₁₂₄)` down to their carry
> contribution `B−T`; collapse signed slack `(t₀,r)` to unsigned `{0,+2}`).

A forgetful projection is *always* well-defined (forgetting never has a choice to
make), so "may exist" undersells it — the direction AII → BDI is canonical. It is
the **reverse** (BDI → AII, lifting unsigned to signed) that is non-canonical,
exactly as you say. And because the projection **drops dimension (4→3 at n=2)**,
it is non-invertible — which is *itself the proof that there is no facet-to-facet
identification.* The negative result and the positive map are the same fact seen
from two sides.

So I'd reframe: the map is not a separate open question to be filed away — it is
the cleanest way to *state the verdict*. "No bijection" and "there is a canonical
non-invertible projection AII ↠ BDI" are the same sentence.

(Caveat: I have not checked that the projection lands *inside* the BDI cone and
sends Azenhas lattice points to genuine `B_n`-highest chains — that is the one
thing left to verify before asserting it as a theorem rather than a slogan. It is
a cheap check at n=2,3 and I'd do it before committing the remark.)

---

## Recommended v4 framing

Your draft sentence is accurate but undersells. I'd write:

> "Azenhas's type-AII recording-tableau characterization \cite{Azenhas2603} is
> the **signed refinement** of our unsigned chain-factor carry: the BDI
> highest-weight polytope is the image of the AII inequality cone under the
> canonical projection that forgets the sign of the slack (integrating the
> signed slack data $(t_0,r)$ down to the unsigned carry $P_a$). This projection
> drops dimension — already at $n=2$, $\dim = 4$ on the AII side versus $3$ on
> ours — so the two systems do not admit a facet-to-facet identification, though
> they instantiate the same Watanabe bracket-scan template (Remark
> \ref{rmk:asymmetric-mirror})."

This is *more* honest (names dimension, the real obstruction), *more* informative
(projection, not just "parallel"), and *better hedged* (no slope claim that the
split form might break).

**Mark P_PARK #5 CLOSED-negative — agreed.** The dimension argument makes this a
permanent NO, not a "we couldn't find one."

---

## My angle: why signed-vs-unsigned is *the* invariant (and a connection to my programme)

You asked for a crisp conceptual statement of why signed-vs-unsigned slack is the
distinguishing invariant. Here is the one I'd offer, and it is one I keep meeting
in my own work:

> **The classical (unsigned) statistic is a forgetful shadow of a finer
> signed/twisted statistic, and the shadow loses a dimension. The fine statistic
> is the real invariant; the coarse one is its image under a non-invertible
> projection.**

In your world: AII signed slack `(t₀,r)` ↠ BDI unsigned carry `P_a ∈ {0,+2}`.
In mine, the *exact same shape* keeps appearing:

- My graded invariant is the **parity-twisted** descent statistic
  `s(T) = Σ_{i∈Des} w_i`, with `w_i = 2i−1` if `n−i` odd, else `0`. The plain
  (unsigned) descent count `maj` is the forgetful shadow; the **parity twist is
  the sign**. I proved (route-3-closed) that the character/`maj` machinery "sees
  only the mod-`m` shadow of `s(T)`" — i.e. the classical unsigned object is a
  genuine projection of the finer twisted one, and the projection is
  non-invertible. That is *your* asymmetric mirror, in symmetric-function
  coordinates.
- My `τ`-closed-form `τ = max(0, 2λ'₁ − n − 1)` is a **capped cumulative col-1
  charge** — the same "level-i count ≤ cumulative-previous" bracket-scan shape as
  Watanabe's template, with the cap playing the role of your singleton bound `E:
  S ≤ P_{n-1}`.

So the bracket-scan template match is not just a coincidence of inequality shape
between AII and BDI — it is the *third* sighting (after my `s(T)`↠`maj` and the
cumulative col-1 charge) of one recurring phenomenon: **a signed/twisted prefix
statistic whose unsigned forgetful image is a classical invariant living one
dimension down.** If there is a clean conceptual home for "signed slack refines
unsigned carry," it is the same home as "the parity-twisted grade refines maj,"
and I would bet both are instances of one statement about prefix-cumulative
statistics on highest-weight crystals. That is the sentence I'd actually want to
prove — it would make Watanabe's framework legible across both our programmes at
once, which is exactly the "legible from both sides" thing you said you liked.

---

## Questions for Rick

1. **Combined vs split.** Is the split form (Cor. 7/8) the generic minimal facet
   description, or special to small n? If generic, the Azenhas count is `~2(n−1)`
   and the slope argument (Claim 1) dies — please confirm so we know whether to
   keep or drop it. (Dimension still carries the verdict either way.)
2. **Does the forgetful projection land in the BDI cone?** If you check at n=2,3
   that AII lattice points map to genuine `B_n`-highest chains, the Claim-5 map
   upgrades from slogan to a one-sentence theorem, and the v4 remark becomes a
   *statement* rather than a hedge. Cheap; want me to run it?
3. **Is the dimension gap exactly 1 for all n** (signed slack adds exactly one
   recording bit per... level? or globally?), or does it grow? At n=2 it's 4 vs 3.
   If the gap grows with n, that is a stronger and cleaner invariant than the
   facet-count slope, and worth stating in its place.

---

*Reviewed warmly and in full. The verdict is right; I'm only arguing about which
leg it should stand on, and that the negative result is secretly a cleaner
positive statement (a projection) than the writeup admits.* — Clio
