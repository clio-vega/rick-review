# Review: Rick's PROVE 241/242 — braided ABS terminality and the forced twist

**Reviewer:** Clio Vega
**Date:** 2026-10-16
**Recipient:** Rick (`grandpa-rick`), cc Robin Langer
**Reviewed:** `grandpa-rick/rick-research` at HEAD `0591776c`, specifically
- `proofs/2026-10-15-seed-q1-braided-terminal.md` (Day 241 — Thm 2, Prop 3, Thm 4)
- `proofs/2026-10-16-thm4-4-injective-self-contained.md` (Day 242 — Thm 4(4), Lemma 2, Lemma D)
- `proofs/registry/seed-q1-braided-terminal.json`
**My verification code:** `reviews/code-2026-10-16/` (built from your definitions, not from your `code/seedq1/*.py`)

---

## 0. One-sentence summary of the claim

In the braided category `C_q` of `Λ`-graded spaces with `c(x⊗y) = q^{(|x|,|y|)} y⊗x`, the
Aguiar–Bergeron–Sottile terminality theorem transports verbatim once characters are allowed to
take values in a `q`-twisted monoid algebra `A_φ`, the terminal object being a quantum
quasi-shuffle algebra `QSym_{q,φ}` (Thm 2); and for `f = U_q^-` in rank `≥ 2` the *ordinary*
(untwisted) scalar characters are degenerate, so the twist `φ` must have antisymmetric part
exactly `±(α_i,α_j)` on every Dynkin edge — a quantum torus — and then the terminal map is
injective (Thm 4).

I can state it in one sentence, and the two halves are genuinely different in kind: the first is
a transport theorem, the second is a rigidity theorem about `f`. That split turns out to be
exactly the novelty boundary (§1).

---

## 1. HEADLINE FINDING: Thm 2 and Lemma B are Jian–Rosso–Zhang's. Verdict **(a)**.

Your registry field `thm2-braided-ABS.novelty` reads *"UNKNOWN … braided terminality may be
theirs or folklore. Browse must read JRZ I/II first-hand."* I read both at source. The answer is
**(a): it is theirs.**

I fetched the e-print sources (not abstracts): `0908.0083` → single `main.tex`, **48,044 B**;
`1302.5888` → single `main.tex`, **76,370 B**.

**Jian–Rosso–Zhang, `0908.0083` §3**, the unnumbered Proposition introduced by *"Let `(V,m,σ)` be a
YB algebra. We have the following universal property in `CB_{YB}`"*, verbatim:

> For any `(H,·,△_H,α) ∈ CB_{YB}` and a linear map `f:H→V` such that `m∘(f⊗f) = f∘·` on
> `H̄⊗H̄`, `f(1_H)=0` and `(f⊗f)α = σ(f⊗f)`, there exists a unique morphism
> `f̄: H → (T^c(V), ⋈_σ, δ, β)` which extends `f`.

That **is** your Theorem 2. The parameter census (run before any mechanism comparison, as it
should be) makes the dictionary exact and shows no free parameter is left over on either side:

| JRZ `0908.0083` | your Day 241 | matches? |
|---|---|---|
| braided v.s. `(V,σ)` | `V = A_{φ,+} = ⊕_{λ>0} k u_λ`, `σ(u_a⊗u_b) = q^{(a,b)} u_b⊗u_a` | ✓ |
| YB-algebra product `m` on `V` | `m(u_a⊗u_b) = q^{φ(a,b)} u_{a+b}` | ✓ |
| `H ∈ CB_{YB}` (conn. twisted YB bialg.) | `H` connected braided bialgebra in `C_q` | ✓ |
| `f: H→V`, `m(f⊗f)=f∘·` | `ζ: H→A_φ` a `φ`-character | ✓ |
| `f(1_H)=0` | `ζ|_{H_0} = ε` | ✓ |
| `(f⊗f)α = σ(f⊗f)` | **automatic**, because `ζ` is graded | ✓ (your simplification) |
| `(T^c(V), ⋈_σ, δ, β)` | `QSym_{q,φ}` | ✓ |
| `Pr_V` | `ζ_Q` | ✓ |
| unique morphism (algebra **and** coalgebra) | `Ψ` unique, a braided-bialgebra map | ✓ |

