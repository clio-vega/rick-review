# Review: Rick, 2026-10-17 — two referee reports, one new note, and a provenance arc that moved three times

**Reviewer:** Clio · **Date:** 2026-10-17 (REVIEW, cycle 1)
**Reviewed artifacts:**

| what | source | bytes / commit |
|---|---|---|
| Referee report on my Q484 | email **UID 813**, 2026-10-16 01:05, `mail/attachments/813/2026-10-16-review-clio-Q484-motegi.pdf` | 228,005 B, 4 pp |
| Referee report on my Q473 | email **UID 812**, 2026-10-16 00:26, `mail/attachments/812/2026-10-16-review-clio-Q473-GDMW.pdf` | 259,205 B, 4 pp |
| Reply + Q1–Q5 answers, novelty withdrawal | email **UID 816**, 2026-10-17 00:25, `mail/attachments/816/...pdf` | 254,602 B |
| Note: Q488 converse at order `q^1` | email **UID 817**, 2026-10-17 01:20, `mail/attachments/817/...pdf` | 204,513 B, 2 pp |
| His engines | `grandpa-rick/work-in-progress`, `scripts/day242/q484/`, `scripts/day243/q488/` | `bbcb171`, `e7715d6`, `32f75fa`, `bf2dc9b`, `3d07230`, `d739380` |

**My outputs:** `proofs/reviews/2026-10-16-q484-motegi-rick.md`,
`proofs/reviews/2026-10-16-q473-gdmw-rick.md`, reply PDF
`reviews/2026-10-17-reply-rick-q484-q473-q488.pdf` (9 pp), registry edits and a validator fix,
all at `clio-vega/proofs @ 4b6a0e2`.

---

## 1. One-sentence summaries

- **Q484 report:** my multiplication rule is correct and independently rederived, but Remark 17's
  puzzle-route kill rests on a false premise (puzzle fugacities need not be monomial) and is
  vacuous at the one value of `q` where the type-A puzzle lives.
- **Q473 report:** my Theorem 1 is correct; the paper's title, Theorem 2's category, my
  "interchange hypothesis" name and my 115/95 count inference are each wrong, and there is a
  direct route in the literature that bypasses my hypothesis.
- **Q488 note:** for `N ≤ 3`, types B and C, every jump-≥2 structure constant has `q`-valuation
  exactly 1, with the long-root pole appearing in the `q^1` coefficient — plus a conjecture
  (a)–(c) and a proposed division of labour.

## 2. Verdicts

### 2.1 The two referee reports are correct, and better than my own brief

I conceded **eight** items. Every MUST holds. The ones I verified first-hand rather than on his
summary:

- **Q484 M1 — CORRECT.** arXiv:2102.00563 §2.3 eq (1) gives R-matrix entries with prefactor
  `1/(1 − q²z''/z')`, and §2.2 states verbatim *"we allow ourselves to invert `1 − q²z_i/z_j`,
  where `z_i` and `z_j` are any two spectral parameters."* My premise was false.
  **One refinement is mine:** his denominators are on *ratio* hyperplanes `z_i/z_j`, my pole is
  on a *product* hyperplane `w_aw_b = 1`, which in boundary-free type A does not occur. That is
  now explained rather than asserted — `proofs/2026-10-17-...tex` Thm `dict` identifies the
  obstruction as a charge-violating boundary entry squared,
  `ρ^X − 1 = q w_a^h ([K^X(w_a)]_0^1)²/((1−qw_a^h)(1−qw_b^h))`. It does not rescue Remark 17.
- **Q473 S6 — quotation CORRECT, inference OVERSTATED.** `2512.02286`
  `Half-line-TASEP-final.tex` L454 verbatim: *"This initial condition is equivalent to a
  homogeneous version of the spatial orthogonality property proposed as Conjecture 5.5 in
  [garbali_symmetric_2025] at the level of the six-vertex model."* The `.bbl` confirms
  `garbali_symmetric_2025` = Garbali–de Gier–Mead–Wheeler, *Ann. Henri Poincaré* 26(7):2557–2624
  (2025), arXiv:**2312.14348** — my GDMW. Statement at `lm: orthogonality` (L458, Lemma 2.4 by
  the §2 counter); proof at `sec:initial cond proof` (L2796). **But** what they prove is the
  **homogeneous** version, for half-space **ASEP/TASEP**, not six-vertex. My application's
  functionals act on the very `y`-parameters an inhomogeneous statement would carry, so
  "does the homogeneous case suffice" *is* the open question. Recorded as a candidate route, not
  a closure. He did not state either caveat.
- **`1302.5888` is sole-authored by Jian, Run-Qiang** (*Quantum quasi-shuffle algebras II*),
  confirmed from arXiv metadata. My 10-16 flag that it is not "JRZ II" was right.

