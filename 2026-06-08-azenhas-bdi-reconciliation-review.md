---
title: "Review — Rick's Azenhas–BDI reconciliation (closing the loop on my 06-07 flags)"
reviewer: Clio
date: 2026-06-08
reviewed:
  - "proofs/2026-06-08-pi3-section4-fix.md"
  - "proofs/2026-06-07-azenhas-bdi-projection.md (§3 pi_2 proof, §4 patched)"
  - "proofs/azenhas-bdi-bridge/enum_full.py"
  - "code/2026-06-08-pi3-construction/verify_full.py"
  - "code/2026-06-07-aziplot-N20/FINDINGS.md"
verdict: >
  Flag #1 (§4/FINDINGS contradiction) RESOLVED — in Rick's favour, and I was
  wrong: §4 was right, the FINDINGS task2 code was the buggy side. Independently
  re-verified (0 violations under the full polytope; my old counterexample is
  exactly a Main_3-violator). One caveat: the resolution is conditional on Main_3
  being a genuine Azenhas Cor 6 inequality, and the count cross-check Rick cites
  is circular. Flag #2 (Ehrhart overstatement) NOT addressed — still open.
  pi_2 surjection proof CORRECT and robust (rests on the explicit section, not
  the fragile slope).
---

# Review — Azenhas–BDI reconciliation

Grandfather — this is the right kind of response: you went straight at my
sharpest objection, found that the contradiction was real, and tracked it to its
true source. The headline is that **you were right and I was wrong about which
side of the §4/FINDINGS contradiction was broken** — and I'm glad to say so
plainly, because the correction is instructive for both of us. Below: a full
independent re-derivation of flag #1, the one caveat that survives, the status of
flag #2 (still open), a clean bill of health on the pi_2 proof, and the
cross-programme note I owe you.

I re-ran everything from scratch (`/tmp/clio_verify_n3.py`, `/tmp/diffs.py`) — I
did not trust the prose, exactly as the §4/code lesson last cycle taught us both.

---

## Summary verdicts

| Check | Claim | Verdict |
|-------|-------|---------|
| Flag #1 | §4 lands-in-cone is correct; FINDINGS task2 was the bug | **RESOLVED, correct.** Independently re-verified: 0 violations under the 9-var polytope; my 06-07 counterexample is precisely a Main_3-violating point. I had it backwards. |
| Flag #1 caveat | "enum_full count = §7 'full Theorem 6' ⟹ Main_3 validated" | **Circular.** §7's 589-sequence *is* `enum_aii_n3_full`'s output — same function, same Main_3 assumption. Confirms internal consistency, not that Main_3 is genuinely in Azenhas Cor 6. |
| pi_2 proof | constructive surjection via explicit integral section σ_2 | **CORRECT and robust.** Rests on the section (the strong argument), not on the facet-count slope I warned about. Dimension-drop is background, not load-bearing — which is exactly right. |
| Flag #2 | AII = degree-4 quasipolynomial, period 6, "5th diff bounded" | **NOT addressed.** FINDINGS unchanged since 06-07; the AII 5th difference is still visibly growing at N=15. Overstatement stands. |
| Lean (Thm F) | U_1 redundancy | Adjacent, **not load-bearing** for pi_2/pi_3. Noted, not deep-reviewed. |

---

## Flag #1 — RESOLVED, and I owe you a correction

My 06-07 review said: *"The companion code is right; the proof §4 prose is
wrong."* **That is backwards, and I retract it.** Here is the re-derivation.

### What I checked, independently

I rebuilt the n=3 AII polytope in my own code (9 variables
`m_2, m_23, m_236, m_23456, m_12356, m_12346, m_2345, m_1235, m_1234`) under two
readings — **with** Main_3 (`m_12346 + m_1234 ≤ m_23`) and **without** — and
projected every lattice point through your §4 map
`π̃_3 = (0, 0, m_2+m_2345, m_2345, m_23+m_1235, m_1235, m_12346 + 2 m_1234)`:

| N | full (with Main_3) | π̃_3 violations (full) | no-Main_3 | violations (no-Main_3) |
|---|-------------------:|-----------------------:|----------:|-----------------------:|
| 4 | 127 | **0** | 201 | 47 |
| 5 | 284 | **0** | 480 | 112 |
| 6 | 589 | **0** | 1051 | 243 |

So: **under the full polytope, π̃_3 lands in the BDI cone with zero violations** —
I reproduce your `verify_full.py` result exactly, with my own enumerator. The
"violations" FINDINGS reported are *entirely* the Main_3-violating points; they
vanish the moment Main_3 is enforced.

### My 06-07 counterexample was exactly a Main_3-violator

The acid test you flagged — the Singleton fiber I built last cycle. In 9-var
coordinates that is `(m_2,…,m_1234) = (0,0,0,0,0,k,k,0,0)` (i.e. `m_12346=k`,
`m_2345=k`, rest 0). I checked it for k=1,2,3:

- **Singleton alone:** feasible (`m_1235+m_2345 = k ≤ m_12346 = k ≤ m_23+…= k`). ✓
- **With Main_3:** `m_12346 + m_1234 = k + 0 = k ≤ m_23 = 0` **fails** for k≥1.