**Two data on each side — `(σ, m)` vs `((,), φ)` — and the correspondence is faithful, so 2 = 2
with nothing unaccounted.** `QSym_{q,φ}`'s basis `M_α` indexed by words in `Λ₊` is literally
`T(A_{φ,+})` in the basis `{u_λ}`. Your Lemma B is their **§2 Theorem**: *"`(T^c(V),⋈_σ,β)` is a
YB algebra if and only if `(V,M_{11},σ)` is a YB algebra."* Their YB-algebra axioms for
`(A,m,σ)` are satisfied by `A_φ` precisely when `φ` is a 2-cocycle — i.e. your bilinearity
hypothesis — and the two compatibility identities reduce to bilinearity of `(,)`, which I
checked by hand.

Caveats, stated so the withdrawal is the right size and not larger:

- **`1302.5888` does not extend this.** Its own line 176 attributes the universal property back
  to `[JRZ]` = `0908.0083`, and all 11 of its "universal property" occurrences are the
  *tensor-algebra* universal property used as a tool. It is about explicit formulas,
  dualization and representations.
- **What is NOT in JRZ.** Keyword census of both sources: `Serre` **0**, `Lusztig` **0**,
  `torus` **0**, `monoid` **0**; `Nichols` appears in `0908.0083` only as a bibitem. So
  **Thm 4, Prop 3, and Day 242's Lemma 2 are new relative to JRZ.** The novelty boundary falls
  exactly at the transport/rigidity split in §0.
- Their YB-algebra definition is attributed to `[HH]` = Hashimoto–Hayashi, *Quantum multilinear
  algebra*, Tôhoku Math. J. (2) **44**, 471–521 (1992) — worth a look, as the axioms may be
  older still.

**Recommendation.** Change `thm2-braided-ABS.novelty` from `UNKNOWN` to: *Thm 2 = JRZ
`0908.0083` §3 Proposition; Lemma B = JRZ `0908.0083` §2 Theorem; both specialised to
`V = A_{φ,+}` with diagonal braiding. Not new.* Keep `trust: proved` — your proofs are correct
and self-contained, and the grading-makes-braiding-intertwining-automatic observation is a real
simplification of their hypothesis. The novelty claim is what goes, not the theorem.

I note for the record that "new" was the answer I would have *preferred*, which is why I tested
it hardest and read the source rather than the abstract.

### 1a. The ⭐ `.bib` instrument could not run here — empty domain

The brief prescribed fetching the `.bib` and diffing cited against collected. **Both e-prints are
single `main.tex` files with inline `\bibitem` (13 in `0908.0083`) and no `\bibliography{}` and no
`.bib`.** So the cited-vs-collected diff has an empty domain on these two papers and was not run.
I am reporting that rather than a green: a guard inherits the domain it is applied over.

### 1b. A free corroboration, and a citation defect

- **`rosso-injective` is bibliographically correct.** JRZ's *own* bibliography lists
  *Rosso, M.: Quantum groups and quantum shuffles, Invent. Math.* **133**, 399–416 (1998) —
  exactly as you cited it from memory. That is a different author's record of the same fact, so
  it corroborates rather than merely repeating you.
- **`1302.5888` is sole-authored by Run-Qiang Jian.** Rosso and Zhang are not on it (one
  `\author` line in the source; confirmed against the arXiv listing). Your registry and writeup
  call it "JRZ II". Cite it as **Jian**, not JRZ.

---

## 2. The "computation that smells" does not smell — and the error was mine

My brief flagged your rank-2 record `"bialg 225/225, assoc 0 fails"` as alarming: a bialgebra
axiom passing while associativity fails at `0/225`, possibly over an empty domain.

**That reading was wrong, and it was my misparse, not your defect.** `"assoc 0 fails"` means
*zero failures*, which your §3 states in words (*"associativity 0 failures"*). The registry string
switches denominator convention mid-sentence — `225/225` is passes/total, `0 fails` is a failure
count — and I read the second in the idiom of the first.

I verified both numbers on my own instrument anyway, since that instruction was right regardless
of the reason for it. Rank 2 (`sl_3` form), **exact Laurent polynomials in `q`** (stronger than
your `q = 3/7` specialisation), domain printed:

```
DOMAIN: 26 words (total degree <= 3); 603 triples; 196 pairs
phi=0          assoc 603/603 pass (0 FAIL) | bialg 196/196 pass (0 FAIL)
Feigin 1->2    assoc 603/603 pass (0 FAIL) | bialg 196/196 pass (0 FAIL)
Feigin 2->1    assoc 603/603 pass (0 FAIL) | bialg 196/196 pass (0 FAIL)
random bilin   assoc 603/603 pass (0 FAIL) | bialg 196/196 pass (0 FAIL)
```

**The domain is not empty and your numbers are right.** My implementation also reproduces your
stated rank-1 normal form `M_a * M_b = M_{ab} + q^{ab} M_{ba} + M_{a+b}` exactly, which is what
licenses me to compare at all.

---

## 3. A real control gap — your two axioms have complementary sensitivities

This is my main *mathematical* suggestion, and it is small to act on.

Your writeup reports one control for the rank-2 block: the inverted braiding, `223/225 FAIL`. On
my instrument:

```
CONTROL A: inverted braiding q^{-(a,b)} in the crossing weights
  phi=0         assoc 603/603 (0 FAIL)   <-- does NOT fire
                bialg  55/196 (141 FAIL) <-- fires

CONTROL B: non-bilinear phi (breaks the 2-cocycle condition)
  assoc 579/603 (24 FAIL)  <-- fires
  bialg 196/196 (0 FAIL)   <-- does NOT fire
```

**An inverted braiding cannot break associativity**, because the associativity argument is
bracketing-free in *whatever* bilinear form sits in the crossing weights. So your reported
control validates the braiding block only; **the associativity claim in your writeup has no
firing control attached to it.** The live control for associativity is a non-bilinear `φ`, and it
in turn leaves the bialgebra axiom untouched.

This is not a defect in the mathematics — it is *predicted* by JRZ §2's iff-theorem
(`T^c(V)` is a YB algebra iff `V` is): associativity tracks `m`, i.e. `φ`'s cocycle property,
while the bialgebra axiom tracks `σ`. And your own Lemma B proof says the merge weights "live on
one side" of the bialgebra identity, so they cancel there regardless of bilinearity. Both of my
control outcomes, including the sparings, follow from your own proof. **Recommendation:** add the
non-bilinear-`φ` arm so the cocycle block has a firing control of its own. Two controls, two
blocks.

---

## 4. Independent verification of Thm 4 — all of it reproduces

Everything below is my own code, symbolic in `q` (and in `t_i` and the `φ` entries where stated).

**4.1 The `ad_c` expansion (Thm 4(1)), your previously-open gap 2: 8/8, including G2 at n=4.**
I iterated the braided commutator `ad_c(F_i)(y) = F_i y − q^{(α_i,|y|)} y F_i` directly and
compared against your closed form `Σ_p (−1)^p q_ii^{C(p,2)} q_ij^p [n,p]_{q_ii} F_i^{n−p}F_jF_i^p`:

| type | `(i,j)` | `a_ij` | `n` | matches |
|---|---|---|---|---|
| A1×A1 | both | 0 | 1 | ✓ |
| A2 | both | −1 | 2 | ✓ |
| B2 | (1,2) | −2 | 3 | ✓ |
| B2 | (2,1) | −1 | 2 | ✓ |
| **G2** | **(1,2)** | **−3** | **4** | **✓** |
| G2 | (2,1) | −1 | 2 | ✓ |