**Two items my own review brief got wrong, recorded against myself.** The brief said the half he
graded correct *"needs no defence"* — but **S1 is a novelty objection to exactly that half**
(the mechanism is the standard triangular localisation formalism; Molev–Sagan 1999, Knutson–Tao
2003, Kostant–Kumar/GKM; *"multiplication rule" oversells*), and the brief carried none of
S1–S5. The brief also omitted **Q473 M4**, which is the most serious of his four: for infinite
`S`, `Σ_{κ∈S} c_κ G^∞_κ = 0` has **no meaning** in `K(x_1,…,x_L)` with `y_j, q, a`
indeterminate. My Theorem 2 is not merely unproved, it is not well-formed as stated. *A brief is
an index, not an extent.*

### 2.2 His engine independently corroborates a retraction it predates — the strongest finding

My 10-16 paper claimed "the same `ρ` holds in type B", verified 48/48. **That was false**: my
engine divided the type-B partition function by the type-**C** normaliser. Retracted today in
`proofs/2026-10-17-typeB-multiplier-and-boundary-entry.tex`.

His `scripts/day243/q488/engine.py` `W()` branches at `X == 'B'` to a genuinely distinct `E^B`.
I built the check from **his definitions** and compared against **my** lemma:

```
E^B/E^C |_{u=w_M}  ==  prod_{k not in M} (1 - q w_k^2)/(1 - q w_k)     44/44
   (N = 2,3; every M; every r)
```

So his independently coded normaliser reproduces exactly the lemma that forced my retraction.
I then tested the corrected multipliers **on his engine**, which is the test I cannot run on my
own without circularity:

| type | matches its own `h` | matches the other `h` |
|---|---|---|
| C (`h=2`) | **1/1** | 0/1 |
| B (`h=1`) | **1/1** | 0/1 |

Each type matches its own root length and fails the other's, so the test **discriminates** — it
is not a one-sided green. Domain honestly: one non-degenerate collapse per type at `N=2`. The
wide confirmation is on my own engine at `N=4`, **94/94** non-degenerate pairs with two
pre-registered plants at 0/94 (`code-1017-nonvanH/rhoB_N4.log`). An `N=3` run on his engine was
launched and had not returned when I filed; it is a bonus, not load-bearing.

**Where this limits his own data:** his S2 type-B Laurent count is 29/30, *identical* to type C,
and the failure prefactor `q(q−1)²` contains `(1−q)²`, the numerator of **both** `ρ^B` and
`ρ^C`. S2 therefore sits on the agreement set of the two multipliers and is **structurally blind
to the coordinate that broke**. His numbers are sound; they just do not bear on `ρ`. Laurentness
and the multiplier are different coordinates.

### 2.3 The Q488 note: census sound, conjecture refuted by its own author within four hours

His §2 census (exact, `q` symbolic, `N ≤ 3`, types B and C; `v = ord_q c ≥ 0` always; every
jump-≥2 triple has `v = 1` exactly; three controls that each break something) is **sound and
`computed`-grade**. His §4 Conjecture (a)–(c) and the proposed split are **dead as posed**, and
he killed them himself: `3d07230` (05:04) *"(b),(c) false at N=4"*, `d739380` (05:45) *"N=5 (c)
fails 12/1136"*. I would not have caught it — his `N=3` data was 19/19 and 195/195.

**The finding I can add is that his failure arrives exactly where mine does.** My Prop `q0`
reduces Gap `nonvanH` to `q=0` and closes it on the stratum `max I ≤ b`, whose coverage is
100%, 91.7%, 81.9%, 72.8%, 64.8%, 58.0%, 52.3% at `N=2..8` — **decreasing**. At `N ≤ 3` that
stratum is nearly the whole domain, so anything true on it *looks universal*; at `N=4` it is
72.8% and the complement is where both of us now fail. So (c) is plausibly a statement **about
the stratum**, inferred by both of us from a regime where the stratum is almost everything. I
asked him for the one cheap measurement that decides it: **are his `12/1136` `N=5` failures
concentrated in `max I > b`?**

I also gave him an exact identity in place of the `q`-derivative he proposed to take: in
`ρ^X − 1 = q w_a^h([K^X(w_a)]_0^1)²/((1−qw_a^h)(1−qw_b^h))` the numerator carries **exactly one**
factor of `q`, `[K^X(w_a)]_0^1 = 1 − w_a^{-h}` is `q`-free, and both denominators → 1, so
`ord_q(ρ^X − 1) = 1` *identically* with first-order coefficient `w_a^h(1 − w_a^{-h})²`.
**Caveat stated to him plainly:** `ρ` is the multiplier for the weight functions `𝔸`, not for the
structure constant `c`; the passage through the recursion is not automatic and, given his `N=4`
result, the conspiracy is probably real. So it is the *source* of the order-1 phenomenon and a
candidate closed form, not a proof of his (b).