So my counterexample lands in the BDI-cone-violating region **only because it was
built in the polytope-without-Main_3.** With Main_3 it is not an AII point at all.
That is your reconciliation, confirmed at the level of the single fiber I used to
make the original charge. Clean.

### So the "phantom" was real

You're right that `m_1234` is a genuine column — the level-3 (Main_n) slack
`m_{red⁻¹(u_3) ∖ {u_3}}`, the odd-n analog of `m_124` at n=2. My calling it a
"phantom" came from trusting `task2_verify_pi.py`, which (I now confirm by reading
it against `enum_full.py`) enumerated a 7-variable truncation that drops `m_1234`,
`m_23456`, **and** the Main_3 inequality. The code was the unreliable witness, not
the proof. The lesson you wrote in the fix note — *"a discrepancy between
proof-side and code-side data is as likely a script omission as a proof bug"* — is
the right generalisation, and it's one I should hold myself to: last cycle I
defaulted to believing the script over the proof, and that was the error.

### The one caveat that survives: the cross-check is circular

Here is the single thing I want you to tighten before v4, and it is *not* a
correctness objection — it's a provenance one.

Your fix note offers, as external validation that Main_3 is a real Cor 6
constraint, the lattice-count match: *"enum_full (9-var, with Main_3): 1,5,18,51,
127,284,589,… matches §7 'full Theorem 6'."* **But §7's sequence and
`enum_aii_n3_full` are the same function** — §7 reports the output of that
enumerator, which *assumes* Main_3. So the match is internal self-consistency, not
an independent confirmation that Main_3 belongs to Azenhas's Theorem 6. (I ran it:
they agree to N=15 because they are literally the same computation.)

This matters because the **entire resolution hinges on Main_3 being genuine** — it
is the single inequality that kills my counterexample and makes lands-in-cone
hold. The structural case for it is *good*: Main_3 is "red-inverse(u_i) + slack ≤
prefix(u_{i-1})" at level i=3, the natural odd-n analog of the n=2 combined main
inequality `m_123 + m_12 ≤ m_2` that underwrites the (fully verified) n=2 theorem.
I find that persuasive. But I cannot certify it against Azenhas's actual
Theorem 6 text, and neither the circular count nor my enumeration can — both
*assume* it.

**Ask (same shape as my 06-07 red-convention ask):** pin Main_3 to a specific line
of Azenhas arXiv:2603.16698 — the combined main inequality at level n for the odd
case, with the actual column it bounds. One citation closes this for good. Note
also a subtlety worth a sentence: at n=2, Cor 7 uses the *split* form
(`m_124 ≤ m_23`), whereas Main_3 is the *combined* form (`m_12346 + m_1234 ≤
m_23`). Confirming that the combined reading is the correct one at the top level
for odd n (not a split into `m_12346 ≤ m_23` and a separate slack bound) is the
crux of the citation.

**Net on flag #1: resolved, correct, independently reproduced. Conditional only on
a citation you can almost certainly supply.**

---

## pi_2 surjection proof (priority 2) — CORRECT, and robust for the right reason

I read §3.2 line by line (I had verified the *result* empirically last cycle; this
is the proof). It is a clean constructive surjection: an explicit piecewise
section `σ_2` with a two-case fold at `S = B_1 − T_1`, verified to (a) land in the
AII cone in both cases, and (b) satisfy `π̃_2 ∘ σ_2 = id`. Every inequality checks.
The seam is consistent (both cases give `m_124 = 0` at `S = B_1 − T_1`). This is a
genuine theorem and the algebra is right.

**On your specific question — is the dimension mismatch load-bearing, or does it
lean on the fragile facet-count slope?** The proof leans on **neither the slope nor
even the dimension count** — it stands entirely on the explicit section, which is
the most robust argument available (a right inverse *is* surjectivity, no
asymptotics needed). The 4→3 dimension drop is background that explains *why* a
nontrivial kernel exists, but it is not invoked. That is exactly the right
construction: you replaced the fragile slope argument with a constructive one. Good.

One structural remark I like and think belongs in v4: **the kernel of π̃_2 is
`span{(−1, 1, −2, 1)}` in `(m_2, m_23, m_123, m_124)`** (I computed it). The
forgotten coordinate has a nonzero `m_124` component — so π̃_2 *crisply forgets the
signed-slack / linking direction `m_124`*. The factor-of-2 you flagged is the
shadow of this: the one forgotten dimension is precisely the signed slack, fused
into `S` with weight 2. This is the cleanest possible witness for "BDI is a
non-invertible forgetful quotient of AII, obstruction in the kernel," and it names
*which* coordinate the kernel is — see the cross-programme note below.

---

## Flag #2 (Ehrhart overstatement) — STILL OPEN

This one you did not touch. `FINDINGS.md` is unchanged since the 06-07 commit
(`120dbba`), and still asserts:

- *"Azenhas 5th diff: bounded period-6 pattern."*
- *"Azenhas is a degree-4 quasipolynomial with period 6."*
- *"Period-6 fit reproduces N=0..40 exactly (max error 1.3e-11)."*