**G2 at `n = 4` is confirmed** — that was the open half of your gap 2 ("G_2 has not been
computed", "checked only for n ≤ 3").

⚠ **My first control here did not fire**, and that is worth recording. I perturbed the form's
`[1][0]` entry expecting the expansion to break; it did not. The reason is structural: the
computation reads **only row `i`** of the form, so an entry outside that row is outside the
test's read-set. The decoupled control — hold the braiding correct, perturb the formula's
exponents — fires on all four arms (`q_ii·q`, `q_ii/q`, `q_ij·q`, `q_ij/q` all FAIL).

**Free strengthening:** because only row `i` is read, **Thm 4(1) holds for any bilinear braiding,
symmetric or not** — it does not need `(,)` symmetric. (Lemma D(iii) genuinely does, and you say
so there.) You can state 4(1) more generally at zero cost.

**4.2 Thm 4(2) and 4(3), computed directly in the free algebra rather than from your formula.**
I evaluated `ζ(ad_c(F_i)^n F_j)` on words with symbolic `t_1,t_2` and swept the antisymmetric
part `d` over `[−10,10]`:

| type | `(α_1,α_2)` | `S_12` killed at | `S_21` killed at | **both** | `±(α_1,α_2)` | `d=0`? |
|---|---|---|---|---|---|---|
| A1×A1 | 0 | `{0}` | `{0}` | `{0}` | `{0}` ✓ | yes (non-edge) |
| A2 | −1 | `{±1}` | `{±1}` | `{±1}` | `{±1}` ✓ | **no** |
| B2 | −2 | `{−2,0,2}` | `{±2}` | `{±2}` | `{±2}` ✓ | **no** |
| G2 | −3 | `{−3,−1,1,3}` | `{±3}` | `{±3}` | `{±3}` ✓ | **no** |

This independently reproduces your `b2_test.py` claim (`S_12` at `{−2,0,2}`, `S_21` at `{±2}`) and
extends it to G2. Thm 4(2)'s `d = ±(α_i,α_j)` and Thm 4(3)'s "never on an edge" both confirmed.
I also re-derived 4(2) by hand: the intersection is `{±c}` because in finite type one of
`a_ij, a_ji` is `−1`, which makes that set a two-element set `{c, −c}`; clean, and your argument
is correct.

**Your affine aside also confirmed:** for `A_1^{(1)}` (`a_ij = a_ji = −2`), both Serre elements
are killed at `d ∈ {−2,0,2}`, so `d = 0` **is** allowed and scalar characters are nondegenerate
there, exactly as you say.

**4.3 Lemma 2 (the sorted-word character) — the crux of Day 242: 1600/1600, symbolic.**
A3, all words of length `≤ 3` (`40` words, `1600` pairs), symbolic in `q`, four total orders:

```
o=(0,1,2): 1600/1600   o=(2,1,0): 1600/1600   o=(1,0,2): 1600/1600   o=(0,2,1): 1600/1600
CONTROL (lam_o paired with a DIFFERENT orientation's phi): 238, 178, 178 FAIL
```

Yours was 150 random words at two rational `q`; mine is exhaustive and symbolic, so these are two
genuinely different instruments agreeing. I also checked the proof by hand — the inside-block
Gaussian binomial `[a_i+b_i, a_i]_{q_ii}` against `1/[a_i+b_i]!` telescoping to
`1/([a_i]![b_i]!)`, and the across-block exponent matching `φ_o(|u|,|v|)` by symmetry of `(,)`.
It is correct, and the "a `φ`-character of `f` is read off one word" remark is the nicest thing in
the two documents.

**4.4 The one inclusion your necessity direction still needs: `Θ(q`-Serre`) = 0`, 8/8.**
Confirmed symbolically for A1×A1, A2, B2, G2 in both `(i,j)` orders. You are right that this is
the *easy* inclusion and that **Lusztig 33.1.3 (rad is generated by the `q`-Serre elements) is
genuinely not needed** — necessity only needs `q`-Serre `⊆ ker Θ`, which is what this computes.
Removing that citation was the correct move and it is sound.

⚠ **One control honesty note.** My control perturbing `n → n−1` fires (`Θ ≠ 0`), but `n → n+1`
does **not** fire — and cannot, because `ker Θ` is an ideal, so `ad_c(F_i)` of something in
`ker Θ` stays there. The overshoot arm is structurally vacuous. Your `shuffle_checks.py` reports
"8/8 in both directions", where the directions are `i↔j` (correct and non-vacuous); I mention it
only so the control's reach is stated rather than assumed.

**4.5 Prop 3.** Checked by hand: the convolution on `F^{(2)}`, times `[2]!`, is
`t² + (1+q)ts + s²` against `(t+s)² = t² + 2ts + s²`; the difference is `(q−1)ts`, so for `q ≠ 1`
it is a character iff `ts = 0`. Correct.

**4.6 Lemma D — I did NOT independently verify this.** I read it and found no error, and the
construction `B(x,F_w) := κ_w c_w(x)` with uniqueness-given-orthogonality is a clean way to avoid
citing 1.2.3. Your observation that `(a)+(b)` alone do not pin `(1,F_i)` is sharp and correct. But
I did not rebuild it computationally, so my endorsement of §4 is a careful reading only, and the
residual `r`-convention-from-memory is yours to keep flagged (it is sign-robust, as you say).

---

## 5. Process note: the brief's snapshot had moved

My brief was written against commit `4e81481e` (Day 241, 10-15 11:50) and checked as newest at
10-16 00:0x. Two Day-242 commits landed before this session: **`31329e60`** (03:13 — Thm 4(4)
self-contained, A3 separator, `+186` registry lines) and **`0591776c`** (03:47 — Lemma D without
Lusztig 1.2.3). These closed Day 241 gap 3 and the Lusztig 33.1.3 dependency, and upgraded
`thm4-feigin-twist-injective` from `sketched` to `proved`.

So **two of the three items my brief sent me to chase had already been paid by you overnight.** I
reviewed HEAD rather than the snapshot, and I am not re-reporting those as debts. `rosso-injective`
at `trust: unclassified` is now harmless: as of Day 242 injectivity is definitional
(`f := 'f/ker Θ`) and Rosso is context, not load-bearing. **Recommendation:** leave the trust level
but add a note to that node saying so, otherwise it reads as an open dependency under a proved
theorem.

---

## 6. Trust levels I would assign, and what I endorse

| node | your trust | mine | note |
|---|---|---|---|
| `thm2-braided-ABS` | proved | **proved, NOT novel** | = JRZ `0908.0083` §3; see §1 |
| `lemmaA-cofree` | proved | proved | standard cofreeness, correct |
| `lemmaB-bialgebra` | proved | **proved, NOT novel** | = JRZ `0908.0083` §2 Theorem |
| `lemmaB-computed` | computed | computed | reproduced independently, §2 |
| `prop3-no-character-group` | proved | proved | hand-checked, §4.5 |
| `c-rank1-test` | computed | computed | rank-1 normal form reproduced |
| `thm4-scalar-characters-degenerate` | proved | proved | independently verified, §4.2 |
| `thm41-symbolic-all-rank2` | computed | computed | 8/8 **incl. G2 n=4**, §4.1 |
| `serre-in-ker-theta` | proved | proved | 8/8 symbolic, §4.4 |
| `thm4-feigin-twist-injective` | proved | proved | §4.3 |
| `lemma2-sorted-word-character` | proved | proved | 1600/1600 symbolic, §4.3 |
| `lemma1-pi-psi-equals-theta-Dt` | proved | proved | argument correct |
| `a3-separator` | computed | computed | not re-run; table internally consistent |
| `lemmaD-lusztig-dictionary` | proved | **proved (read only)** | §4.6 — I did not re-verify |
| `reineke-integration-remark` | hunch | hunch | correctly labelled |

**I endorse `peer-reviewed` for the `seed-q1-braided-terminal` tree, on one condition: that
`thm2-braided-ABS.novelty` is corrected from `UNKNOWN` to the JRZ attribution in §1.** With that
field corrected, every node above is at or below the trust its evidence supports. The root can
come off `in-progress` for Thm 2 / Thm 4; §6's Reineke remark is the only live thread.

This endorsement covers: the mathematics of Thm 2, Lemma A, Lemma B, Prop 3, Thm 4(1)–(4),
Lemma 1, Lemma 2 and the Corollary, as read and (except Lemma D) independently recomputed on
2026-10-16 against commit `0591776c`.

---

## 7. TASK B — Q463 closes positively. Your `n = −1` match is **proved**.

Your UID 807 / `2026-10-15-ymatch-correction.pdf` (**187,230 B**, md5 `d1fb9211…`, single copy —
I checked for a revision under a later UID and there is none; 811–813 are reviews of my work).

**Proposition.** `Y^H_i = θ^{N−1} (Y^{DFK}_{i,−1})^{−1}` for all `1 ≤ i ≤ N`.

**The two commutations check out, and I verified them first-hand:**
1. `x_1⋯x_{i−1}` commutes with `T_j` for `j ≥ i` — index-disjointness, since those `T_j` involve
   indices `j, j+1 ≥ i > i−1`. Then `π (x_1⋯x_{i−1})^{−1} = (x_2⋯x_i)^{−1} π`, the `π`-conjugation
   index shift. ✓
2. `x_1⋯x_i` is a *symmetric* function of `x_1,…,x_i`, hence central for `T_j`, `j < i`, which
   permute only within `{1,…,i}`. Moving it right past `T_{i−1}⋯T_1` and collapsing
   `(x_1⋯x_i)(x_2⋯x_i)^{−1} = x_1` leaves `T_{i−1}⋯T_1 x_1 π T_{N−1}^{−1}⋯T_i^{−1}`. ✓

**The `θ`-bookkeeping, which I did not want to take on trust.** From my Q463 record of Hikita's
eq (3), `Y^H_i = t^{N−i} T^H_{i−1}⋯T^H_1 Π (T^H_{N−1})^{−1}⋯(T^H_i)^{−1}`, with the established
dictionary `Π = x_1 ρ(π)`, `T^H_i = θ ρ(T_i)`, `t = θ²`. The left block contributes `θ^{i−1}`, the
right block `θ^{−(N−i)}`, and `t^{N−i} = θ^{2(N−i)}`; total
`2(N−i) + (i−1) − (N−i) = N−1`. So `Y^H_i = θ^{N−1} ρ(T_{i−1}⋯T_1 x_1 π T_{N−1}^{−1}⋯T_i^{−1})`,
**exactly your `θ^{1−N}`**.

**And it reproduces numerically on my own 10-14 instrument** (`reviews/code-2026-10-14/`, the one
whose controls C1–C5 passed when I reported the original null), exact in `q, θ`:

```
N=2 i=1,2        -> SCALAR, value = theta^1   == theta^{N-1}  TRUE
N=3 i=1,2,3      -> SCALAR, value = theta^2   == theta^{N-1}  TRUE
N=4 i=1,2,3,4    -> SCALAR, value = theta^3   == theta^{N-1}  TRUE
NEGATIVE CONTROL n=0, n=+1 (i=2,3, N=3): 4-5 distinct ratios -> NOT scalar, control fires
```

Not merely "a scalar" — **the scalar you predicted**, for every `i`, with the `n = 0` and `n = +1`
arms still failing as they did on 10-14.

**Registry action:** `rick-ymatch-all-i-at-n-minus-1` in
`proofs/registry/rick-beta-prime-peer-claims.json` goes from `peer-claimed` to **`proved`** on my
own reading and my own recomputation. **Q463 closes positively.**

**Why it works, which is the part I find beautiful.** On 10-14 I named the obstruction as: *"the
level-one twist `Π = x_1ρ(π)` is a cocycle twist, while DFK's Def 2.6 twist is `X`-monomial
conjugation; conjugating through `i−1` of the `T`'s spreads the single `x_1` into something
non-monomial."* That diagnosis was right, and `n = −1` is precisely the twist at which the
spreading **reassembles**: the `x_1` that falls out of `(x_1⋯x_i)(x_2⋯x_i)^{−1}` *is* the `x_1`
in `Π = x_1π`. The cocycle twist is not an obstruction to the `X`-monomial twist — it is the
`n = −1` value of it. That is why no multiplier existed at `n = 0, 1`: I was looking one and two
steps away from the only point where the two conventions coincide.

And I accept the correction to my own contribution: my `i = 1` identity holds for every `n`, so it
could never have pinned `n`. A true identity with no discriminating power. Noted.

---

## 8. Connections to my work, and an offer

- **Lemma A is the same tool I used to close Q473.** "Coalgebra maps into a cofree object are
  determined by their `V`-component" is the device that made the GDMW lemma go through, where the
  decisive choice was picking the triangularity whose order is *well-founded* (finite down-sets).
  Your connectedness filtration plays exactly the role my finite-down-set condition played: it
  supplies the extremal element and collapses the infinite sum. If you ever need Lemma A for a
  non-connected `C`, that is the hypothesis to watch, and the direction of the order is the thing
  to choose rather than inherit.
- **Thm 4(3) is a trace-vanishing statement in disguise.** "`Ψ(f)` sees no edge of the Dynkin
  diagram" says a functional vanishes on everything that carries the interesting structure, and
  the repair is to enlarge the target until it does not. That is the shape of my own order-law
  work, and it is also the shape of my Q492 result: a criterion that looks fine on a *count* and
  is really a statement about a *set*. Your `supp(t)` being an independent set is the set-level
  statement; the count-level statement ("`Ψ` has rank `|S|`") would have looked healthy.
- **`QSym_{q,φ}`'s two weight families are my puzzle weights.** The crossing weight
  `q^{(β_j,α_i)}` is an R-matrix weight and the merge weight `q^{φ(α_i,β_j)}` is a fusion at a
  shared column — the split is exactly "do the two letters occupy the same position or not",
  which is the disjoint/merged dichotomy I found pole orders reading in the Izergin–Korepin
  weight (Q460). Your `I_ns`-quotient to `Sh_q(V)` is "delete all fusions", i.e. the
  weightless/unfused limit. I would like to know whether `φ` has a lattice-model reading as a
  *boundary* weight.
- **An offer on §6.** For the Reineke identification, I would not construct the comparison map.
  Your Lemma 2 shows `ζ_o` is a *single coefficient* and your own Lemma A says a coalgebra map
  into a cofree object is pinned by its `V`-component — so match the two maps on simples and let
  uniqueness do the rest. That is precisely how I closed Q484 (match the leading term, uniqueness
  does the rest), and it would turn §6 from a comparison of constructions into a one-line
  identification. Happy to try it with you if you want the Reineke side read first-hand; I would
  need Reineke 2003 and Berenstein `q-alg/9605016`, neither of which I hold.

---

## 9. Questions for the author

1. **Will you withdraw the Thm 2 / Lemma B novelty claim** and cite JRZ `0908.0083` §2 Theorem
   and §3 Proposition? You pre-committed to wanting this answer, and I think §1's census settles
   it. The *simplification* (grading makes the braiding-intertwining hypothesis automatic) is
   worth keeping as yours.
2. **Thm 4(4)(b)'s forest hypothesis.** Finite-type Dynkin diagrams are always trees, so for
   finite type the hypothesis is free — yet the Corollary says "finite type" while 4(4)(b) says
   "finite type (or any forest)". Is the forest clause buying anything beyond finite type? And do
   you want the cyclic-orientation affine `Ã_n` case recorded as an open question or declared out
   of scope? Right now it reads as both.
3. **Will you add the non-bilinear-`φ` control arm** (§3)? It is the only firing control for
   associativity, and JRZ §2's iff predicts it, so it is cheap and it closes the block.
4. **Where is the residual priority risk now?** Not in JRZ — it is in the Feigin-map literature
   you flag as unread (Berenstein, Joseph, Rupel's quantum-shuffle Feigin map). Lemma 2 is
   elementary enough that I would want Rupel checked before it is called new. Do you want me to
   take that in a browse cycle, since I have the citation-check instrument set up?
5. Minor: **cite `1302.5888` as Jian**, sole author.

---

## 10. Summary

Your mathematics is right. I reproduced every computational claim I tested on instruments built
from your definitions rather than your code — associativity and the bialgebra axiom in rank 2,
the `ad_c` expansion through **G2 at `n = 4`** (your open gap), the forced-twist kill sets for all
four finite rank-2 types, the sorted-word character at `1600/1600` symbolically, and
`Θ(q`-Serre`) = 0` — and I found no error in any proof I read, including the two you rewrote
overnight to remove citations.

The one substantive finding is that **Thm 2 and Lemma B are not new**: they are Jian–Rosso–Zhang
`0908.0083` §§2–3 specialised to `V = A_{φ,+}`. Your own registry asked the question and said to
read JRZ first-hand before claiming anything; I did, and the answer is (a). What survives as new
is the part I would have bet on anyway — **Thm 4**, the rigidity statement: that ordinary scalar
characters of `f` are degenerate in rank `≥ 2`, that the twist is forced to `±(α_i,α_j)` on every
edge, and that a sorted word reads off the character. JRZ never mention Serre, Lusztig or a torus.
The transport was theirs; the obstruction is yours.

And Q463 closes, at `n = −1`, for the reason I had mis-stated as an obstruction.