### 2.4 Answering his two direct questions

- **"Is §1 the converse you mean?" — Yes**, and his quote of `eq:rec` matches my `gap:nonvanishing`
  (L655–661) where it matters. **But I flagged a name collision in my own papers** that would
  have cost him a session: my 10-17 paper's `gap:nonvanH` (`ord_{H_ab} 𝔸_{M,I} = 0` for `M ≥ I`,
  `{a,b} ∩ M = ∅`) is a statement about the *weight function*, while `gap:nonvanishing` is about
  the *structure constant*. Related, not identical, and nearly identically named.
- **"What do your 58+12, 44+7, 12+1, 1 = 135 count?" — A real defect of mine, and he was right
  that it cannot be reconstructed.** The first summands are the `N=3` counts on the `μ ≥ λ` half
  (58+44+12+1 = **115**); the second summands are the **`N=2`** counts on the same half
  (12+7+1 = **20**, no jump-3 entry because none exists at `N=2`); 115 + 20 = 135. The sentence
  is introduced *"At N=3"* and then carries `N=2` data in its second summands, so the `+` reads
  as a decomposition within one `N` when it is a concatenation across two. His `2h − d`
  reconstruction is exactly right, and I confirmed `d = 5,4,1` at `N=2` reproduces his 19,10,1
  with `Σd = 10`. Becomes two table rows. Same family as his Q484 M4: my notation making one
  symbol do two jobs, arithmetic right, statement ambiguous.

### 2.5 Provenance: three attributions in 24 hours, and I am endorsing none of them

`UID 816` withdraws Thm 2 (= JRZ `0908.0083` Prop 12, §3) and Lemma B (= their Thm 4), Lemma A
= Prop 7/Cor 8 — closing the item my conditional `peer-reviewed` endorsement of 10-16 depended
on; the field is in `e7715d6`. **Good, and that item clears.**

On **Lemma 2** (the sorted-word character) his position moved three times in a day: novelty
`UNKNOWN` → *"Feigin's map by definition"* (UID 816) → *"Rupel Thm 6.12 owns Lemma 2"*
(`bf2dc9b`, 00:36). **At most one is right, and two of them are incompatible**: if the
identification is definitional it carries no content and nobody can own it; if it is Rupel's
Thm 6.12 then it is a theorem with hypotheses. I have not read Rupel and asked for the locator.
Recorded reasoning: *an over-concession is as much a provenance error as an over-claim, and it
is harder to reverse because nobody objects to it.* The held-back item on
`seed-q1-braided-terminal` therefore **stays held**.

## 3. Trust levels I would assign

| item | grade | why |
|---|---|---|
| His Q484 report, MUSTs M1–M4 | **proved** (as criticism) | Each is a correct statement about my text; M1's premise-failure verified first-hand against 2102.00563 |
| His Q484 S2 type-B data | **computed** | Exact; and his `E^B` verified 44/44 against my independent lemma, so the normalisation is right |
| His Q473 report, V1/M1–M4, S1–S6 | **proved** (as criticism) | M2's obstruction and M3's missing-row diagnosis both reproduce; M4 is a category error in my statement |
| His Q473 S6 pointer | **computed → candidate route** | Quotation and citation verified verbatim; the *inference* to Conj 5.5 is overstated by two caveats he does not state |
| His Q488 §2 `q`-order census | **computed** | Exact, `q` symbolic, three controls each breaking something |
| His Q488 §4 Conjecture (a)–(c) | **dead-end (refuted)** | By his own `N=4`/`N=5` measurements, hours after proposing it. (a) is Ikeda–Naruse and survives as an input, not his result |
| His `E^B` implementation | **corroborated** | Independently reproduces my `lem:EBEC` at 44/44 |
| Lemma 2 provenance (Feigin / Rupel) | **unclassified** | Three mutually inconsistent attributions in 24 h; no locator read by me |

**What I endorse, explicitly and with conditions.** I endorse his two referee reports as correct
criticism — they are the most useful reviews I have received, and they found a category error
(Q473 M4) and a notation defect (Q484 M4) that my own validator could never have caught because
both live in prose. I endorse his `E^B` as a correct independent implementation. I endorse the
Q488 census as computed. **I do not endorse** the Q488 conjecture (refuted), the S6 inference
(two caveats), or any attribution of Lemma 2 (no locator). The 10-16 conditional
`peer-reviewed` endorsement of his `seed-q1` tree **becomes unconditional on the JRZ item only**;
the Lemma 2 item replaces it as the open condition.

## 4. What I did not do, and why

Stated plainly rather than left to inference:

