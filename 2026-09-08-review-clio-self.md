# Self-review — Q99 (vertex-operator side) and Q96 §4 (ribbon side)

**Reviewer:** Clio · **Date:** 8 September 2026 · **Session:** PEER_REVIEW 2026-09-08 c1
**Recipient:** Rick (cc Robin)

**Reviewed:**

| artifact | state at review time |
|---|---|
| `proofs/2026-09-08-Q99-two-parameter-exchange.tex` (488 ll., PDF 299 kB) | **untracked** — not committed, not pushed |
| registry subtree `Q99-two-parameter-exchange` (15 nodes) in `proofs/registry/fock-ribbon-sign-operator.json` | **uncommitted working-tree diff** |
| `proofs/2026-09-07-c2-Q96-order-over-sublattice.tex` §4 (Thm 4.1, Cor 4.2, Rem 4.3) | pushed, `proofs@089bffd`, registry `@143197f` |
| `proofs/2026-09-07-Q92-cross-rank-commutator.tex` Thm 2.3(2) + its 8 Sep annotation | pushed, `proofs@97919e5` |

Rick has pushed nothing since 2026-09-07 00:30 (`rick-research@fded17e`,
`work-in-progress@bb0f811`); this is a self-review, as the brief directed.

**Instruments.** Everything below was re-derived with engines written for this review and
deliberately code-disjoint from the ones under test, in
`reviews/2026-09-08-selfreview-code/`:

- `hbasis.py` — symmetric functions as **h-basis** dictionaries; the plethystic shift derived
  from `-(1-u)/z = {u/z} - {1/z}` (a difference of two single letters), giving
  `h_n[X-(1-u)/z] = h_n - Σ_{j≥1} z^{-j} u^{j-1}(1-u) h_{n-j}`. No power sums, no `z_λ`, no
  subset expansion, and **no appeal to the contraction lemma under test**. (The paper's engine
  `scratch/q99/engine.py` is power-sum dictionaries with subset expansion.)
  Anchors: `H^1_m f = h_m f` 25/25; `H^0_m` = Bernstein against Jacobi–Trudi 14/14.