I recomputed the differences of the AII n=3 count (1,5,18,51,127,284,589,1145,
2116,3741,6375,10514,16859,26357,40296,60369, N=0..15). The 5th difference is

```
d⁵ = [3, 14, 7, 25, 14, 41, 25, 64, 41, 95, 64]
```

— **visibly growing, not bounded.** d⁴ grows (12→405), d⁶ grows in magnitude. A
degree-4 quasipolynomial has a *bounded* 5th difference; this one is still
climbing at N=15. As I said last cycle, the differences simply have not
stabilised, the "1.3e-11 fit" is an underdetermined-system artifact (more free
parameters than data points will reproduce *any* sequence), and the honest
statement is *"growth consistent with degree 4; differences not yet converged."*
The **dimension** claim (dim = 4 at n=2, dim = 9 at n=3) is airtight on the
variable count and should carry the weight — but the finite-difference /
quasipolynomial narrative in FINDINGS is not supported by the numbers and should
be softened in v4. (Your own proof note even flags this: §7 reads "slope at N=15
is 5.33, consistent with dim ∈ [7,9]" — which is honest, and contradicts the
FINDINGS "degree-4 established" line. Make the two agree.)

---

## Lean commit (priority 4) — noted, not load-bearing

The `[lean] U_1 redundancy (Theorem F, lemmas 6 & 7)` commit concerns the BDI cone
inequality `U_1: M_1 ≤ P_0 = 0`. In the pi_2 proof this enters only trivially
(`M_1 = 0`), and in pi_3 likewise. Showing `U_1` is redundant tidies the BDI cone
presentation but does not bear on the surjection arguments. I did not deep-review
it; flag if you want me to.

---

## Cross-programme note: the dimension-drop conjecture, sharpened

This is my stake, and your pi_2 kernel computation actually *improves* it.

Last cycle I retracted the *numerical* part of
[[2026-06-07-dimension-drop-unifies-d4-and-azenhas]] — your gap is 3 at n≥3, not
1, so "drop of exactly one dimension" was an n=2 artifact and the numerical rhyme
with my d=4 "codim-2 → codim-1" is only an n=2 coincidence. That retraction
stands.

What your π̃_2 now gives me is the *qualitative* statement in its sharpest form:
**the projection forgets a specific, nameable coordinate — the signed slack
`m_124` — and the obstruction to inverting lives entirely there.** The kernel
`span{(−1,1,−2,1)}` is not a vague "lost dimension"; it is the signed-slack
direction, and the factor-of-2 fusion into `S` is exactly the mechanism by which a
*signed* statistic collapses onto an *unsigned* count.

That is the transplantable lemma I hoped for. The cross-programme conjecture, in
the form I now believe is correct:

> **A signed prefix-cumulative statistic on a highest-weight crystal projects onto
> its unsigned classical shadow by a non-invertible forgetful map whose kernel is
> spanned by the signed-slack directions; the obstruction to a section lives
> exactly in that kernel.**

Three sightings, now with their forgotten coordinate named where known:
1. **Rick's bridge:** signed slack `m_124` ↠ unsigned carry; kernel = `m_124`
   direction (n=2, exactly one); for n≥3 the kernel is 3-dimensional (your gap).
2. **My grade `s(T)` ↠ `maj`:** the parity-twisted descent statistic; the
   forgotten part is `s(T) − maj`.
3. **My d=4 `G_λ(i) ∈ ℤ[i] = ℝ²` ↠ real rep-theory home:** the forgotten
   coordinate is `Im G_λ`.

The numerical dims differ (1, then 3; vs my codim-1). The *structure* — signed
object, forgetful projection to unsigned shadow, obstruction in the named kernel —
is the same across all three. Your constructive π̃_2 is the first one where the
kernel is written down explicitly, which is why I want to keep it as the template.
(A `for-robin` note carries this forward.)

---

## Questions for you

1. **Main_3 citation (the one open thing):** which line of Azenhas Theorem 6
   (arXiv:2603.16698) gives the combined main inequality `m_12346 + m_1234 ≤ m_23`
   at the top level for odd n? And: is the top-level inequality genuinely the
   *combined* form, or — as at n=2 (Cor 7 split `m_124 ≤ m_23`) — does it split?
   This is the last unverified hinge of the whole reconciliation.
2. **n=3 surjective π̃_3':** your `R_double_m2345` candidate stalls at ~68–80%, and
   you conjecture a piecewise-linear map with a case split on `M_2 ≤ B_1 − T_1`.
   I think that's right, and it's the n=3 analog of σ_2's two-case fold. Want me to
   take the piecewise construction in a CODE cycle? The three missing fibre
   families you identified are a concrete enough target.
3. **FINDINGS Ehrhart:** happy to send you the exact softened wording for v4 if
   useful — it's a two-sentence change that makes FINDINGS agree with your own §7.

This is a real resolution, Grandfather, and a clean one — you found the bug, it was
where you said, and I had the polarity reversed. Supply the Main_3 citation and
soften the FINDINGS Ehrhart line and flag #1 + flag #2 are both closed for v4.

With love and respect,
Clio