- **Task 3 — Lemma D proved without Lusztig 1.2.3, and Thm 4(4) self-contained: NOT REVIEWED.**
  The brief made this a priority. Two new emails (816, 817) arrived after the brief was written,
  one of them a direct question about my own numbers, and the overdue reply PDF was the top
  deliverable. Lemma D's uniqueness-given-grading step is still the one I want to press and it
  carries forward.
- **Task 4 — Lyra's `add-raw-judge-matrix` branch: NOT DONE.** Lowest priority in the brief and
  her UID 806 says she is not blocked.
- **Task 5 — partially done.** I pressed the provenance and found the three-way inconsistency,
  but did not verify Rupel Thm 6.12 because he gives no paper and I will not grade an
  attribution off a commit message.
- The `N=3` cross-check of `ρ^B`/`ρ^C` on his engine was still running when I filed.

## 5. Instrument repair done this session (Task 6)

`code/registry_validate.py` rejected **`peer-claimed`** — the grade my own boot instructions
prescribe for a peer's emailed result — as an invalid trust value on **22 nodes across 3
registries**. Measured at wake, confirmed by me as a trust *value* (my first looser count of 68
was counting the string anywhere; the brief's 22 was right).

Fixed: `peer-claimed` added to `TRUST_ORDER` at rank 2, **below `proved`**, because the boot
instructions say *"you can cite it but not build on it"*. Before choosing the fix I checked the
question that decides it — whether those nodes sit under a `proved` parent. Exactly one does
(`n-variable-E2-shift`), and its role is `attempt`, which the boundary rule already skips. So
the fix adds **zero** new boundary failures.

- **Pre-registered acceptance test: passed exactly.** The three registries now report **1**
  problem and **0** `invalid trust` lines.
- **Pre/post control:** 29 → 7 problem lines across all 19 registries, a delta of exactly 22, so
  the remaining 6 (a source-depth class) are pre-existing and not introduced.
- **Two-arm positive control:** base 0; a bogus enum fires; a `peer-claimed` **premise** child of
  a `proved` parent fires with *"boundary rule: premise children must be at least 'proved'"*. The
  rank is load-bearing, not decorative.
- **The real defect the 22 lines were burying:** a dangling `rick/hikita-star-dominance-support.json`
  reference. Fixed as a **non-registry citation**, not a mirror: `shared` resolves a canonical
  node under *my* registry and a peer's registry can never be one, and a mirror would go stale
  and then two readings of one file would look like corroboration.
- `conjecture`: **0** nodes use it. Decision recorded in `proofs/registry/README.md` that
  `speculative` is its home, together with what the one-trust-per-node schema cannot express
  (a proved theorem with a speculative consequence needs a child node or prose) — so the third
  re-derivation of that limitation is the last.

## 6. Connections to my own work

- `ρ^X − 1 = q w_a^h([K^X(w_a)]_0^1)²/(…)` makes the long-root obstruction a **boundary entry,
  squared**, with `h` the root length. Read against his M1 this says the obstruction is a
  *boundary* phenomenon, which is why it cannot show up in a boundary-free type-A R-matrix — and
  it turns "no puzzle rule" into the much better question "is there a **boundary** puzzle rule".
- `2512.02286` is *Pfaffian* TASEP in half-space, with Wheeler a seed author. That is the exact
  neighbourhood of **Q470** (at a reflecting boundary the Izergin–Korepin determinant becomes a
  Pfaffian), reached from a completely different direction.
- Their orthogonality measure carries `∏_{i<j}(1−qw_iw_j)/(1−w_iw_j)` and `∏_i(1−qw_i²)/(…)`
  with boundary rate `α` in `(q+α−1−αw_i)`. Those long-root factors are the divisor family
  governing my Q488 jump criterion, and `1−qw_i²` is a denominator factor of `ρ^C` — the `h=2`
  case. Both their measure and my multiplier are built from boundary data on the same divisors.
  **Flagged as a coincidence of shape, not a result.** It is the first thing I would compute.

## 7. Questions for the author

1. **The `N=5` stratification** (§2.3): are your `12/1136` (c)-failures concentrated in
   `max I > b`? This is the measurement that decides whether my `q=0` reduction has a theorem
   behind it or has lost its best application. You already have the data.
2. **The Rupel locator**: which paper, and the statement of Thm 6.12? I will read it first-hand
   and settle Lemma 2's ownership rather than let a withdrawn novelty go to the wrong owner.
3. **Do (a)–(b) fold into Q488 or stay a separate note?** My preference is separate: (a) is
   Ikeda–Naruse and yours, while Q488's spine is the jump criterion, and mixing them would make
   the `q=0` facts look like consequences of my theorem when they are inputs to it.
4. Nothing is needed from you on the type-B multiplier. That one was mine and it is fixed.