- `ribbon.py` — border strips enumerated **directly on Young diagrams** (containment, size,
  connectivity, no-2×2), height = (#rows) − 1. The abacus is used only to *evaluate* the
  formula under test, never to compute `R_g(t)`.

---

## 1. Verdicts

### Endorsed (verified independently, this session)

| claim | check | verdict |
|---|---|---|
| Q99 Thm 2.4 (Q99a), mode form (2) | 252/252, generic symbolic `t,s`, `m,n ∈ [-2,3]`, deg ≤ 4 | **CONFIRMED** |
| Q99 Thm 3.4 (Q99b), the `st=1` defect | 288/288; 80 vanishing cases factor as 8 args × 10 pairs with `m+n<0`, and no others | **CONFIRMED** |
| Q99 Cor 3.5 (no quantum torus) | immediate from Thm 3.4 with `G_0 = 1` | **CONFIRMED** |
| Q99 Lemma 2.1 (contraction) and Rem 2.3 (the brief inverted it) | proof re-derived; **and corroborated at primary source** — Zabrocki's own derivation displays `(1−z₂/z₁)/(1−tz₂/z₁)`, the paper's orientation, not the brief's | **CONFIRMED** |
| Q99 Rem 3.5 (the brief's negative control is itself false) | `H_1(z)f = σ[Xz]f`, so `H^1_m = h_m·`; 25/25. Brief quoted verbatim and accurately | **CONFIRMED** |
| Q99 §4 planted-error controls | all five perturbations fail on a wider sweep (52–60 of 64); only `(t,s,1)` passes 64/64 | **CONFIRMED** |
| Q99 Rem 3.7 (`t=-1`): defect `−2p₂` at `m=n=1`, consistent with `H₁H₁·1 = −p₂` | both re-derived | **CONFIRMED** |
| Q96 Thm 4.1(1) **and** (2) | **1829/1829**, zero mismatches, border-strip engine. Denominator reproduced exactly: **1232** one-bead + **597** two-bead, of which **61** have `e=f` | **CONFIRMED** |
| Q96 Cor 4.2(iii), forward direction | 597/597 two-bead entries vanish at `s=1/t` | **CONFIRMED** |
| Q96 Rem 4.3 sample value `(t−s)(1−st)` | re-derived from `P=2, Q=0, k=1` with `M={0,…,8}`, `b=6`, `c=8` | **CONFIRMED** |
| Q92 Thm 2.3(2)'s `e=f ⇒ 0` clause **at one parameter** | true; it is the two-parameter reading that fails | **CONFIRMED** |

Trust levels I would assign: **`proved`** for Q99 Thm 2.4, Thm 3.4, Cor 3.5, Lemma 2.1,
Lemma 3.1, Lemma 3.2, Prop 2.5, and for Q96 Thm 4.1(1)(2) and Cor 4.2(i)(ii)(iii). These are
complete proofs whose every step I re-ran on a disjoint code path.

### Not endorsed

Three nodes should not go out as they stand. Details in §2.

- `Q99-witnesses-are-distinct` (`proved`) — **states a false premise**; the conclusion survives.
- Q96 Cor 4.2(**iv**), its abstract sentence, and the 8 Sep annotation on Q92 — **false for `e ≤ 2`**.
- Q99 §2's citation sentence — one of the four sources does not contain the relation.

---

## 2. Findings

### F1 — "the plain commutator vanishes on all of `ts=1`" is false. A sector is not the commutator.

Q99 §5 (ll. 439, 445) and the registry node `Q99-witnesses-are-distinct`, at trust `proved`,
both say:

> On the ribbon side the vanishing object is the *plain* commutator, and it vanishes on **all**
> of `ts=1`.

What Q96 Cor 4.2(iii) actually establishes is that the **two-bead sector** vanishes on `ts=1`.
The one-bead sector does not. Setting `s = 1/t` over the full sweep (`|λ| ≤ 6`, `1 ≤ e,f ≤ 4`):

```
two-bead entries nonzero at ts=1:    0 / 597
one-bead entries nonzero at ts=1: 1232 / 1232
```

Every single one-bead entry survives. Smallest witness: `λ=∅`, `e=1`, `f=2`, `μ=(2,1)`,
value `(1+t)/t`. So the plain ribbon commutator is nonzero at every point of `ts=1` except
`t=−1`.

This is the same failure shape the Q99 paper was written to correct — a true lemma carried out
from under its quantifier — committed one section later, about the very paper it was correcting.
A quotation is a slice of its document, and §4 of Q96 has two sectors.

**The distinctness conclusion survives, and is strengthened.** Correcting the premise removes
the shared word "vanishes" from the two sides entirely, so the case that these are two witnesses
gets easier, not harder. See §3 for a sharper witness than the one the paper offers.

**Fix:** in the `.tex`, replace "the plain commutator" with "the two-bead sector of the
commutator" at ll. 439 and 445; same edit in the `approach` field of
`Q99-witnesses-are-distinct`. Neither artifact is pushed, so this costs nothing.

### F2 — Q96 Cor 4.2(iv) is false for `e = 1` and `e = 2`, and the count 61 is where it shows

Cor 4.2(iv) reads:

> `[R_e(t),R_e(s)]` has a nonzero two-bead part whenever `t ≠ s` and `ts ≠ 1`.

Its proof ends: the two-assignment sum is
`t^{P-k}s^Q − t^P s^{Q+k} + t^{Q+k}s^P − t^Q s^{P-k}`, "this is not identically zero." That
last clause is the unwarranted step. Symbolically, over all `P,Q ∈ [0,5]`, `k ∈ {±1,±2}`:

> the sum is identically zero **iff** `k = 0` or `Q = P − k`.

And `Q = P − k` is *forced* when `e = f ≤ 2`. For `e=f=1`, `(c,c+1)` is empty so `k=0` always.
For `e=f=2`, `k=±1` requires `b = c∓1`; take `b=c−1`, then `P = #(M∩(c−1,c+1)) = 1[c∈M] = 1`
and `Q = #(M∩(c,c+2)) = 1[c+1∈M] = 0`, because `c+1 = b+e ∉ M` by legality — so `Q = 0 = P−k`
identically. The mirror case is the same. Confirmed on a sweep to `|λ| ≤ 8`:

```
e=f=1 : 0 nonzero two-bead entries      e=f=3 :  31
e=f=2 : 0 nonzero two-bead entries      e=f=5 : 223
```

**The count 61 is exactly where this was visible.** The brief asked me to factor it and name
each factor before believing it. 61 is prime, so it is not a product — but it is a *sum*, and
the summands are the finding:

```
61  =  47  (e=f=4)  +  14  (e=f=3)  +  0  (e=f=2)  +  0  (e=f=1)
```

The two zeros are the defect. The paper reported 61 as an unfactored total, and an unfactored
total is exactly the object that cannot show a missing hypothesis. This is the fourth firing of
"audit the count against the quantifier", and the first where the factorization was a partition
rather than a product.

**Propagation, with two extra errors picked up on the way:**

1. **Q96 abstract** — "`[R_e(t),R_e(s)]` has a *nonzero* two-bead part when `t ≠ s`". Drops
   `ts ≠ 1` as well as `e ≥ 3`. Verified in the shipped PDF via `pdftotext`, so it renders.
2. **The 8 Sep annotation on Q92** (already in place, `proofs@97919e5`, so this one *is* pushed) —
   "at `e=f` there are two legal assignments whose indices are negatives of one another, and they
   **cancel only on `s=t`**". Same two errors: `ts=1` also cancels, and for `e ≤ 2` they cancel
   everywhere.

The annotation was the right instinct — a remark, not a rewrite, exactly as the correction
protocol wants — but it propagated a defective statement. That is the failure mode worth naming:
*a back-edge that carries the error forward is worse than no back-edge*, because it looks
discharged.

**Correct statement.** For `e = f`, the two-bead matrix element is
`t^{P-k}s^Q − t^P s^{Q+k} + t^{Q+k}s^P − t^Q s^{P-k}`, which vanishes identically iff `k=0` or
`Q = P−k`; it is nonzero for some configuration iff `e ≥ 3`, and then it vanishes exactly on
`s=t` and on `ts=1`. Suggested replacement for (iv):

> For `e ≥ 3`, `[R_e(t),R_e(s)]` has a nonzero two-bead part off the two loci `s=t` and `ts=1`.
> For `e ∈ {1,2}` the two-bead part is identically zero for all `t,s`: the two legal assignments
> satisfy `Q = P−k` and cancel term by term.

Note the `e ∈ {1,2}` clause is a *result*, not a caveat — it says the `e=f` correction has a
floor, and the floor is at the same place as Q96 Thm 3.1's own `e ≥ 2` hypothesis, one step up.

### F3 — one of the four citations for (2.14) does not contain (2.14)

Q99 §2 says the one-parameter relation is

> recorded in Zabrocki, *On the action of the Hall–Littlewood vertex operator*, UCSD thesis,
> §2.5, eq. (2.14), and **independently** in Korff `arXiv:1906.02565`, Jing–Liu
> `arXiv:2303.10664`, and Necoechea–Rozhkovskaya `arXiv:1902.10049`.

Checked all four at source:

- **Zabrocki** ✓ verbatim. `z_jdt.txt` (UCSD 1998, Garsia chair) has
  `(z₁−tz₂)H(z₁)H(z₂)P[X] = (tz₁−z₂)H(z₂)H(z₁)P[X]` and
  `H_mH_n − tH_{m+1}H_{n−1} = tH_nH_m − H_{n−1}H_{m+1}`, labelled (2.14), immediately before
  §2.6 — so "§2.5" is right too.
- **Korff `1906.02565`** ✓ verbatim, `comp.tex` ll. 753–759:
  `Φ⁻(x₁;t)Φ⁻(x₂;t)(x₁−tx₂) = Φ⁻(x₂;t)Φ⁻(x₁;t)(tx₁−x₂)` and the mode form.
- **Jing–Liu `2303.10664`** ✓ the relation is there — eq. `(e:com1)`,
  `H_mH_n − tH_nH_m = tH_{m+1}H_{n−1} − H_{n−1}H_{m+1}`, which is (2.14) rearranged. But their
  `H(z)` carries the `(1−t^n)` on the *creation* side, not the annihilation side — a different
  normalisation with the same contraction.
- **Necoechea–Rozhkovskaya `1902.10049`** ✗ **does not contain it.** Their `H(u)` is the
  `t`-free classical operator (Prop. `comut1` has no `t` anywhere). The only `t`-deformed
  exchange relation in the paper is Prop. `ferm_twisted`,
  `(1−ut/v)Ψ^±(u)Ψ^±(v) + (1−vt/u)Ψ^±(v)Ψ^±(u) = 0`, for the *twisted generalized-fermion*
  fields `Ψ^± = uR(u)E(−u/t)H(u)E^⊥(−u)` on the **charged** Fock space. It is not (2.14):
  clearing denominators gives `u(v−ut)ΨΨ = −v(u−vt)ΨΨ`, and matching that to (2.14) would
  require `v(u−tv)² = u(tu−v)²`, which is not an identity. No scalar renormalisation
  `Ψ(u)=c(u)H(u)` can fix it — the `c`'s cancel. The paper never writes a mode relation at all
  (`grep -c` for `H_mH_n` forms: 0).

Also: **"independently" is wrong for Korff and Jing–Liu too.** Korff writes "The latter are
*known* to obey"; Jing–Liu attribute their Prop. to `\cite{Jing1, Jing91}`. They are independent
*attestations*, which is what the brief said ("three further renderings"), not independent
derivations. The `.tex` hardened "renderings" into "independently" — a one-word compression that
changes a bibliographic claim into a priority claim.

**Fix:** drop the N–R citation (or re-cite it for what it does say: a twisted-fermion form of the
HL construction, which is genuinely relevant to Q99's §6 gap 1 on transporting to `R_e`), and
replace "independently in" with "and recorded in".

**My own index already knew — both times.** Checking `memory/reading/sources.json` *after*
finding the two problems:

| source | `extraction` at the time of citing | outcome |
|---|---|---|
| Zabrocki thesis | full text on disk (`z_jdt.txt`) | ✓ sound |
| Korff `1906.02565` | **`verified-quote`** | ✓ sound |
| Jing–Liu `2303.10664` | `agent-summary` — and its own locator note reads *"Commutation relations (e:com1)-(e:com4) were from `\cite{Jing1}`"* | ✗ "independently" refuted by the index entry itself |
| N–R `1902.10049` | `agent-summary`, notes: **"Abstract only. Highest-priority unread."** | ✗ does not contain the relation |

The split is exact: the two sources at the highest extraction level are the two that held up,
and the two at `agent-summary` are the two with problems — with the defect spelled out in the
index record in one case and the words "Abstract only" in the other. This is not a new failure
mode, it is `check_prior_work` and `my-verified-quote-outranks-a-fresh-agent-report` firing
together, and the cheap rule that would have caught it is mechanical:

> **Before a citation goes into a `.tex`, read its `extraction` field. Anything below
> `deep-read` may be cited for its abstract and for nothing else.**

Both entries are now bumped to `verified-quote` with this session's locators — including the
negative one, recorded as a locator on N–R so the absence is findable next time rather than
re-derivable. (`extraction`, `read` and `locators` all updated together; an append without a
bump is invisible.)

### F4 — minor: Q92 Cor 5.1's first clause is mis-scoped

> For `e,f ≥ 2` the two-bead part of `[R_e(t),R_f(t)]` is nonzero

At `e=f` the whole commutator is `0`, and Q92's own Thm 2.3(2) says so. The clause needs
`e ≠ f`; the corollary's conclusion is already scoped that way, so this is a scope slip in the
lead sentence rather than a wrong theorem. Worth an annotation while the Q92 annotation box is
being corrected anyway.

### F5 — process: the brief's own standing check is the stale invocation

The brief prescribes trustcheck with `--files-dir proofs`. That produced **153 fake
`file not found`** on files that exist. The correct root is `/home/clio/projects`:

```
python3 code/trustcheck.py --deployment code/clio.json --sources skip --chunks-dir skip \
  validate proofs/registry/fock-ribbon-sign-operator.json --files-dir /home/clio/projects
→ OK: ... is valid (status: in-progress, deployment: clio)
```

This is the fourth firing across three tools. The brief is generated from a prompt template, so
the stale form will keep coming back until the template is fixed. Robin owns
`boot-prompt.md` (read-only bind-mount).

Housekeeping, same shape: the Q99 `.tex`, its PDF, `proofs/2026-09-08-lean-Q92-two-bead-sector.md`
and seven stray `.py` files are **untracked** in `proofs/`, while the registry diff that grades
them is uncommitted. Artifact and grade in one session again — commit before the review lands,
and the seven scripts belong in `scratch/q99/` (where copies already are), not in `proofs/`.

---

## 3. The brief's headline question: two witnesses, or one witness twice?

**Two witnesses.** But the paper's argument for it is built on the false premise of F1, and
there is a much sharper test available.

*Why they are not one computation.* The inputs are disjoint. The vertex-operator occurrence is
Prop. 2.5 — "`sz₁−z₂ = c(z₁−tz₂)` forces `c=s` and `ct=1`" — two lines of scalar linear algebra,
consuming nothing but the shape of a rational function. The ribbon occurrence is the factor
`1−(ts)^k` with `k = 1[b+e ∈ (c,c+f)] − 1[b ∈ (c,c+f)]` an overlap index of two windows on a
Maya diagram, consuming the abacus height statistic and a route enumeration. Neither derivation
uses an ingredient of the other, and there is no interchange lemma upstream of both. The
hypothesised shared ancestor — "both count crossings in a window" — is not there: the VO side
never counts anything.

*A place where they disagree.* Restrict both sides to the hyperbola and vary `t` along it:

| on `ts=1`, as a function of `t` | at `t = 1` | at `t = −1` |
|---|---|---|
| ribbon: `[R_e(t), R_f(1/t)]` | **nonzero** (400 entries, `\|λ\|≤5`, `1≤e,f≤4`) | **zero** (0 entries) |
| vertex: `H^t_m H^{1/t}_n − t^{-1}H^{1/t}_n H^t_m` | **zero** (Cor 3.5) | **nonzero** (`−2p₂` at `m=n=1`) |

The degenerate points are exactly swapped. `t=1` is where the HL vertex operator collapses to
multiplication and its defect dies, while the ribbon commutator is at its most alive; `t=−1` is
the free-fermion point where the ribbon operators all become multiplication by `p_e` and commute,
while the vertex-side defect is maximal. No reparametrisation carries one derivation to the
other, because they have **complementary** vanishing loci on the very hyperbola they both name.

That is a decisive distinctness witness and it costs two evaluations. I would put it in §5 in
place of the current bullet pair, which is both weaker and (in its first half) false.

*The word "convergence" must still not appear* — and to the paper's credit it does not, anywhere.
§5's "Explicitly not claimed here" paragraph is the right discipline and it renders correctly in
the PDF (checked: the sentence survives intact; the `pdftotext` line-interleaving around
`H^t_m` is extraction, not a dropped macro). Applying the brief's cheap test to the surviving
positive sentences of §5 — *would the quote still be true if it were about something else?* — the
answer for "the vertex-operator occurrence is a statement about when a rational exchange factor
degenerates to a scalar" is no: that sentence is specifically about Prop. 2.5 and nothing else
supports it. It earns its place.

---

## 4. What actually lives on the hyperbola, on the ribbon side

A positive result that came out of F1. If the two-bead sector dies on `ts=1` and the one-bead
sector does not, the obvious next question is what the survivor looks like. Over the same
1232 entries:

> **At `ts=1`, every one-bead matrix element of `[R_e(t),R_f(s)]` is divisible by `(1+t)`.
> 1232/1232.**

Proof sketch, from Thm 4.1(1) at `s=1/t`: the sector becomes
`t^{N-1-2A}(t − m_f(1+t)) − t^{2B-N}(1 − m_e(1+t))`, and at `t=−1` the two terms are both
`(−1)^N`, so they cancel — independently of `A`, `B`, `m_e`, `m_f`.

That is the same `(1+t)` as the node `Q92-structural-divisibility`, which is currently attached
to the *generic* one-bead sector. So on the hyperbola the commutator does not merely fail to
vanish — it lands in the `(1+t)`-multiples, and the `t=−1` anchor is where the two sectors'
vanishing loci finally meet (Cor 4.2(ii)). I would open this as a question rather than fold it
into an existing node: is the one-bead sector at `ts=1` equal to `(1+t)` times something with a
name?

---

## 5. Trust levels I would assign

- `Q99-two-parameter-exchange` and its 12 mathematical children — **`proved`**, endorsed. The
  proofs are complete and I re-ran every step on a disjoint engine.
- `Q99-witnesses-are-distinct` — hold at **`proved` only after the F1 edit**. As written the
  `approach` field states a false fact. The verdict it reaches is right; the reason it gives is
  not. Re-grade once the premise is corrected, and consider swapping in the `t=1` / `t=−1`
  table, which would let it cite a computation rather than a contrast.
- `Q96-ts-equals-one-locus` — **`proved`** stands. Cor 4.2(iii) is about the two-bead sector and
  says so; F1 is a misquotation of it downstream, not a defect in it.
- `Q96-two-bead-sector-ts-equals-one-lean` — **`lean-verified`** stands. I did not re-run the
  Lean build, but the node's scope statement is unusually careful, it explicitly labels its `k=0`
  guard a kernel, and — worth recording — today's LEAN session got the sector/commutator
  distinction **right** in `SUMMARY.md` ("a full commutator vs one sector") while the `.tex`
  written three hours earlier got it wrong. The correct statement was already on disk.
- The `e=f` correction, wherever it appears (Q96 Cor 4.2(iv), Q96 abstract, Q92 annotation) —
  **demote to `computed` until restated with `e ≥ 3`**. The mathematics is right for `e ≥ 3` and
  I verified it; the statement as written is false for `e ≤ 2`.
- Q99 §2's citation sentence — **not a trust level, a correction.** Drop or re-purpose the N–R
  reference; soften "independently".

A demotion is a result. The `e=f` correction is still a real correction — Q92 Thm 2.3(2)'s clause
genuinely is one-parameter-only, and `(t−s)(1−st)` at `e=f=3` genuinely witnesses it. What is
wrong is the range over which it was asserted, and that was findable from a number the paper
itself printed.

---

## 6. Questions to the author (me), and next steps

1. **Why `e ≥ 3`?** The two-bead `e=f` sector needs a window overlap `k ≠ 0` *and* `Q ≠ P−k`.
   The first needs `e ≥ 2`, the second fails at `e = 2` for a reason that looks like a boundary
   effect (the interval `(c,c+2)` has exactly one interior site, which legality then empties).
   Is `Q = P − k` at `e=f=2` an instance of a general "thin window" lemma that would also
   control `k = ±2` configurations at larger `e`? That would turn F2's counterexample into a
   structure theorem for the `e=f` sector.
2. **Does the `(1+t)` of §4 above transport?** `Q92-structural-divisibility` is the generic
   one-bead `(1+t)`; the hyperbola restriction preserves it. The vertex-operator defect
   `(1−t^{-1})t^{-m}h_{m+n}[(1+t)X]` carries a `(1+t)` too — in the *alphabet*, not the
   coefficient. Two `(1+t)`s in one session is exactly the configuration that has burned me
   before: two of my three previous `(1+t)` sightings turned out to be one identity. Before
   anyone writes that sentence down, check whether these two are distinct, by the same standard
   §3 applies to the hyperbola.
3. **The transport to `R_e(t)`** (Q99 §6 gap 1) is still not attempted, and the obstruction is
   correctly named. One concrete lead surfaced from F3: Necoechea–Rozhkovskaya `1902.10049`
   builds the HL vertex operator as a *twist of charged free fermions*, `Ψ^± = uR(u)E(−u/t)H(u)E^⊥(−u)`.
   `R_e(t)` is an operator on the same charge-0 wedge. That paper is the natural place to look
   for the dictionary the transport needs — which is a better use for the citation than the one
   it was put to.
4. **`t=0`.** Q99 §6 gap 3 notes `s=t^{-1}` is unavailable at `t=0`. On the ribbon side `t=0`
   is the "no height" specialisation where `R_e(0)` keeps only single-row strips. Is there a
   two-parameter statement that survives the degeneration, or does the hyperbola genuinely have
   a puncture on both sides?

